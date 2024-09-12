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
            img_filename = os.path.basename(img_src.split('?')[0])
            valid_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.svg')
            if not img_filename.lower().endswith(valid_extensions):
                continue
            if img_src.startswith('//'):
                img_url = 'https:' + img_src
            elif img_src.startswith('http'):
                img_url = img_src
            else:
                img_url = f"https:{img_src}" if img_src.startswith('/w/') else f"{base_url}{img_src}"
            try:
                img_response = requests.get(img_url, headers={'User-Agent': 'Mozilla/5.0'})
                img_response.raise_for_status()
                img_filepath = os.path.join(folder, img_filename)
                with open(img_filepath, 'wb') as f:
                    f.write(img_response.content)
                downloaded_count += 1
                print(f"Image téléchargée : {img_filepath}")
                if max is not None and downloaded_count >= max:
                    break
                time.sleep(1)
            except Exception as e:
                print(f"Échec du téléchargement de {img_url} : {e}")


# Exercice 3 :

def recursive_navigation(url: str, nb: int) -> list[str]:
    visited_links = []
    headers = {'User-Agent': 'Mozilla/5.0'}
    while nb > 0:
        visited_links.append(url)
        html = fetch_html(url)
        soup = BeautifulSoup(html, 'html.parser')
        content_div = soup.find(id='mw-content-text')
        if not content_div:
            print(f"Contenu principal introuvable à l'URL : {url}")
            break
        paragraphs = content_div.find_all('p', recursive=False)
        if not paragraphs:
            print(f"Aucun paragraphe trouvé dans le contenu principal à l'URL : {url}")
            break

        link_found = False
        for paragraph in paragraphs:
            for element in paragraph.find_all(['span', 'small', 'sup']):
                element.decompose()
            for link in paragraph.find_all('a', href=True):
                href = link['href']
                if href.startswith('/wiki/') and not ':' in href and not href.startswith('/wiki/Wikip%C3%A9dia'):
                    next_url = f"https://fr.wikipedia.org{href}"
                    if next_url not in visited_links:
                        url = next_url
                        link_found = True
                        break
            if link_found:
                break

        if not link_found:
            print(f"Aucun lien valide trouvé sur la page : {url}")
            break

        nb -= 1

    return visited_links
