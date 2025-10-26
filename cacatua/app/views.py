from django.shortcuts import render
from .models import Person
from .models import User

# Create your views here.

from .models import Person

def diversion(request):
    person_list = Person.objects.all()
    users = User.objects.all()
    return render(request, 'app/home.html', {'persons': person_list, 'users': users})

def divertido(request, slug):
    person = Person.objects.get(slug=slug)
    return render(request, 'app/person.html', {'person': person})
