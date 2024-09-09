import requests
import os
import csv

# Exercice 1 : 

def get_companies_with_name(name: str) -> list[dict]:
    try:
        url = "https://recherche-entreprises.api.gouv.fr/search"
        params = {
            "q": name,
            "per_page": 10
        }
        response = requests.get(url, params=params)
        print(url)
        response.raise_for_status()
        data = response.json()
        companies = []
        for company in data['results']:
            company_info = {
                "SIREN": company.get('siren'),
                "Nom": company.get('nom_raison_sociale'),
                "Date de création": company['siege'].get('date_creation')
            }
            companies.append(company_info)
        return companies
    except (requests.RequestException, ValueError, KeyError):
        return []
    
# Exercice 2 :

def get_all_companies_with_name(name: str) -> list[dict]:
    try:
        base_url = "https://recherche-entreprises.api.gouv.fr/search"
        params = {
            'q': name,
            'page': 1
        }
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()
        companies = []
        total_pages = data.get('total_pages', 1)
        for page in range(1, total_pages + 1):
            params['page'] = page
            response = requests.get(base_url, params=params)
            response.raise_for_status()
            data = response.json()
            for company in data.get('results', []):
                company_info = {
                    'siren': company.get('siren'),
                    'nom_entreprise': company.get('nom_complet'),
                    'date_creation': company['siege'].get('date_creation')
                }
                companies.append(company_info)
        return companies
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

# Exercice 3 :

def get_and_store_companies(filename: str, name: str):
    try:
        companies = get_all_companies_with_name(name)
        if not companies:
            return
        existing_sirens = set()
        if os.path.exists(filename):
            with open(filename, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    existing_sirens.add(row['siren'])
        new_companies = []
        for company in companies:
            if company['siren'] not in existing_sirens:
                new_companies.append(company)
        new_companies.sort(key=lambda x: x['siren'])
        file_exists = os.path.isfile(filename)
        with open(filename, mode='a' if file_exists else 'w', newline='', encoding='utf-8') as file:
            fieldnames = ['siren', 'nom_entreprise', 'date_creation']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            
            if not file_exists:
                writer.writeheader()
            
            for company in new_companies:
                writer.writerow(company)
        
    except Exception as e:
        print(f"An error occurred: {e}")
        return
