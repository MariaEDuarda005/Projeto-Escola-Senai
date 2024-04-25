from django.http import HttpResponse
from django.shortcuts import redirect, render
from hashlib import sha256
from .models import Professor, Turma, Atividade
from django.db import connection, transaction
from django.contrib import messages # Biblioteca de mensagens do Django 

# Create your views here.
# def abre_login(request):
#     return render(request, 'login.html')

# def abre_cadastro(request):
#     return render(request, 'cadastro.html')

def initial_population():
    print("Populando o Banco de dados")
    
    cursor = connection.cursor()
    
    # ---------------------- Popular Tabela Professor 
    senha = "123456"
    senha_armazenar = sha256(senha.encode()).hexdigest()
    # Montamos aqui a instrução sql
    insert_sql_professor = "INSERT INTO App_Escola_professor (nome,email,senha) VALUES "
    insert_sql_professor = insert_sql_professor + "('Prof. Barak Obama', 'barak.obama@gmail.com', '" + senha_armazenar + "'),"
    insert_sql_professor = insert_sql_professor + "('Profa. Angela Merkel', 'angela.merkel@gmail.com', '"+ senha_armazenar +"'),"
    insert_sql_professor = insert_sql_professor + "('Prof. Xi Jinping', 'xi.jinping@gmail.com', '"+ senha_armazenar +"')"
    
    cursor.execute(insert_sql_professor)
    transaction.atomic() # Necessario commit para insert e update
    # Fim da População da tabela Professor
    
    # ---------------------- Popular Tabela Turma
    # Montamos aqui a instrução sql
    insert_sql_turma = "INSERT INTO App_Escola_turma (nome_turma, id_professor_id) VALUES"
    insert_sql_turma = insert_sql_turma + "('1° Semestre - Desenvolvimento de Sistemas', 1),"
    insert_sql_turma = insert_sql_turma + "('2° Semestre - Desenvolvimento de Sistemas', 2),"
    insert_sql_turma = insert_sql_turma + "('3° Semestre - Desenvolvimento de Sistemas', 3)"
    
    cursor.execute(insert_sql_turma) 
    transaction.atomic() # Necessario commit para insert e update
    # Fim da População da tabela Atividade
    
    
    # ---------------------- Popular Tabela Atividade
    # Montamos aqui a instrução sql
    insert_sql_atividade = "INSERT INTO App_Escola_atividade (nome_atividade, id_turma_id) VALUES"
    insert_sql_atividade = insert_sql_atividade + "('Apresentar Fundamentos da Programação', 1),"
    insert_sql_turma = insert_sql_atividade + "('Apresentar FrameWork Django', 2),"
    insert_sql_atividade = insert_sql_atividade + "('Apresentar conceitos de Gerenciamento de Projetos', 3)"
    
    cursor.execute(insert_sql_atividade) 
    transaction.atomic() # Necessario commit para insert e update
    # Fim da População da tabela Atividade
    
def abre_index(request):
    dado_pesquisa = 'Obama'
    
    verifica_populado = Professor.objects.filter(nome__icontains=dado_pesquisa)
    
    if len(verifica_populado) == 0:
        print("Não esta populado")
        initial_population()
    else:
        print("Achei Obama", verifica_populado)
        
    return render(request, 'login.html')
        
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
                # Se logou corretamente traz as turmas do professor
                # Para isso instanciamos o model turmas professor
                id_logado = dados_professor[0]
                id_logado = id_logado['id']
                turmas_do_professor = Turma.objects.filter(id_professor = id_logado)
                print("\nTurma do professor ", turmas_do_professor)
 
                return render(request, 'telaProfessor.html', {'usuario_logado': usuario_logado,
                                                        'turma_do_professor': turmas_do_professor,
                                                        'id_logado': id_logado})
            else:
                messages.info(request, 'Usuario ou senha incorretos. Tente Novamente.')
                return render(request, 'login.html')
        
        messages.info(request, "Olá " + email + ", seja bem vindo! Percebemos que você é novo por aqui. Complete seu cadastro.")
        return render(request, 'cadastro.html', {'login': email})
    #return HttpResponse("Login enviado com sucesso!")
    
def confirmar_cadastro(request):
    if(request.method == 'POST'):
        nome = request.POST.get('nome')
        email = request.POST.get('login')
        senha = request.POST.get('senha')
        senha_criptografada = sha256(senha.encode()).hexdigest()
        
        grava_professor = Professor(
            nome=nome,
            email=email,
            senha=senha_criptografada
        )
        
        grava_professor.save()
        
        mensagem = "OLÁ PROFESSOR " + nome + ", SEJA BEM VINDO"
        print(mensagem)
        return HttpResponse(mensagem) 
        
