from django.shortcuts import render
from .models import Person

# Create your views here.

from .models import Person

def diversion(request):
    person_list = Person.objects.all()
    return render(request, 'app/home.html', {'persons': person_list})

def divertido(request, slug):
    person = Person.objects.get(slug=slug)
    return render(request, 'app/person.html', {'person': person})
