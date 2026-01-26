# memegenerator/_test_.py
import requests

# URL de la API de Imgflip para obtener memes
url = 'https://api.imgflip.com/get_memes'

# Hacemos la petición GET [cite: 106-108]
response = requests.get(url)

# Convertimos la respuesta a JSON [cite: 109]
response_json = response.json()

# Imprimimos para ver la estructura
print("Status:", response_json['success'])

# Vamos a ver el primer meme de la lista para entender cómo viene la info
first_meme = response_json['data']['memes'][0]
print("----------------")
print("Nombre:", first_meme['name'])
print("URL Imagen:", first_meme['url'])