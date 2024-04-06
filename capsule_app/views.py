from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from django.views import generic
from .forms import *
from django.shortcuts import redirect

# Create your views here.

def index(request):
    creator_primary_capsules = Capsule.objects.all().filter(is_primary=True)
    return render(request, 'capsule_app/index.html', {'creator_primary_capsules':creator_primary_capsules})

class CapsuleDetailView(generic.DetailView):
    model= Capsule

class CreatorListView(generic.ListView):
    model = Creator

class CreatorDetailView(generic.DetailView):
    model = Creator

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['capsules'] = Capsule.objects.filter(creator=self.kwargs.get(self.pk_url_kwarg))
        return context
    
def create_capsule(request, creator_id):
    form = CapsuleForm()
    creator = Creator.objects.get(pk=creator_id)

    if request.method == 'POST':
        capsule_data = request.POST.copy()
        capsule_data['creator_id'] = creator_id
        form = CapsuleForm(capsule_data)

        if form.is_valid():
            capsule = form.save(commit=False)
            capsule.creator = creator
            capsule.save()
            return redirect('creator-detail', creator_id)
    
    context = {'form':form}

    return render(request, 'capsule_app/capsule_form.html', context)

def update_capsule(request, capsule_id, creator_id):
    
    capsule = Capsule.objects.get(id=capsule_id)
    form = CapsuleForm(instance=capsule)

    if request.method == 'POST':
        capsule_data = request.POST.copy()
        capsule_data['creator_id'] = creator_id
        form = CapsuleForm(request.POST, instance=capsule)

        if form.is_valid():
            form.save()
            return redirect('creator-detail', creator_id)
    
    context = {'form':form}

    return render(request, 'capsule_app/capsule_form.html', context)

def delete_capsule(request, capsule_id, creator_id):
    capsule = Capsule.objects.get(id=capsule_id)

    if request.method == 'POST':
        capsule.delete()

        return redirect('creator-detail', creator_id)
    
    return render(request, 'capsule_app/delete_capsule.html', {'capsule':capsule})

def view_capsule(request, capsule_id, creator_id):
    capsule = Capsule.objects.get(pk=capsule_id)
    return render(request, 'capsule_app/view_capsule.html', {'capsule':capsule})

def update_creator(request, creator_id):
    creator = Creator.objects.get(id=creator_id)
    form = CreatorForm(instance=creator)

    if request.method == 'POST':
        form = CreatorForm(request.POST, instance=creator)

        if form.is_valid():
            form.save()
            return redirect('creator-detail', creator_id)
    
    context = {'form':form}

    return render(request, 'capsule_app/update_creator.html', context)