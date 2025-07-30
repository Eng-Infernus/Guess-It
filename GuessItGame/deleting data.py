import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'GuessIT.settings')  # Replace 'GuessIT' with your project name
django.setup()

from GuessItGame.models import Category, Question, QuestionAnswers, TeamAnswers, GameCategory, GameTeam, Game, Team, \
    Users


def delete_all_data():
    """Delete all data from the database in proper order to avoid foreign key constraints"""

    print("🗑️  Starting database cleanup...")

    # Delete in reverse order of dependencies to avoid foreign key constraint errors

    # 1. Delete TeamAnswers (depends on Team and Question)
    team_answers_count = TeamAnswers.objects.count()
    TeamAnswers.objects.all().delete()
    print(f"✔ Deleted {team_answers_count} team answers")

    # 2. Delete QuestionAnswers (depends on Question)
    question_answers_count = QuestionAnswers.objects.count()
    QuestionAnswers.objects.all().delete()
    print(f"✔ Deleted {question_answers_count} question answers")

    # 3. Delete Questions (depends on Category)
    questions_count = Question.objects.count()
    Question.objects.all().delete()
    print(f"✔ Deleted {questions_count} questions")

    # 4. Delete GameCategory (many-to-many through table)
    game_categories_count = GameCategory.objects.count()
    GameCategory.objects.all().delete()
    print(f"✔ Deleted {game_categories_count} game-category relationships")

    # 5. Delete GameTeam (many-to-many through table)
    game_teams_count = GameTeam.objects.count()
    GameTeam.objects.all().delete()
    print(f"✔ Deleted {game_teams_count} game-team relationships")

    # 6. Delete Games (depends on Users)
    games_count = Game.objects.count()
    Game.objects.all().delete()
    print(f"✔ Deleted {games_count} games")

    # 7. Delete Teams
    teams_count = Team.objects.count()
    Team.objects.all().delete()
    print(f"✔ Deleted {teams_count} teams")

    # 8. Delete Categories
    categories_count = Category.objects.count()
    Category.objects.all().delete()
    print(f"✔ Deleted {categories_count} categories")

    # 9. Delete Users (no dependencies)
    users_count = Users.objects.count()
    Users.objects.all().delete()
    print(f"✔ Deleted {users_count} users")

    print("🎉 Database cleanup completed successfully!")


def delete_only_seed_data():
    """Delete only the seed data (questions, answers, categories) but keep users, games, teams"""

    print("🗑️  Starting seed data cleanup...")

    # Delete only seed-related data
    question_answers_count = QuestionAnswers.objects.count()
    QuestionAnswers.objects.all().delete()
    print(f"✔ Deleted {question_answers_count} question answers")

    questions_count = Question.objects.count()
    Question.objects.all().delete()
    print(f"✔ Deleted {questions_count} questions")

    # Delete game-category relationships
    game_categories_count = GameCategory.objects.count()
    GameCategory.objects.all().delete()
    print(f"✔ Deleted {game_categories_count} game-category relationships")

    categories_count = Category.objects.count()
    Category.objects.all().delete()
    print(f"✔ Deleted {categories_count} categories")

    print("🎉 Seed data cleanup completed successfully!")


def confirm_deletion():
    """Ask for confirmation before deleting"""
    print("⚠️  WARNING: This will delete data from your database!")
    print("\nChoose an option:")
    print("1. Delete ALL data (users, games, teams, questions, everything)")
    print("2. Delete ONLY seed data (questions, answers, categories)")
    print("3. Cancel")

    choice = input("\nEnter your choice (1/2/3): ").strip()

    if choice == "1":
        confirm = input("Are you sure you want to delete ALL data? Type 'YES' to confirm: ")
        if confirm == "YES":
            delete_all_data()
        else:
            print("❌ Deletion cancelled")
    elif choice == "2":
        confirm = input("Are you sure you want to delete seed data? Type 'YES' to confirm: ")
        if confirm == "YES":
            delete_only_seed_data()
        else:
            print("❌ Deletion cancelled")
    elif choice == "3":
        print("❌ Operation cancelled")
    else:
        print("❌ Invalid choice")


if __name__ == "__main__":
    confirm_deletion()