from django.shortcuts import render, redirect, get_object_or_404
from .models import Sala, Categoria, Topico, Resposta, Voto, Tag
from .forms import SalaForm, CategoriaForm, TopicoForm, RespostaForm, TagForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.db.models import Q

# Função para verificar acesso à Sala
def check_access_to_sala(request, sala):
    if not sala.publico:
        user_profile = request.user.userprofile

        # Verifica o tipo de usuário
        if sala.tipo_usuario_permitido:  # Se o campo não estiver vazio
            if user_profile.tipo_usuario != sala.tipo_usuario_permitido:
                return HttpResponseForbidden("Você não tem permissão para acessar esta sala.")

        # Verifica os cursos permitidos
        if sala.cursos_permitidos.exists() and not user_profile.cursos.filter(id__in=sala.cursos_permitidos.values_list('id', flat=True)).exists():
            return HttpResponseForbidden("Você não tem permissão para acessar esta sala.")

    return None

# Listar Salas com filtro de acesso
def sala_list(request):
    salas = []  # Inicializa a lista vazia

    if request.user.is_authenticated:
        user_profile = request.user.userprofile

        # Filtra Salas públicas
        salas_publicas = Sala.objects.filter(publico=True)

        # Filtra Salas onde o usuário tem permissão com base nos cursos e tipo de usuário
        salas_com_permissao = Sala.objects.filter(
            Q(tipo_usuario_permitido__isnull=True) |  # Salas sem restrição de tipo de usuário
            Q(tipo_usuario_permitido='') |  # Salas com tipo de usuário indefinido
            Q(tipo_usuario_permitido=user_profile.tipo_usuario)  # Salas que permitem o tipo de usuário
        ).filter(
            Q(cursos_permitidos__isnull=True) |  # Salas sem restrição de cursos
            Q(cursos_permitidos__in=user_profile.cursos.all())  # Salas que permitem os cursos do usuário
        ).distinct()

        # Combine as duas listas manualmente
        salas = list(salas_publicas) + list(salas_com_permissao)

    else:
        # Apenas salas públicas para usuários não autenticados
        salas = list(Sala.objects.filter(publico=True))

    return render(request, 'salas/sala_list.html', {'salas': salas})

# Criar nova Sala (apenas para administradores)
@login_required
@user_passes_test(lambda u: u.is_authenticated and (u.is_superuser or u.groups.filter(name="Moderadores").exists()))
def create_sala(request):
    if request.method == 'POST':
        form = SalaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('forum:sala_list')
    else:
        form = SalaForm()
    return render(request, 'salas/create_sala.html', {'form': form})

# Editar Sala (apenas para administradores)
@login_required
@user_passes_test(lambda u: u.is_authenticated and (u.is_superuser or u.groups.filter(name="Moderadores").exists()))
def edit_sala(request, sala_id):
    sala = get_object_or_404(Sala, id=sala_id)
    access_error = check_access_to_sala(request, sala)
    if access_error:
        return access_error

    if request.method == 'POST':
        form = SalaForm(request.POST, instance=sala)
        if form.is_valid():
            form.save()
            return redirect('forum:sala_list')
    else:
        form = SalaForm(instance=sala)
    return render(request, 'salas/edit_sala.html', {'form': form})

# Excluir Sala (apenas para administradores)
@login_required
@user_passes_test(lambda u: u.is_authenticated and (u.is_superuser or u.groups.filter(name="Moderadores").exists()))
def delete_sala(request, sala_id):
    sala = get_object_or_404(Sala, id=sala_id)
    access_error = check_access_to_sala(request, sala)
    if access_error:
        return access_error

    sala.delete()
    return redirect('forum:sala_list')

# Views para Categoria
def categoria_list(request, sala_id):
    sala = get_object_or_404(Sala, id=sala_id)
    categorias = Categoria.objects.filter(sala=sala)
    return render(request, 'categorias/categoria_list.html', {'sala': sala, 'categorias': categorias})

