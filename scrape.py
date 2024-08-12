import requests
from bs4 import BeautifulSoup
import json

# Function to scrape quotes from a page
def scrape_quotes(page_url):
    response = requests.get(page_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    quotes = []

    for quote in soup.find_all('div', class_='quote'):
        text = quote.find('span', class_='text').get_text()
        author = quote.find('small', class_='author').get_text()
        tags = [tag.get_text() for tag in quote.find_all('a', class_='tag')]
        quotes.append({
            'text': text,
            'author': author,
            'tags': tags
        })

    return quotes

# Scrape all pages
all_quotes = []
page = 1
base_url = 'https://quotes.toscrape.com/page/{}/'

while True:
    url = base_url.format(page)
    quotes = scrape_quotes(url)
    
    if not quotes:  # Stop if no quotes are found (end of pages)
        break
    
    all_quotes.extend(quotes)
    page += 1

# Save the scraped quotes to a JSON file
with open('output.json', 'w', encoding='utf-8') as f:
    json.dump(all_quotes, f, ensure_ascii=False, indent=4)

print(f"Scraped data saved to output.json")
