from django.shortcuts import render

def homepage(request):
    return render(request, 'hola.html')