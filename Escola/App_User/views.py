from django.shortcuts import render
from django.contrib import messages # Biblioteca de mensagens do django
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# Create your views here.

def formulario_novo_user(request):
    return render(request, 'Cad_User.html')

@login_required
def salvar_usuario(request):
    usuario = request.POST.get('usuario')
    email = request.POST.get('email')
    senha = request.POST.get('senha')
    
    usuario_logado = request.user.username
    
    if usuario != None and usuario != '' and email != None and email != '' and senha != None and senha != '':
        try:
            tem_usuario = User.objects.get(username=usuario)
            
            if tem_usuario:
                messages.info(request, 'Usuario ' + usuario + ' já existe no sistema. Tente outro nome')
                return render(request, 'Cad_User.html', {'usuario_logado': usuario_logado})
            
        except User.DoesNotExist:
            dados_usuario = User.objects.create_user(username=usuario, email=email, password=senha)
            dados_usuario.save()
            messages.info(request, 'Usuario ' + usuario + ' cadastro com sucesso')
            return render(request, 'Cad_User.html', {'usuario_logado': usuario_logado})