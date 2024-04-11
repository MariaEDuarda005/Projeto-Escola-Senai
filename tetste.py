from django.http import HttpResponse
from django.shortcuts import render
from hashlib import sha256
from .models import Professor, Turma, Atividade
from django.db import connection, transaction
from django.contrib import messages #Biblioteca de mensagens de Django
 
# Create your views here.
 
def initial_population():
 
    print("Vou popular")
 
    cursor = connection.cursor()
 
    # Popular Tabela Professor
    senha = '123456' # senha inical
    senha_armazenar = sha256(senha.encode()).hexdigest()
    insert_sql_professor = "INSERT INTO App_Escola_professor (nome, email, senha) VALUES"
    insert_sql_professor = insert_sql_professor + "('Prof, Barak Obama', 'barak.obama@gmail.com', '" + senha_armazenar + "'),"
    insert_sql_professor = insert_sql_professor + "('Profa, Angela Markel', 'angela.markel@gmail.com', '" + senha_armazenar + "'),"
    insert_sql_professor = insert_sql_professor + "('Prof, Xi Jinping', 'xi.jinping@gmail.com', '" + senha_armazenar + "')"
    print('\ninseriu professor\n')
    cursor.execute(insert_sql_professor)
    transaction.atomic() # Necessario commit para insert e update
    # Fim da População da tabela proessor
 
    #----------------------------------------------------------------------------------------------------------------------------------------
    # Popular Tabela Turma
    #Montamos aqui nossa instrução SQL
    insert_sql_turma = "INSERT INTO App_Escola_turma (nome_turma, id_professor_id) VALUES"
    insert_sql_turma = insert_sql_turma + "('1o Semestre - Desenvolvimento de Sistemas', 1),"
    insert_sql_turma = insert_sql_turma + "('2o Semestre - Desenvolvimento de Sistemas', 2),"
    insert_sql_turma = insert_sql_turma + "('3o Semestre - Desenvolvimento de Sistemas', 3)"
    print('\ninseriu turma\n')
 
 
    cursor.execute(insert_sql_turma)
    transaction.atomic() #Necessario commit para insert e update
 
    #Fim da população da tabela Turma
 
 
    #-----------------------------------------------------------------------------------------------------------------------------------------
    #Populando a Tabela Atividade
    #Montamos aqui nossa instrução SQL
    insert_sql_atividade = "INSERT INTO App_Escola_atividade (nome_atividade, id_turma_id) VALUES"
    insert_sql_atividade = insert_sql_atividade + "('Apresentar Fundamentos de Programação', 1),"
    insert_sql_atividade = insert_sql_atividade + "('Apresentar Framework Django', 2),"
    insert_sql_atividade = insert_sql_atividade + "('Apresentar Conceitos de Gerenciamento de Projetos', 3)"
    print('\ninseriu atividade\n')
 
    cursor.execute(insert_sql_atividade)
    transaction.atomic() #Aqui ele garante que ou ele salva todas as linhas no banco, se não não salva nenhuma
 
    #Fim da População da tabela Atividade
 
    print("Populado")
 
 
 
def abre_index(request):
    #return render(request, 'Index.html')
    dado_pesquisa = 'Obama'
 
    verifica_populado = Professor.objects.filter(nome__icontains = dado_pesquisa)
 
    if len(verifica_populado) == 0:
        print("Não está populado")
        initial_population() # chama a função para realizar a população
    else:
        print("Achei o Obama", verifica_populado)
 
    return render(request, 'Login.html')
 
def enviar_login(request):
    if (request.method == 'POST'):
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        senha_criptografada = sha256(senha.encode()).hexdigest()
        dados_professor = Professor.objects.filter(email= email).values("nome", "senha", "id")
        print("\nDados do Professor ", dados_professor)
 
        if dados_professor:
            senha = dados_professor[0]
            senha = senha['senha']
            usuario_logado = dados_professor[0]
            usuario_logado = usuario_logado['nome']
 
            if (senha == senha_criptografada):
 
                #Se logou corretamente traz as turmas do professor, para isso instalciamos o models turmas do professor
                id_logado = dados_professor[0]
                id_logado = id_logado['id']
                turmas_do_professor = Turma.objects.filter(id_professor = id_logado)
                print("\nTurma do professor ", turmas_do_professor)
 
                return render(request, 'Cons_Turma_Lista.html', {'usuario_logado': usuario_logado,
                                                                 'turmas_do_professor': turmas_do_professor,
                                                                 'id_logado': id_logado})
            else:
                messages.info(request, 'Usuario ou senha incorretos. Tente Novamente.')
                return render(request, 'Login.html')
       
        messages.info(request, 'Olá' + email + ', seja bem vindo! Percebemos que você é novo por aqui. Complete o seu cadastro.')
        return render(request, 'Cadastro.html', {'login': email})    
 
 
def confirmar_cadastro(request):
 
    if (request.method == 'POST'):
        nome = request.POST.get("nome")
        email= request.POST.get('login')
        senha = request.POST.get('senha')
        senha_criptografada = sha256(senha.encode()).hexdigest()
 
        grava_professor = Professor(
            nome = nome,
            email = email,
            senha = senha_criptografada
        )
        grava_professor.save()
 
        mensagem = "OLÁ PROFESSOR " +nome+ ", SEJA BEM VINDO!"
        return HttpResponse(mensagem)
   
    # return render(request, 'Cadastro.html')
 
 
# def abre_pageProfessor(request):
#     return render(request, 'Page_professor.html')
 
 
# def abre_cadastroTurma(request):
#     return render(request, 'CadastroTurma.html')
 
# def abre_cadastroAtividade(request):
#     return render(request, 'CadastroAtividade.html')