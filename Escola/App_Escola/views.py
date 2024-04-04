from django.shortcuts import render
from hashlib import sha256
from .models import Professor, Turma, Atividade
from django.db import connection, transaction
from django.contrib import messages # Biblioteca de mansagem 

# Create your views here.
def abre_index(request):
    return render(request, 'Index.html')

def abre_login(request):
    return render(request, 'login.html')

def abre_telaProfessor(request):
    return render(request, 'telaProfessor.html')

def abre_cadastroTurma(request):
    return render(request, 'cadastroTurma.html')

def abre_cadastroAtividade(request):
    return render(request, 'cadastroAtividade.html')


def initial_population():
    print("Populando o Banco de dados")
    
    cursor = connection.cursor()
    
    # ---------------------- Popular Tabela Professor 
    senha = "123456"
    senha_armazenar = sha256(senha.encode()).hexdigest()
    # Montamos aqui a instrução sql
    insert_sql_professor = "INSERT INTO App_Escola_professor (nome,email,senha) VALEUS "
    insert_sql_professor = insert_sql_professor + "('Prof. Barak Obama', 'barak.obama@gmail.com', '" + senha_armazenar + "'),"
    insert_sql_professor = insert_sql_professor + "('Profa. Angela Merkel', 'angela.merkel@gmail.com', '"+ senha_armazenar +"'),"
    insert_sql_professor = insert_sql_professor + "('Prof. Xi Jinping', 'xi.jinping@gmail.com', '"+ senha_armazenar +"')"
    
    cursor.execute(insert_sql_professor)
    transaction.atomic() # Necessario commit para insert e update
    # Fim da População da tabela Professor
    
    # ---------------------- Popular Tabela Turma
    # Montamos aqui a instrução sql
    insert_sql_turma = "INSERT INTO App_Escola_turma (nome_turma, id_professor_id) VALEUS"
    insert_sql_turma = insert_sql_turma + "('1° Semestre - Desenvolvimento de Sistemas', 1),"
    insert_sql_turma = insert_sql_turma + "('2° Semestre - Desenvolvimento de Sistemas', 2),"
    insert_sql_turma = insert_sql_turma + "('3° Semestre - Desenvolvimento de Sistemas', 3)"
    
    cursor.execute(insert_sql_turma) 
    transaction.atomic() # Necessario commit para insert e update
    # Fim da População da tabela Atividade
    
    
    # ---------------------- Popular Tabela Atividade
    # Montamos aqui a instrução sql
    insert_sql_atividade = "INSERT INTO App_Escola_atividade (nome_atividade, id_turma_id) VALEUS"
    insert_sql_atividade = insert_sql_atividade + "('Apresentar Fundamentos da Programação', 1),"
    insert_sql_turma = insert_sql_atividade + "('Apresentar FrameWork Django', 2),"
    insert_sql_atividade = insert_sql_atividade + "('Apresentar conceitos de Gerenciamento de Projetos', 3)"
    
    cursor.execute(insert_sql_atividade) 
    transaction.atomic() # Necessario commit para insert e update
    # Fim da População da tabela Atividade