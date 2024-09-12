import requests

# Exercice 1 :

def get_request(url: str) -> (int, any):
    response = requests.get(url)
    return response.status_code, response.json()

# Exercice 2 :

def get_countries_info(country_codes: list, info: list) -> (int, str):
    url = 'https://restcountries.com/v3.1/alpha'
    params = {
        'codes': ','.join(country_codes),
        'fields': ','.join(info)
    }
    response = requests.get(url, params=params)
    return response.status_code, response.json()

# Exercice 3 :

def handle_request_status(url: str) -> int | str:
    try:
        response = requests.post(url)
        response.raise_for_status()
        return response.status_code
    except requests.exceptions.HTTPError as http_err:
        return {http_err}
    except requests.exceptions.RequestException as req_err:
        return {req_err}
    except Exception as err:
        return {err}

# Exercice 4 :

def send_query_parameters(params: dict) -> dict:
    url = 'https://httpbin.org/response-headers'
    response = requests.get(url, params=params)
    return response.json()

def send_headers(headers: dict) -> str:
    url = 'https://httpbin.org/headers'
    response = requests.get(url, headers=headers)
    return response.json().get('headers', '')