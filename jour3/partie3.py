import requests
from bs4 import BeautifulSoup
from html_utils import fetch_html
import os
import time

# Exercice 1 :

def find_links_in_paragraphs(url: str) -> list[str]:
    try:
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception(f"Erreur de requête, code de statut: {response.status_code}")
        page_content = response.content
        soup = BeautifulSoup(page_content, 'html.parser')
        paragraphs = soup.find_all('p')
        links = []
        for p in paragraphs:
            a_tags = p.find_all('a', href=True)
            for a in a_tags:
                links.append(a['href'])
        return links
    except requests.RequestException as e:
        raise Exception(f"Erreur lors de la requête GET: {e}")

# Exercice 2 :

def download_images(url: str, folder: str, max: int | None = None):
    if not os.path.exists(folder):
        os.makedirs(folder)
    html = fetch_html(url)
    soup = BeautifulSoup(html, 'html.parser')
    img_tags = soup.find_all('img')
    base_url = 'https://upload.wikimedia.org'
    downloaded_count = 0

    for img in img_tags:
        img_src = img.get('src')
        if img_src and not img_src.startswith('/static/'):
            if img_src.startswith('//'):
                img_url = 'https:' + img_src
            elif img_src.startswith('http'):
                img_url = img_src
            else:
                img_url = f"{base_url}{img_src}"
            try:
                img_response = requests.get(img_url, headers={'User-Agent': 'Mozilla/5.0'})
                img_response.raise_for_status()
                img_filename = os.path.join(folder, os.path.basename(img_url))
                with open(img_filename, 'wb') as f:
                    f.write(img_response.content)
                downloaded_count += 1
                print(f"Image téléchargée : {img_filename}")
                if max is not None and downloaded_count >= max:
                    break
                time.sleep(1)
            except Exception as e:
                print(f"Échec du téléchargement de {img_url} : {e}")

# Exercice 3 :

def recursive_navigation(url: str, nb: int) -> list[str]:
    visited_links = []
    
    while nb > 0:
        visited_links.append(url)
        html = fetch_html(url)
        soup = BeautifulSoup(html, 'html.parser')
        paragraphs = soup.find_all('p')
        link_found = False
        
        for paragraph in paragraphs:
            links = paragraph.find_all('a', href=True)
            wiki_links = [a['href'] for a in links if a['href'].startswith('/wiki')]
            if len(wiki_links) >= nb:
                next_link = wiki_links[nb - 1]
                url = f"https://fr.wikipedia.org{next_link}"
                link_found = True
                break
        
        if not link_found:
            print(f"Aucun lien trouvé pour {url} avec nb = {nb}")
            break
        
        nb -= 1

    return visited_links