@login_required
@user_passes_test(lambda u: u.is_authenticated and (u.is_superuser or u.groups.filter(name="Moderadores").exists()))
def create_categoria(request, sala_id):
    sala = get_object_or_404(Sala, id=sala_id)
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            categoria = form.save(commit=False)
            categoria.sala = sala
            categoria.save()
            return redirect('forum:categoria_list', sala_id=sala.id)
    else:
        form = CategoriaForm()
    return render(request, 'categorias/create_categoria.html', {'form': form, 'sala': sala})

@login_required
@user_passes_test(lambda u: u.is_authenticated and (u.is_superuser or u.groups.filter(name="Moderadores").exists()))
def edit_categoria(request, sala_id, categoria_id):
    sala = get_object_or_404(Sala, pk=sala_id)
    categoria = get_object_or_404(Categoria, pk=categoria_id)

    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            return redirect('forum:categoria_list', sala_id=sala.id)
    else:
        form = CategoriaForm(instance=categoria)

    return render(request, 'categorias/edit_categoria.html', {'form': form, 'sala': sala, 'categoria': categoria})

@login_required
@user_passes_test(lambda u: u.is_authenticated and (u.is_superuser or u.groups.filter(name="Moderadores").exists()))
def delete_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id)
    sala_id = categoria.sala.id
    categoria.delete()
    return redirect('categoria_list', sala_id=sala_id)

# Views para Tópico
def topico_list(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id)
    query = request.GET.get("q")  # Obtém o termo digitado na pesquisa
    topicos = Topico.objects.filter(categoria=categoria).order_by('-created_at')

    if query:
        topicos = topicos.filter(Q(title__icontains=query) | Q(content__icontains=query))

    tags = Tag.objects.filter(topicos__categoria=categoria).distinct()

    return render(request, 'topicos/topico_list.html', {'categoria': categoria, 'topicos': topicos, 'tags': tags, 'query': query})

def topico_detail(request, topico_id):
    topico = get_object_or_404(Topico, id=topico_id)
    respostas = topico.respostas.all().order_by('-votos', '-created_at')
    tags = topico.tags.all()
    return render(request, 'topicos/topico_detail.html', {
        'topico': topico,
        'respostas': respostas,
        'tags': tags,
    })

@login_required
def create_topico(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id)
    if request.method == 'POST':
        form = TopicoForm(request.POST)
        if form.is_valid():
            topico = form.save(commit=False)
            topico.categoria = categoria
            topico.author = request.user
            topico.save()
            topico.tags.set(form.cleaned_data['tags'])
            return redirect('forum:topico_list', categoria_id=categoria.id)
    else:
        form = TopicoForm()
    return render(request, 'topicos/create_topico.html', {'form': form, 'categoria': categoria})

@login_required
def edit_topico(request, topico_id):
    topico = get_object_or_404(Topico, id=topico_id)
    if request.user != topico.author:
        return redirect('forum:topico_detail', topico_id=topico.id)

    if request.method == 'POST':
        form = TopicoForm(request.POST, instance=topico)
        if form.is_valid():
            topico = form.save(commit=False)
            topico.save()
            topico.tags.set(form.cleaned_data['tags'])
            return redirect('forum:topico_detail', topico_id=topico.id)
    else:
        form = TopicoForm(instance=topico)

    return render(request, 'topicos/edit_topico.html', {'form': form, 'topico': topico})

@login_required
def delete_topico(request, topico_id):
    topico = get_object_or_404(Topico, id=topico_id)
    if request.user != topico.author:
        return redirect('forum:topico_detail', topico_id=topico.id)
    categoria_id = topico.categoria.id
    topico.delete()
    return redirect('forum:topico_list', categoria_id=categoria_id)

