from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.abre_index, name='abre_index'),
    path('enviar_login', views.enviar_login, name='enviar_login'),
    path('confirmar_cadastro', views.confirmar_cadastro, name='confirmar_cadastro'),
    path('cad_turma/<int:id_professor>', views.cad_turma, name='cad_turma'),
    path('salvar_turma', views.salvar_turma_nova, name='salvar_turma_nova'),
    path('lista_turma/<int:id_professor>', views.lista_turma, name='lista_turma'),
    path('excluir_turma/<int:id_turma>', views.excluir_turma, name='excluir_turma'),
    path('cad_atividade/<int:id_turma>', views.cad_atividade, name='cad_atividade'),
    path('sair', views.sair, name='sair'),
    path('atividade_arquivo/<str:nome_arquivo>', views.exibir_arquivo, name='exibir_arquivo'),
    path('exportar_excel_turma/', views.exportar_para_excel_turmas, name='exportar_excel_turma'),
    path('exportar_excel_atividade', views.exportar_para_excel_Atividades, name='exportar_excel_atividade')
]
