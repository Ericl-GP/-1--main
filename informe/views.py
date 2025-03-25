# views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Info, Banner
from .forms import InfoForm, BannerForm

# Informes page view
def informes(request):
    banners = Banner.objects.all()
    infos = Info.objects.all()
    return render(request, 'informes.html', {'banners': banners, 'infos': infos})


#------------------------------------------------------------
# Info views
def info_list(request):
    infos = Info.objects.all().order_by('-created_at')
    return render(request, 'infos/info_list.html', {'infos': infos})

def info_create(request):
    if request.method == "POST":
        form = InfoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('informes')
    else:
        form = InfoForm()
    return render(request, 'infos/info_form.html', {'form': form})

def info_detail(request, info_id):
    info = get_object_or_404(Info, id=info_id)
    return render(request, 'infos/info_detail.html', {'info': info})

def info_update(request, info_id):
    info = get_object_or_404(Info, id=info_id)
    if request.method == "POST":
        form = InfoForm(request.POST, instance=info)
        if form.is_valid():
            form.save()
            return redirect('informes')
    else:
        form = InfoForm(instance=info)
    return render(request, 'infos/info_form.html', {'form': form})

def info_delete(request, info_id):
    info = get_object_or_404(Info, id=info_id)
    if request.method == "POST":
        info.delete()
        return redirect('informes')
    return render(request, 'infos/info_confirm_delete.html', {'info': info})

#------------------------------------------------------------
# Banner views
def banner_list(request):
    banners = Banner.objects.all()
    return render(request, 'banners/banner_list.html', {'banners': banners})

def banner_create(request):
    if request.method == "POST":
        form = BannerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('informes')
    else:
        form = BannerForm()
    return render(request, 'banners/banner_form.html', {'form': form})

def banner_update(request, pk):
    banner = get_object_or_404(Banner, pk=pk)
    if request.method == "POST":
        form = BannerForm(request.POST, request.FILES, instance=banner)
        if form.is_valid():
            form.save()
            return redirect('informes')
    else:
        form = BannerForm(instance=banner)
    return render(request, 'banners/banner_form.html', {'form': form})

def banner_delete(request, pk):
    banner = get_object_or_404(Banner, pk=pk)
    if request.method == "POST":
        banner.delete()
        return redirect('informes')
    return render(request, 'banners/banner_confirm_delete.html', {'banner': banner})