def cad_turma(request, id_professor):
    usuario_logado = Professor.objects.filter(id=id_professor).values("nome", "id")
    usuario_logado = usuario_logado[0]
    usuario_logado = usuario_logado['nome']
    print(usuario_logado, "USUARIO LOGADO EM CAD_CLIENTE")
    return render(request, 'Cad_turma.html', {'usuario_logado': usuario_logado, 
            'id_logado': id_professor})
    # return render(request, 'Cad_turma.html', {'usuario_logado': usuario_logado, 
    #         'id_logado': id_professor, 'turmas_do_professor': turmas_do_professor})

def salvar_turma_nova(request):
    if(request.method == 'POST'):
        nome_turma = request.POST.get('nome_turma')
        id_professor = request.POST.get('id_professor')
        professor = Professor.objects.get(id=id_professor)
        grava_turma = Turma(
            nome_turma=nome_turma,
            id_professor=professor
        )
        
        grava_turma.save()
        messages.info(request, 'Turma ' + nome_turma + ' cadastrado com sucesso.')
        
        # Redirecionar para uma nova URL apos a gravação bem sucedida
        return redirect('lista_turma', id_professor=id_professor)
    
def lista_turma(request, id_professor):
    dados_professor = Professor.objects.filter(id=id_professor).values("nome", "id")
    usuario_logado = dados_professor[0]
    usuario_logado = usuario_logado['nome']
    id_logado = dados_professor[0]
    id_logado = id_logado['id']
    turmas_do_professor = Turma.objects.filter(id_professor=id_logado)
    print(turmas_do_professor)
    return render(request, 'telaProfessor.html', {'usuario_logado': usuario_logado,
                                                  'turma_do_professor': turmas_do_professor,
                                                  'id_logado': id_logado})
            
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

def excluir_turma(request, id_turma):
    try:
        with transaction.atomic():
            turma = Turma.objects.get(pk=id_turma)
            id_professor = turma.id_professor_id
            print(id_professor)
            turma.delete()

            professor = Professor.objects.get(pk=id_professor)
            turmas_professor = Turma.objects.filter(id_professor=id_professor)
            print(f'>>>professor{id_professor}')

        # return render(request, "telaProfessor.html", {
        #     "turmas_professor": turmas_professor,
        #     "id_logado": id_professor
        return redirect('lista_turma', id_professor=id_professor)
        
    except Turma.DoesNotExist:
        return HttpResponse("Turma not found.", status=404)

def cad_atividade(request, id_turma):
    turma = Turma.objects.get(pk=id_turma)
    atividades_turma = Atividade.objects.filter(id_turma_id=id_turma)
    arquivo = request.FILES.get('arquivo') # Obtem o arquivo enviado pelo formulario
    if request.method == "POST":
        descricao = request.POST["descricao"]
        turma = Turma.objects.get(pk=id_turma)

        # atomicidade, só entra nessa parte se o resto estiver correto
        with transaction.atomic():
            grava_atividade = Atividade(
                nome_atividade=descricao, 
                id_turma=turma, 
                arquivo=arquivo
            )
            grava_atividade.save()
        
        atividades_turma = Atividade.objects.filter(id_turma_id = id_turma)

        return render(request, "turmaAtividade.html",{
            # contexto, leva as informações para a pagina html
            "id_turma": id_turma,
            "atividades": atividades_turma
        })
       
        
    return render(request, "turmaAtividade.html", {
        "id_turma": id_turma,
        "atividades": atividades_turma
    })

# def cad_atividade(request):
#     if request.method == 'POST':
#         nome_atividade = request.POST.get('nome_atividade')
#         id_turma = request.POST.get('id_turma')
#         id_logado = request.POST.get('id_logado')
#         turma = Turma.objects.get(id=id_turma)
#         arquivo = request.FILES.get('arquivo') # Obtem o arquivo enviado pelo formulario
#         grava_atividade = Atividade(
#             nome_atividade=nome_atividade,
#             id_turma=id_turma,
#             arquivo=arquivo # Associa a atividade
#         )
#         grava_atividade.save()
#         messages.info(request, 'Atividade' + nome_atividade + ' cadastrada com sucesso.')
#         nome_da_turma = turma.nome_turma
#         dados_professor = Professor.objects.filter(id=id_logado).values("nome", "id")
#         usuario_logado = dados_professor[0]
#         usuario_logado = usuario_logado['nome']
#         atividades_da_turma = Atividade.objects.filter(id_turma=turma)
        
#         return render(request, 'turmaAtividade.html', 
#                       {'usuario logado': usuario_logado,
#                        'atividades_da_turma': atividades_da_turma,
#                        'id_logado': id_logado,
#                        'nome_da_turma': nome_da_turma})

def sair(request):
    return render(request, 'login.html')