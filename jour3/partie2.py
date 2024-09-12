from bs4 import BeautifulSoup
import re

# Exercice 0 :

def create_bs_obj(file: str) -> BeautifulSoup:
    with open(file, 'r', encoding='utf-8') as html_file:
        return BeautifulSoup(html_file.read(), 'html.parser')
    
# Exercice 1 :

def find_title(file: str) -> str:
    soup = create_bs_obj(file)
    title_tag = soup.title
    return str(title_tag) if title_tag else ''

# Exercice 2 :

def find_paragraphs(file: str) -> list[str]:
    soup = create_bs_obj(file)
    paragraphs = soup.find_all('p')
    return [str(p) for p in paragraphs]

# Exercice 3 :

def find_links(file: str) -> list[str]:
    soup = create_bs_obj(file)
    links = soup.find_all('a', href=True)
    return [link['href'] for link in links]

# Exercice 4 :

def find_elements_with_css_class(file: str, class_name: str) -> list[str]:
    soup = create_bs_obj(file)
    elements = soup.find_all(class_=class_name)
    return [str(element) for element in elements]

# Exercice 5 :

def find_headers(file: str) -> list[str]:
    soup = create_bs_obj(file)
    headers = soup.find_all(re.compile(r'^h[1-6]$'))
    return [header.get_text() for header in headers]

# Exercice 6 :

def extract_table(file: str) -> list[dict]:
    soup = create_bs_obj(file)
    table = soup.find('table')
    data = []
    for row in table.find_all('tr')[1:]:
        cols = row.find_all('td')
        if len(cols) == 3:
            fruit = {
                'name': cols[0].get_text().strip(),
                'color': cols[1].get_text().strip(),
                'price': float(cols[2].get_text().strip().replace('$', '').replace(',', ''))
            }
            data.append(fruit)
    return data

    