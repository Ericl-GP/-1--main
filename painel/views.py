from django.shortcuts import render
from django.contrib.auth.models import User
from forum.models import Curso, Sala, Categoria, Topico, Resposta, Voto  
from painel.models import GoogleForm

from django.shortcuts import render
from django.contrib.auth.models import User
from forum.models import Sala, Categoria, Topico, Resposta, Voto  
from painel.models import GoogleForm
from contas.models import UserProfile

def dashboard_view(request):
    # Contadores gerais de usuários
    total_users = User.objects.count()
    total_ingressos = UserProfile.objects.filter(tipo_usuario="ingresso").count()
    total_egressos = UserProfile.objects.filter(tipo_usuario="egresso").count()

    # Contagem de usuários por curso
    cursos_data = []
    cursos = Curso.objects.all()
    for curso in cursos:
        total_usuarios = UserProfile.objects.filter(cursos=curso).count()
        total_ingressos = UserProfile.objects.filter(cursos=curso, tipo_usuario="ingresso").count()
        total_egressos = UserProfile.objects.filter(cursos=curso, tipo_usuario="egresso").count()

        cursos_data.append({
            'curso': curso.nome,  # Nome do curso
            'total_usuarios': total_usuarios,
            'total_ingressos': total_ingressos,
            'total_egressos': total_egressos,
        })

    # Dados das Salas, Categorias, Tópicos, Respostas e Votos
    salas_data = []
    salas = Sala.objects.all()
    for sala in salas:  
        total_categorias = sala.categorias.count()  
        total_topicos = Topico.objects.filter(categoria__sala=sala).count()  
        total_respostas = Resposta.objects.filter(topico__categoria__sala=sala).count()  
        total_votos = Voto.objects.filter(resposta__topico__categoria__sala=sala).count()  

        salas_data.append({
            'sala': sala.name,  
            'total_categorias': total_categorias,  
            'total_topicos': total_topicos,
            'total_respostas': total_respostas,
            'total_votos': total_votos
        })

    # Contador de formulários
    total_formularios = GoogleForm.objects.count()

    context = {
        'total_users': total_users,
        'total_ingressos': total_ingressos,
        'total_egressos': total_egressos,
        'cursos_data': cursos_data,  # Informações sobre cursos e usuários
        'salas_data': salas_data,
        'total_formularios': total_formularios,
    }
    return render(request, 'dashboard.html', context)




#-------------------------------------------------------------------------
from django.shortcuts import render, get_object_or_404, redirect
from .models import GoogleForm
from .forms import GoogleFormForm
from django.contrib.auth.decorators import login_required

# Listagem de Formulários com filtro de pesquisa
def form_list(request):
    search_query = request.GET.get('search', '')  # Obtém o valor da pesquisa
    if search_query:
        # Se houver pesquisa, filtra os formulários pelo título ou descrição
        forms = GoogleForm.objects.filter(titulo__icontains=search_query) | GoogleForm.objects.filter(descricao__icontains=search_query)
    else:
        # Caso contrário, exibe todos os formulários
        forms = GoogleForm.objects.all()
    
    return render(request, 'form_list.html', {'forms': forms, 'search_query': search_query})

# Detalhes do Formulário
def form_detail(request, form_id):
    form = get_object_or_404(GoogleForm, id=form_id)
    return render(request, 'form_detail.html', {'form': form})

# Criação de Formulários
@login_required
def form_create(request):
    if request.method == "POST":
        form = GoogleFormForm(request.POST)
        if form.is_valid():
            google_form = form.save(commit=False)  # Não salva imediatamente
            google_form.author = request.user  # Atribui o usuário logado como autor
            google_form.save()  # Agora salva com o autor atribuído
            return redirect('formulario_lista')  # Redireciona após criação
    else:
        form = GoogleFormForm()  # Exibe o formulário em branco

    return render(request, 'form_form.html', {'form': form})

# Atualização de Formulários
@login_required
def form_update(request, form_id):
    form = get_object_or_404(GoogleForm, id=form_id)
    if request.method == "POST":
        form = GoogleFormForm(request.POST, instance=form)
        if form.is_valid():
            form.save()
            return redirect('formulario_lista')  # Redireciona após atualização
    else:
        form = GoogleFormForm(instance=form)  # Carrega o formulário existente para edição

    return render(request, 'form_form.html', {'form': form})

# Deletar Formulários
@login_required
def form_delete(request, form_id):
    form = get_object_or_404(GoogleForm, id=form_id)
    if request.method == 'POST':
        form.delete()  # Deleta o formulário
        return redirect('formulario_lista')  # Redireciona para a lista de formulários
    return render(request, 'form_confirm_delete.html', {'form': form})
