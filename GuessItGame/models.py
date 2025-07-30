from django.db import models


# Create your models here.

class Users(models.Model):
    username = models.CharField(max_length=50, unique=True)
    hashed_password = models.CharField(max_length=255)

    def __str__(self):
        return self.username


class Game(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name="games")
    turn = models.PositiveIntegerField(null=True, blank=True)
    tot_score = models.PositiveIntegerField(default=0)

    # many‑to‑many helpers (see through tables below)
    teams = models.ManyToManyField("Team", through="GameTeam", related_name="games")
    categories = models.ManyToManyField("Category", through="GameCategory", related_name="games")

    def __str__(self):
        return f"Game #{self.pk} (user {self.user_id})"


class Team(models.Model):
    team_name = models.CharField(max_length=100)
    color = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return self.team_name


class GameTeam(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    t_order = models.PositiveIntegerField()
    score = models.PositiveIntegerField(default=0)
    hints = models.CharField(max_length=255, blank=True)

    class Meta:
        unique_together = (("game", "team"),)


class Category(models.Model):
    category_name = models.CharField(max_length=100, primary_key=True)
    times_picked = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.category_name


class GameCategory(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        unique_together = (("game", "category"),)


class Question(models.Model):
    text = models.CharField(max_length=500)
    correct_answer = models.CharField(max_length=255)
    helper_hint_text = models.CharField(max_length=255, blank=True)
    points = models.PositiveIntegerField()
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="questions")

    def __str__(self):
        return self.text[:60]


class QuestionAnswers(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answers")
    answer_text = models.CharField(max_length=255)

    class Meta:
        unique_together = (("question", "answer_text"),)


class TeamAnswers(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    picked_answer = models.CharField(max_length=255)

    class Meta:
        unique_together = (("team", "question"),)
