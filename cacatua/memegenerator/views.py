# Create your views here.

from django.shortcuts import render
import requests

def index(request):
    # Hacemos la petición a la API
    url = 'https://api.imgflip.com/get_memes'
    response = requests.get(url)
    data = response.json()
    
    # Extraemos la lista de memes. 
    # La API devuelve: { 'success': True, 'data': { 'memes': [...] } }
    memes = data['data']['memes']
    
    # Pasamos la lista a la plantilla
    return render(request, 'memegenerator/index.html', {'memes': memes})