# Views para Resposta
@login_required
def add_resposta(request, topico_id):
    topico = get_object_or_404(Topico, id=topico_id)
    if request.method == 'POST':
        form = RespostaForm(request.POST)
        if form.is_valid():
            resposta = form.save(commit=False)
            resposta.topico = topico
            resposta.author = request.user
            resposta.save()
            return redirect('forum:topico_detail', topico_id=topico.id)
    else:
        form = RespostaForm()
    return render(request, 'respostas/add_resposta.html', {'form': form, 'topico': topico})

@login_required
def edit_resposta(request, resposta_id):
    resposta = get_object_or_404(Resposta, id=resposta_id)
    if request.user != resposta.author:
        return redirect('forum:topico_detail', topico_id=resposta.topico.id)

    if request.method == 'POST':
        form = RespostaForm(request.POST, instance=resposta)
        if form.is_valid():
            form.save()
            return redirect('forum:topico_detail', topico_id=resposta.topico.id)
    else:
        form = RespostaForm(instance=resposta)
    return render(request, 'respostas/edit_resposta.html', {'form': form, 'resposta': resposta})

@login_required
def voto_resposta(request, resposta_id):
    resposta = get_object_or_404(Resposta, id=resposta_id)

    try:
        voto = Voto.objects.get(user=request.user, resposta=resposta)
        voto.delete()
        resposta.votos -= 1
    except Voto.DoesNotExist:
        Voto.objects.create(user=request.user, resposta=resposta)
        resposta.votos += 1

    resposta.save()
    return redirect('forum:topico_detail', topico_id=resposta.topico.id)

@login_required
def delete_resposta(request, resposta_id):
    resposta = get_object_or_404(Resposta, id=resposta_id)
    topico_id = resposta.topico.id
    if request.user != resposta.author:
        return redirect('forum:topico_detail', topico_id=topico_id)
    resposta.delete()
    return redirect('forum:topico_detail', topico_id=topico_id)

# Views para Tag
@login_required
@user_passes_test(lambda u: u.is_authenticated and (u.is_superuser or u.groups.filter(name="Moderadores").exists()))
def create_tag(request):
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('forum:tag_list')
    else:
        form = TagForm()
    return render(request, 'tags/create_tag.html', {'form': form})

@login_required
@user_passes_test(lambda u: u.is_authenticated and (u.is_superuser or u.groups.filter(name="Moderadores").exists()))
def delete_tag(request, tag_id):
    tag = get_object_or_404(Tag, id=tag_id)
    if request.method == 'POST':
        tag.delete()
        return redirect('forum:tag_list')
    return render(request, 'tags/confirm_delete.html', {'tag': tag})

def tag_list(request):
    tags = Tag.objects.all()
    return render(request, 'tags/tag_list.html', {'tags': tags})

def topicos_by_tag(request, tag_id):
    tag = get_object_or_404(Tag, id=tag_id)
    topicos = tag.topicos.all()
    return render(request, 'tags/topics_by_tag.html', {'tag': tag, 'topicos': topicos})


#-------------------------------------------------------

from django.http import JsonResponse

def assetlinks(request):
    data = [{
        "relation": ["delegate_permission/common.handle_all_urls"],
        "target": {
            "namespace": "android_app",
            "package_name": "com.onrender.curvilinea_egressos.twa",
            "sha256_cert_fingerprints": ["82:32:E6:AB:F0:54:26:06:73:6E:C7:EB:80:9E:E9:B5:B5:48:CA:31:37:3C:1E:B1:6A:32:52:AB:53:D2:C2:A1"]
        }
    }]
    return JsonResponse(data, safe=False)


#-------------------------------------------------------

from django.shortcuts import render, redirect
from .models import Notificacao

def listar_notificacoes(request):
    notificacoes = request.user.notificacoes.all()  # Pega as notificações do usuário
    return render(request, 'notificacoes.html', {'notificacoes': notificacoes})

def marcar_como_lida(request, notificacao_id):
    notificacao = Notificacao.objects.get(id=notificacao_id, user=request.user)
    notificacao.lida = True
    notificacao.save()
    return redirect('forum:listar_notificacoes')

#-------------------------------------------------------

def sobre(request):
    return render(request, 'sobre.html')