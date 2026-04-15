"""
Web Scraping - Basic Examples
"""

import requests
from bs4 import BeautifulSoup
import time

def fetch_webpage(url):
    """Fetch a webpage and return its HTML content"""
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching webpage: {e}")
        return None

def extract_links(html_content):
    """Extract all links from HTML content"""
    soup = BeautifulSoup(html_content, 'html.parser')
    links = []
    for link in soup.find_all('a', href=True):
        links.append(link['href'])
    return links

def extract_text(html_content):
    """Extract text content from HTML"""
    soup = BeautifulSoup(html_content, 'html.parser')
    return soup.get_text()

def extract_images(html_content):
    """Extract all image URLs from HTML"""
    soup = BeautifulSoup(html_content, 'html.parser')
    images = []
    for img in soup.find_all('img', src=True):
        images.append(img['src'])
    return images

def get_page_title(html_content):
    """Extract the page title"""
    soup = BeautifulSoup(html_content, 'html.parser')
    title = soup.find('title')
    return title.text if title else "No title found"

def extract_meta_description(html_content):
    """Extract meta description from HTML"""
    soup = BeautifulSoup(html_content, 'html.parser')
    meta_desc = soup.find('meta', attrs={'name': 'description'})
    return meta_desc['content'] if meta_desc else "No meta description found"

def scrape_example_website():
    """Example: Scrape a sample website (example.com)"""
    url = "https://example.com"
    
    print(f"Scraping {url}...")
    html_content = fetch_webpage(url)
    
    if html_content:
        print(f"Page title: {get_page_title(html_content)}")
        print(f"Meta description: {extract_meta_description(html_content)}")
        print(f"Number of links: {len(extract_links(html_content))}")
        print(f"Number of images: {len(extract_images(html_content))}")
        
        # Print first few links
        links = extract_links(html_content)
        print("\nFirst 5 links:")
        for link in links[:5]:
            print(f"  - {link}")

def scrape_headers(html_content):
    """Extract all headers (h1-h6) from HTML"""
    soup = BeautifulSoup(html_content, 'html.parser')
    headers = {}
    for i in range(1, 7):
        headers[f'h{i}'] = [h.text.strip() for h in soup.find_all(f'h{i}')]
    return headers

def main():
    print("Web Scraping Examples\n")
    print("=" * 50)
    
    # Scrape example website
    scrape_example_website()
    
    print("\n" + "=" * 50)
    print("\nNote: For real web scraping projects:")
    print("1. Always check the website's robots.txt file")
    print("2. Respect rate limits and add delays between requests")
    print("3. Use proper user-agent headers")
    print("4. Consider using APIs when available")
    print("5. Be aware of legal and ethical considerations")

if __name__ == "__main__":
    main()