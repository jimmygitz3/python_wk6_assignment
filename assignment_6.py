import requests
import os
from urllib.parse import urlparse
from uuid import uuid4

def is_valid_image(response):
    content_type = response.headers.get('Content-Type', '')
    return content_type.startswith('image/')

def get_filename_from_url(url):
    parsed_url = urlparse(url)
    filename = os.path.basename(parsed_url.path)
    if not filename or '.' not in filename:
        filename = f"image_{uuid4().hex}.jpg"
    return filename

def fetch_and_save_image(url, saved_files):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        if not is_valid_image(response):
            print(f"✗ Skipped (Not an image): {url}")
            return

        filename = get_filename_from_url(url)
        filepath = os.path.join("Fetched_Images", filename)

        if filename in saved_files:
            print(f"✗ Skipped (Duplicate): {filename}")
            return

        with open(filepath, 'wb') as f:
            f.write(response.content)

        saved_files.add(filename)
        print(f"✓ Successfully fetched: {filename}")
        print(f"✓ Image saved to {filepath}")

    except requests.exceptions.RequestException as e:
        print(f"✗ Connection error for {url}: {e}")
    except Exception as e:
        print(f"✗ Unexpected error for {url}: {e}")

def main():
    print("Welcome to the Ubuntu Image Fetcher")
    print("A tool for mindfully collecting images from the web\n")

    urls = input("Enter image URLs separated by commas:\n").split(',')
    urls = [url.strip() for url in urls if url.strip()]

    os.makedirs("Fetched_Images", exist_ok=True)
    saved_files = set()

    for url in urls:
        fetch_and_save_image(url, saved_files)

    print("\nConnection strengthened. Community enriched.")

if __name__ == "__main__":
    main()