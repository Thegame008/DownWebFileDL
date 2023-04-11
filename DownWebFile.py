import os
import requests
from bs4 import BeautifulSoup
import re
import argparse

parser = argparse.ArgumentParser(description='Scraping utility to download files from a URL with a specific extension')
parser.add_argument('url', type=str, help='The URL of the page to scrape')
parser.add_argument('-ext', type=str, nargs='+', help='The extension(s) of the files to download')

args = parser.parse_args()

# URL de la página web
url = args.url

# Descargar la página web
print(f"Descargando página web: {url}")
page = requests.get(url)

# Analizar la página web con BeautifulSoup
print("Analizando página web...")
soup = BeautifulSoup(page.content, 'html.parser')

# Buscar todos los enlaces a archivos con la(s) extensión(es) especificada(s)
print("Buscando archivos...")
if args.ext:
    ext_pattern = r'\.(' + '|'.join(args.ext) + ')$'
    file_links = soup.find_all('a', href=re.compile(ext_pattern))
else:
    file_links = soup.find_all('a', href=True)

# Descargar cada archivo
for link in file_links:
    file_url = url + link['href']
    file_name = os.path.basename(file_url)
    print(f"Descargando archivo: {file_name}...")
    response = requests.get(file_url)
    with open(file_name, 'wb') as f:
        f.write(response.content)
        print(f"Archivo guardado: {file_name}")

print("Descarga completada.")
