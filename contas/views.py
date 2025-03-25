from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group, Permission
from django.contrib import messages
from django.contrib.auth.forms import PasswordResetForm
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, RegisterForm

from contas.models import UserProfile
from forum.models import Resposta, Voto
from .forms import EditProfileForm

# ------------------------- Views Gerais -------------------------
def home(request):
    return render(request, 'home.html')

def explorar(request):
    return render(request, 'explorar.html')

# ------------------------- Autenticação -------------------------
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Login realizado com sucesso!')
                return redirect('contas:home')
            else:
                messages.error(request, 'Usuário ou senha inválidos.')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, 'Você saiu com sucesso.')
    return redirect('contas:login')

# ------------------------- Registro -------------------------
def assign_permissions_to_group(group):
    content_type = ContentType.objects.get_for_model(User)
    permissions = Permission.objects.filter(content_type=content_type)
    for perm in permissions:
        group.permissions.add(perm)

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            try:
                username = form.cleaned_data['username']
                email = form.cleaned_data['email']
                password1 = form.cleaned_data['password1']
                tipo_usuario = form.cleaned_data['tipo_usuario']
                cursos = form.cleaned_data['cursos']

                # Cria o usuário
                user = User.objects.create_user(username=username, email=email, password=password1)

                # Cria o perfil do usuário
                user_profile = UserProfile.objects.create(user=user, tipo_usuario=tipo_usuario)
                user_profile.cursos.set(cursos)  # Adiciona os cursos selecionados

                messages.success(request, 'Conta criada com sucesso! Faça login.')
                return redirect('contas:login')
            except Exception as e:
                messages.error(request, f'Ocorreu um erro: {e}')
        else:
            messages.error(request, 'Por favor, corrija os erros no formulário.')
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})

# ------------------------- Redefinição de Senha -------------------------
def password_reset_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            associated_users = User.objects.filter(email=email)
            if associated_users.exists():
                for user in associated_users:
                    subject = "Redefinição de senha"
                    email_template_name = "password_reset_email.html"
                    context = {
                        "email": user.email,
                        "domain": request.get_host(),
                        "site_name": "Seu Site",
                        "uid": user.id,
                        "token": "gerar_token",  # Implementar lógica real
                    }
                    email_content = render_to_string(email_template_name, context)
                    send_mail(subject, email_content, settings.DEFAULT_FROM_EMAIL, [user.email])
                messages.success(request, 'E-mail de redefinição de senha enviado.')
                return redirect('userapp:login')
            else:
                messages.error(request, 'Nenhum usuário encontrado com este e-mail.')
    return render(request, 'password_reset.html')

# ------------------------- Perfil do Usuário -------------------------

def profile_view(request):
    return render(request, 'profile.html')

@login_required
def edit_profile(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    if request.method == "POST":
        form = EditProfileForm(request.POST, request.FILES, user_profile=user_profile, instance=request.user)
        if form.is_valid():
            form.save(user_profile=user_profile)
            messages.success(request, "Perfil atualizado com sucesso!")
            return redirect('contas:profile')
    else:
        form = EditProfileForm(user_profile=user_profile, instance=request.user)
    return render(request, 'edit_profile.html', {'form': form})

@login_required
def delete_account(request):
    if request.method == "POST":
        password = request.POST.get('password')
        delete_actions = request.POST.get('delete_actions')
        user = request.user

        if not authenticate(username=user.username, password=password):
            messages.error(request, "Senha incorreta. Tente novamente.")
            return redirect('contas:delete_account')

        if delete_actions == 'yes':
            user.topico_set.all().delete()
            Resposta.objects.filter(author=user).delete()
            Voto.objects.filter(user=user).delete()
        
        user.delete()
        messages.success(request, "Sua conta foi excluída com sucesso!")
        return redirect('contas:login')
    return render(request, 'delete_account.html')
