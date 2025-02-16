import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin
from duckduckgo_search import DDGS
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# List of locations to search for, including all 50 states of the US and all provinces of Canada
locations = [
    # U.S. States
    "alabama", "alaska", "arizona", "arkansas", "california", "colorado", "connecticut", "delaware",
    "florida", "georgia", "hawaii", "idaho", "illinois", "indiana", "iowa", "kansas", "kentucky",
    "louisiana", "maine", "maryland", "massachusetts", "michigan", "minnesota", "mississippi",
    "missouri", "montana", "nebraska", "nevada", "new hampshire", "new jersey", "new mexico",
    "new york", "north carolina", "north dakota", "ohio", "oklahoma", "oregon", "pennsylvania",
    "rhode island", "south carolina", "south dakota", "tennessee", "texas", "utah", "vermont",
    "virginia", "washington", "west virginia", "wisconsin", "wyoming", "district of columbia",
    
    # Canadian Provinces and Territories
    "alberta", "british columbia", "manitoba", "new brunswick", "newfoundland and labrador",
    "nova scotia", "ontario", "prince edward island", "quebec", "saskatchewan", "northwest territories",
    "nunavut", "yukon"
]    

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

def scrape_price_list(url, session, driver, location):
    try:
        driver.get(url)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Find all links on the page
        links = soup.find_all('a', href=True)

        for link in links:
            href = link['href']
            # Check if the link is a PDF
            if href.lower().endswith('.pdf'):
                # Construct full URL if necessary
                full_url = urljoin(url, href)
                download_file(full_url, url, session, location)
    except Exception as e:
        print(f"Failed to scrape {url}: {e}")

def download_file(file_url, page_url, session, location):
    try:
        response = session.get(file_url)
        response.raise_for_status()

        # Ensure the downloads directory exists
        download_dir = f'downloads/{location}'
        os.makedirs(download_dir, exist_ok=True)

        # Extract filename from URL and save in downloads directory
        filename = os.path.join(download_dir, file_url.split('/')[-1])
        with open(filename, 'wb') as file:
            file.write(response.content)
        print(f"Downloaded: {filename}")

        # Generate APA reference
        generate_apa_reference(page_url, filename, session)
    except requests.RequestException as e:
        print(f"Failed to download {file_url}: {e}")
    except FileNotFoundError as e:
        print(f"File not found error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred while downloading {file_url}: {e}")

def generate_apa_reference(page_url, filename, session):
    try:
        response = session.get(page_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract metadata
        title = soup.title.string if soup.title else "No title"
        author = soup.find('meta', attrs={'name': 'author'})
        author = author['content'] if author else "No author"
        date = "n.d."  # No date available

        # Format APA reference
        reference = f"{author}. ({date}). {title}. Retrieved from {page_url}\n"

        # Append to references file
        with open("references.txt", "a") as ref_file:
            ref_file.write(reference)
    except requests.RequestException as e:
        print(f"Failed to generate reference for {page_url}: {e}")
    except Exception as e:
        print(f"An unexpected error occurred while generating reference for {page_url}: {e}")

def main():
    # Set up Selenium WebDriver using webdriver-manager
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument(f"user-agent={USER_AGENT}")
    driver = webdriver.Chrome(options=chrome_options)

    # Create a session to persist cookies and headers
    session = requests.Session()
    session.headers.update({'User-Agent': USER_AGENT})

    for location in locations:
        query = f"funeral general price list {location}"
        urls = search_funeral_homes(query)
        for url in urls:
            print(f"Scraping {url}")
            scrape_price_list(url, session, driver, location)

    driver.quit()

if __name__ == "__main__":
    main()