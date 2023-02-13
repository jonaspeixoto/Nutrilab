from django.shortcuts import redirect, render
from django.http import HttpResponse
from .utils import password_is_valid
from django.contrib import messages , auth
from django.contrib.messages import constants
from django.contrib.auth.models import User
def cadastro(request):
    
    if request.user.is_authenticated:
        return HttpResponse('estou logado')

    if request.method == "GET":
        return render(request, 'cadastro.html' )

    elif request.method == "POST":
        username = request.POST.get('usuario')
        senha = request.POST.get('senha')
        email = request.POST.get('email')
        confirmar_senha = request.POST.get('confirmar_senha')
        if not password_is_valid(request, senha, confirmar_senha):
            return redirect('/auth/cadastro')
        if User.objects.filter(email=email).exists():
            messages.add_message(request, constants.ERROR, 'Já existe usuario com esse email')
            return redirect('/auth/cadastro')
    try:
        usuario = User.objects.create_user(username=username, email=email, password=senha)
        usuario.save()
        return redirect('/auth/logar')
    except:
        pass
def logar(request):
    if request.user.is_authenticated:
        return HttpResponse('estou logado')

    if request.method == "GET":
        return render(request, 'login.html')

    elif request.method == "POST":
        username = request.POST.get('usuario')
        senha = request.POST.get('senha')
        usuario = auth.authenticate(username=username, password=senha)

    if not usuario:
        messages.add_message(request, constants.ERROR, 'Username ou senha inválidos')
        return redirect('/auth/logar')
    else:
        auth.login(request, usuario)
        return redirect('/auth/sair')

def sair(request):
    return HttpResponse('estou logado')