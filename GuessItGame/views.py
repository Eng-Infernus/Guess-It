# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.db import transaction
from .models import *
import random
import json


def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match')
            return render(request, 'register.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return render(request, 'register.html')

        user = User.objects.create_user(username=username, password=password)
        Users.objects.create(username=username, hashed_password=password)

        messages.success(request, 'Account created successfully')
        return redirect('login')

    return render(request, 'register.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('game_setup')
        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def game_setup(request):
    if request.method == 'POST':
        num_teams = int(request.POST.get('num_teams'))
        team_names = []
        team_colors = []

        for i in range(num_teams):
            team_names.append(request.POST.get(f'team_name_{i}'))
            team_colors.append(request.POST.get(f'team_color_{i}'))

        # Store team info in session
        request.session['team_names'] = team_names
        request.session['team_colors'] = team_colors
        request.session['num_teams'] = num_teams

        return redirect('category_selection')

    return render(request, 'game_setup.html')


@login_required
def category_selection(request):
    categories = Category.objects.all()

    if request.method == 'POST':
        selected_categories = request.POST.getlist('categories')

        if len(selected_categories) != 5:
            messages.error(request, 'You must select exactly 5 categories')
            return render(request, 'category_selection.html', {'categories': categories})

        # Create game and teams
        user_obj = Users.objects.get(username=request.user.username)
        game = Game.objects.create(user=user_obj, turn=0)

        # Create teams
        team_names = request.session.get('team_names')
        team_colors = request.session.get('team_colors')
        team_order = list(range(len(team_names)))
        random.shuffle(team_order)  # Randomize turn order

        # Default hints JSON
        default_hints = {
            "double_points": True,
            "remove_choices": True,
            "view_hint": True,
            "replace_question": True
        }

        for i, order_idx in enumerate(team_order):
            team = Team.objects.create(
                team_name=team_names[order_idx],
                color=team_colors[order_idx]
            )
            GameTeam.objects.create(
                game=game,
                team=team,
                t_order=i,
                hints=json.dumps(default_hints)
            )

        # Add categories to game
        for cat_name in selected_categories:
            category = Category.objects.get(category_name=cat_name)
            GameCategory.objects.create(game=game, category=category)

        request.session['game_id'] = game.id
        return redirect('game_board')

    return render(request, 'category_selection.html', {'categories': categories})


@login_required
def game_board(request):
    game_id = request.session.get('game_id')
    game = get_object_or_404(Game, id=game_id)

    # Get game teams in order
    game_teams = GameTeam.objects.filter(game=game).order_by('t_order')
    current_team = game_teams[game.turn % len(game_teams)]

    # Get categories for this game
    game_categories = GameCategory.objects.filter(game=game)
    categories = [gc.category for gc in game_categories]

    # Get available questions organized by category and points
    questions_grid = {}
    point_values = [10, 20, 30, 40, 50]

    # Get all answered/cancelled questions for this game (not just teams)
    # Get only teams in this game
    team_ids = game_teams.values_list('team_id', flat=True)

    # Get questions answered by those teams (in this game only)
    # Get all (category, points) pairs used in this game
    answered_pairs = TeamAnswers.objects.filter(
        team_id__in=team_ids
    ).values_list('question__category__category_name', 'question__points')

    answered_set = set(answered_pairs)

    for category in categories:
        questions_grid[category.category_name] = {}
        for points in point_values:
            # Mark slot unavailable if any team in this game answered that (category, points)
            questions_grid[category.category_name][points] = (
                    (category.category_name, points) not in answered_set
            )

    # Check if game is over
    total_questions = sum([sum([1 for available in cat_questions.values() if available])
                           for cat_questions in questions_grid.values()])

    context = {
        'game': game,
        'game_teams': game_teams,
        'current_team': current_team,
        'categories': categories,
        'questions_grid': questions_grid,
        'point_values': point_values,
        'game_over': total_questions == 0
    }

    return render(request, 'game_board.html', context)


def safe_json_loads(json_string, default=None):
    """Safely load JSON string with fallback to default value"""
    try:
        return json.loads(json_string)
    except (json.JSONDecodeError, TypeError, ValueError):
        return default if default is not None else {}


@login_required
def question_view(request, category_name, points):
    game_id = request.session.get('game_id')
    game = get_object_or_404(Game, id=game_id)
    game_teams = GameTeam.objects.filter(game=game).order_by('t_order')
    current_team = game_teams[game.turn % len(game_teams)]

    category = get_object_or_404(Category, category_name=category_name)

    # Get available questions (exclude ALL answered questions, not just by teams)
    team_ids = game_teams.values_list('team_id', flat=True)

    answered_questions = TeamAnswers.objects.filter(
        team_id__in=team_ids,
        question__category=category
    ).values_list('question_id', flat=True)

    available_questions = Question.objects.filter(
        category=category,
        points=points
    ).exclude(id__in=answered_questions)

    if not available_questions.exists():
        messages.error(request, 'No questions available for this category and point value')
        return redirect('game_board')

    # Select random question
    question = random.choice(available_questions)

    # Get all answer choices
    answers = list(QuestionAnswers.objects.filter(question=question).values_list('answer_text', flat=True))
    random.shuffle(answers)

    # Get current team's available hints with safe JSON loading
    default_hints = {
        "double_points": True,
        "remove_choices": True,
        "view_hint": True,
        "replace_question": True
    }

    hints_data = safe_json_loads(current_team.hints, default_hints)

    context = {
        'question': question,
        'answers': answers,
        'current_team': current_team,
        'game': game,
        'available_hints': hints_data,
        'category_name': category_name,
        'points': points
    }

    return render(request, 'question.html', context)


@login_required
def submit_answer(request):
    if request.method == 'POST':
        game_id = request.session.get('game_id')
        game = get_object_or_404(Game, id=game_id)
        game_teams = GameTeam.objects.filter(game=game).order_by('t_order')
        current_team = game_teams[game.turn % len(game_teams)]

        question_id = request.POST.get('question_id')
        selected_answer = request.POST.get('selected_answer')
        double_points_requested = request.POST.get('double_points') == 'true'

        question = get_object_or_404(Question, id=question_id)

        # Always record the answer to mark question as used/cancelled
        TeamAnswers.objects.create(
            team=current_team.team,
            question=question,
            picked_answer=selected_answer
        )

        # Load and check hint availability
        default_hints = {
            "double_points": True,
            "remove_choices": True,
            "view_hint": True,
            "replace_question": True
        }
        hints_data = safe_json_loads(current_team.hints, default_hints)
        is_double_allowed = double_points_requested and hints_data.get("double_points", False)

        # Check if correct
        is_correct = selected_answer == question.correct_answer
        points_awarded = 0

        if is_correct:
            points_awarded = question.points
            if is_double_allowed:
                points_awarded *= 2
                # Mark double_points as used
                hints_data["double_points"] = False
                current_team.hints = json.dumps(hints_data)
                current_team.save()

            current_team.score += points_awarded
            current_team.save()

            game.tot_score += points_awarded
            game.save()

        # Move to next turn
        game.turn += 1
        game.save()

        request.session['last_result'] = {
            'correct': is_correct,
            'points_awarded': points_awarded,
            'correct_answer': question.correct_answer,
            'team_name': current_team.team.team_name
        }

        return redirect('result')

    return redirect('game_board')


@login_required
def use_hint(request):
    if request.method == 'POST':
        game_id = request.session.get('game_id')
        game = get_object_or_404(Game, id=game_id)
        game_teams = GameTeam.objects.filter(game=game).order_by('t_order')
        current_team = game_teams[game.turn % len(game_teams)]

        hint_type = request.POST.get('hint_type')
        question_id = request.POST.get('question_id')

        question = get_object_or_404(Question, id=question_id)

        # Safe JSON loading with default hints
        default_hints = {
            "double_points": True,
            "remove_choices": True,
            "view_hint": True,
            "replace_question": True
        }
        hints_data = safe_json_loads(current_team.hints, default_hints)

        if not hints_data.get(hint_type, False):
            return JsonResponse({'status': 'error', 'message': 'Hint not available'}, status=400)

        # Use the hint
        hints_data[hint_type] = False
        current_team.hints = json.dumps(hints_data)
        current_team.save()

        response_data = {'status': 'success', 'hint_used': hint_type}

        if hint_type == 'remove_choices':
            # Remove 2 wrong answers (ensure correct answer is never removed)
            all_answers = list(QuestionAnswers.objects.filter(question=question).values_list('answer_text', flat=True))
            wrong_answers = [ans for ans in all_answers if ans != question.correct_answer]

            # Shuffle and take up to 2 wrong answers (in case there are fewer than 2 wrong answers)
            random.shuffle(wrong_answers)
            removed_choices = wrong_answers[:min(2, len(wrong_answers))]
            response_data['removed_choices'] = removed_choices

        elif hint_type == 'view_hint':
            response_data['hint_text'] = question.helper_hint_text

        elif hint_type == 'replace_question':
            # Mark current question as answered/cancelled to remove it from pool
            TeamAnswers.objects.create(
                team=current_team.team,
                question=question,
                picked_answer='REPLACED'
            )

            team_ids = game_teams.values_list('team_id', flat=True)

            answered_questions = TeamAnswers.objects.filter(
                team_id__in=team_ids,
                question__category=question.category
            ).values_list('question_id', flat=True)

            replacement_questions = Question.objects.filter(
                category=question.category,
                points=question.points
            ).exclude(id__in=answered_questions)

            if replacement_questions.exists():
                new_question = random.choice(replacement_questions)
                new_answers = list(
                    QuestionAnswers.objects.filter(question=new_question).values_list('answer_text', flat=True))
                random.shuffle(new_answers)

                response_data.update({
                    'new_question_id': new_question.id,
                    'new_question_text': new_question.text,
                    'new_answers': new_answers
                })
            else:
                response_data = {'status': 'error', 'message': 'No replacement questions available'}

        return JsonResponse(response_data)

    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)


@login_required
def result(request):
    result_data = request.session.get('last_result')
    if not result_data:
        return redirect('game_board')

    return render(request, 'result.html', {'result': result_data})


@login_required
def final_scores(request):
    game_id = request.session.get('game_id')
    game = get_object_or_404(Game, id=game_id)

    game_teams = GameTeam.objects.filter(game=game).order_by('-score')

    context = {
        'game': game,
        'game_teams': game_teams
    }

    return render(request, 'final_scores.html', context)


@login_required
def end_game(request):
    """End the current game early"""
    if request.method == 'POST':
        return redirect('final_scores')
    return redirect('game_board')
