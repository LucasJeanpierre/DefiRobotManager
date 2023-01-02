from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
    message = "Hello, world. You're at the stats index."
    return render(request, template_name='stats/index.html', context={'message': message})
