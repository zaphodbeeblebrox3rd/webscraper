import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin
from duckduckgo_search import DDGS

# Define a User-Agent string to mimic a browser
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"

def search_funeral_homes(query, num_results=10):
    try:
        # Initialize the list to store URLs
        urls = []

        # Perform a search using DuckDuckGo
        with DDGS() as ddgs:
            for r in ddgs.text(query, max_results=num_results):
                urls.append(r['href'])
        
        return urls
    except Exception as e:
        print(f"Failed to retrieve search results: {e}")
        return []

def scrape_price_list(url):
    try:
        headers = {'User-Agent': USER_AGENT}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all links on the page
        links = soup.find_all('a', href=True)

        for link in links:
            href = link['href']
            if 'price-list' in href.lower() or 'gpl' in href.lower():
                # Construct full URL if necessary
                full_url = urljoin(url, href)
                download_file(full_url, url)
    except requests.RequestException as e:
        print(f"Failed to scrape {url}: {e}")

def download_file(file_url, page_url):
    try:
        headers = {'User-Agent': USER_AGENT}
        response = requests.get(file_url, headers=headers)
        response.raise_for_status()

        # Ensure the downloads directory exists
        download_dir = 'downloads'
        os.makedirs(download_dir, exist_ok=True)

        # Extract filename from URL and save in downloads directory
        filename = os.path.join(download_dir, file_url.split('/')[-1])
        with open(filename, 'wb') as file:
            file.write(response.content)
        print(f"Downloaded: {filename}")

        # Generate APA reference
        generate_apa_reference(page_url, filename)
    except requests.RequestException as e:
        print(f"Failed to download {file_url}: {e}")
    except FileNotFoundError as e:
        print(f"File not found error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred while downloading {file_url}: {e}")

def generate_apa_reference(page_url, filename):
    try:
        headers = {'User-Agent': USER_AGENT}
        response = requests.get(page_url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract metadata
        title = soup.title.string if soup.title else "No title"
        author = soup.find('meta', attrs={'name': 'author'})
        author = author['content'] if author else "No author"
        date = "n.d."  # No date available

        # Format APA reference
        reference = f"{author}. ({date}). {title}. Retrieved from {page_url}\n"

        # Write to references file
        with open("references.txt", "a") as ref_file:
            ref_file.write(reference)
    except requests.RequestException as e:
        print(f"Failed to generate reference for {page_url}: {e}")
    except Exception as e:
        print(f"An unexpected error occurred while generating reference for {page_url}: {e}")

def main():
    query = "funeral general price list canada"
    urls = search_funeral_homes(query)

    for url in urls:
        print(f"Scraping {url}")
        scrape_price_list(url)

if __name__ == "__main__":
    main()