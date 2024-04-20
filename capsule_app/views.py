from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from django.views import generic
from .forms import *
from django.contrib.auth.models import Group
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .decorators import allowed_users
from guardian.shortcuts import assign_perm
from guardian.decorators import permission_required_or_403

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
    
@login_required(login_url='login')
@allowed_users(allowed_roles=['creators'])
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
            user = creator.user
            capsule.save()
            return redirect('creator-detail', creator_id)
    
    context = {'form':form}

    return render(request, 'capsule_app/capsule_form.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['creators'])
@permission_required_or_403('change_capsule', (Capsule, 'pk', 'capsule_id'))
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

@login_required(login_url='login')
@allowed_users(allowed_roles=['creators'])
@permission_required_or_403('change_capsule', (Capsule, 'pk', 'capsule_id'))
def delete_capsule(request, capsule_id, creator_id):
    capsule = Capsule.objects.get(id=capsule_id)

    if request.method == 'POST':
        capsule.delete()

        return redirect('creator-detail', creator_id)
    
    return render(request, 'capsule_app/delete_capsule.html', {'capsule':capsule})

def view_capsule(request, capsule_id, creator_id):
    capsule = Capsule.objects.get(pk=capsule_id)
    return render(request, 'capsule_app/view_capsule.html', {'capsule':capsule})

@login_required(login_url='login')
@allowed_users(allowed_roles=['creators'])
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

def registerPage(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)

        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            group = Group.objects.get(name='creators')
            user.groups.add(group)
            creator = Creator.objects.create(user=user,)
            creator.save()

            messages.success(request, 'Account has been created for ' + username)
            return redirect('login')
        
    context = {'form':form}
    return render(request, 'registration/register.html', context)