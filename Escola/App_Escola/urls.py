from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.abre_index, name='abre_index'),
    path('login', views.abre_login, name='abre_login'),
    path('telaProfessor', views.abre_telaProfessor, name='telaProfessor'),
    path('cadastroTurma', views.abre_cadastroTurma, name='cadastroTurma'),
    path('cadastroAtividade', views.abre_cadastroAtividade, name='cadastroAtividade'),
]
