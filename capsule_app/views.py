from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from django.views import generic
from .forms import *
from django.shortcuts import redirect

# Create your views here.

def index(request):
    return render(request, 'console_app/index.html')