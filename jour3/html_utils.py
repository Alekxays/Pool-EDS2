import os


def url_to_filename(url):
    import hashlib

    # Use SHA-256 hashing
    hash_object = hashlib.sha256(url.encode())
    # Hexadecimal representation
    return hash_object.hexdigest()


def fetch_html(url: str) -> str:
    import requests

    from pathlib import Path

    # Convert URL to a safe filename
    url_slug = url_to_filename(url)
    filename = f"{url_slug}.html"
    filepath = os.path.join('html_cache', filename)

    f = Path(filepath)
    if f.exists():
        print("Loading HTML from the cache")
        return f.read_text()
    print("Fetching HTML from the website")
    # Make the request
    r = requests.get(url)
    r.raise_for_status()

    # Save the HTML content to a file
    os.makedirs('html_cache', exist_ok=True)  # Create cache directory if not exists
    f.write_text(r.text)
    return r.text
