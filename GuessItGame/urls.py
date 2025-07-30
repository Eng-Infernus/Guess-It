# GuessItGame/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('setup/', views.game_setup, name='game_setup'),
    path('categories/', views.category_selection, name='category_selection'),
    path('board/', views.game_board, name='game_board'),
    path('question/<str:category_name>/<int:points>/', views.question_view, name='question'),
    path('submit/', views.submit_answer, name='submit_answer'),
    path('hint/', views.use_hint, name='use_hint'),
    path('result/', views.result, name='result'),
    path('scores/', views.final_scores, name='final_scores'),
    path('end-game/', views.end_game, name='end_game'),

]