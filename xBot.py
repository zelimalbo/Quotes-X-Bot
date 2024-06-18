import requests
from bs4 import BeautifulSoup
import re
import random
import time

def get_random_quote():
    random_int = random.randint(0, 416)  # Random quote selection

    # Requesting URL
    response = requests.get('https://everydaypower.com/famous-movie-quotes/')
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
    else:
        print("Request failed")
        print(response.status_code)
        return None

    pattern = r"^\d+\. (.*)$"
    quote_list = []
    quote_items = soup.find('div', id='mvp-content-wrap')
    for quote_item in quote_items.find_all('p'):
        text = quote_item.text.strip()
        if re.match(pattern, text):
            match = re.search(pattern, text)
            quote = match.group(1)
            quote_list.append(quote)  # Adding quotes from URL onto list

    if quote_list:
        selected_quote = quote_list[random_int]  # Chosen quote to be printed
        return selected_quote
    return None

def print_quote():
    quote = get_random_quote()
    if quote:
        print(quote)

# Schedule the job to print the quote every 10 seconds
while True:
    print_quote()
    time.sleep(86400)  # Wait 10 seconds before printing the next quote
