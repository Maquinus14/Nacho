from django.shortcuts import render
from .models import Person

def diversion(request):
    return render(request, 'app/app.html')

# Create your views here.

from .models import Person

def diversion(request):
    person_list = Person.objects.all()
    return render(request, 'home.html', {'persons': person_list})

def divertido(request, slug):
    person = Person.objects.get(slug=slug)
    return render(request, 'home.html', {'person': person})
