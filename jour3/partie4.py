import requests
from bs4 import BeautifulSoup
import pandas as pd

# Exercice 1 : 

def get_one_book() -> dict:
    url = "http://books.toscrape.com/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    first_book = soup.find('article', class_='product_pod')
    title = first_book.h3.a['title']
    rating_class = first_book.p['class'][1]
    rating_map = {
        'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5
    }
    rating = rating_map.get(rating_class, 0)
    price = float(first_book.select('p.price_color')[0].text[1:])
    return {
        'title': title,
        'rating': rating,
        'price': price
    }

# Exercice 2 :

def get_one_book_complete() -> dict:
    base_url = "http://books.toscrape.com/"
    response = requests.get(base_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    first_book = soup.find('article', class_='product_pod')
    book_page_url = base_url + first_book.h3.a['href']
    response = requests.get(book_page_url)
    book_soup = BeautifulSoup(response.content, 'html.parser')
    title = first_book.h3.a['title']
    rating_class = first_book.p['class'][1]
    rating_map = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5}
    rating = rating_map.get(rating_class, 0)
    price = float(first_book.select('p.price_color')[0].text[1:])
    description = book_soup.select_one('meta[name="description"]')['content'].strip()
    return {
        'title': title,
        'rating': rating,
        'price': price,
        'description': description
    }

# Exercice 3 :

def get_page_books(url: str = None) -> list:
    if url is None:
        url = "http://books.toscrape.com/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    books = []
    for book in soup.find_all('article', class_='product_pod'):
        title = book.h3.a['title']
        rating_class = book.p['class'][1]
        rating_map = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5}
        rating = rating_map.get(rating_class, 0)
        price = float(book.select('p.price_color')[0].text[1:])
        description_url = book.h3.a['href']
        book_page_url = f"http://books.toscrape.com/catalogue/{description_url}"
        book_response = requests.get(book_page_url)
        book_soup = BeautifulSoup(book_response.content, 'html.parser')
        description = book_soup.select_one('meta[name="description"]')['content'].strip()
        books.append({
            'title': title,
            'rating': rating,
            'price': price,
            'description': description
        })
        
    return books
# Exercice 4 :

def get_page_range(start: int, end: int, url: str = "http://books.toscrape.com/") -> pd.DataFrame:
    all_books = []
    for page_num in range(start, end + 1):
        page_url = f"{url}catalogue/page-{page_num}.html"
        books = get_page_books(page_url)
        all_books.extend(books)
    return pd.DataFrame(all_books)

# Exercice 5 :

def get_category(category_url: str) -> pd.DataFrame:
    books = []
    while category_url:
        response = requests.get(category_url)
        soup = BeautifulSoup(response.content, 'html.parser')
        for book in soup.find_all('article', class_='product_pod'):
            title = book.h3.a['title']
            rating_class = book.p['class'][1]
            rating_map = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5}
            rating = rating_map.get(rating_class, 0)
            price = float(book.select('p.price_color')[0].text[1:])
            books.append({'title': title, 'rating': rating, 'price': price})
        next_page = soup.find('li', class_='next')
        if next_page:
            category_url = category_url.rsplit('/', 1)[0] + '/' + next_page.a['href']
        else:
            category_url = None
    return pd.DataFrame(books)
    

# Exercice 6 :

def get_all_categories(file: str) -> pd.DataFrame:
    base_url = "http://books.toscrape.com/"
    response = requests.get(base_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    category_links = soup.select("div.side_categories ul li ul li a")
    all_books = []
    for category_link in category_links:
        category_name = category_link.text.strip()
        category_url = base_url + category_link['href']
        category_df = get_category(category_url)
        if not category_df.empty:
            category_df['category'] = category_name
            all_books.append(category_df)
    if all_books:
        combined_df = pd.concat(all_books, ignore_index=True)
        combined_df.to_csv(file, index=False)
        return combined_df
    else:
        return pd.DataFrame()

# Exercice 7 :

def basic_statistics(df: pd.DataFrame) -> (float, float):
    avg_price = df['price'].mean()
    avg_rating = df['rating'].mean()
    return avg_price, avg_rating

def categories_statistics(df: pd.DataFrame) -> pd.DataFrame:
    stats = df.groupby('category').agg(
        nb_book=('title', 'size'),
        avg_price=('price', 'mean'),
        avg_rating=('rating', 'mean')
    ).reset_index()
    stats['avg_price'] = stats['avg_price'].round(2)
    stats['avg_rating'] = stats['avg_rating'].round(2)
    return stats

def price_distribution(df: pd.DataFrame) -> pd.DataFrame:
    bins = pd.interval_range(start=0, freq=10, end=df['price'].max() + 10)
    df['price_bin'] = pd.cut(df['price'], bins=bins)
    dist = df['price_bin'].value_counts().sort_index().reset_index()
    dist.columns = ['range', 'nb_books']
    dist['range'] = dist['range'].apply(lambda x: x.left)
    return dist