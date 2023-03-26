import requests
from bs4 import BeautifulSoup
from flask import Flask, jsonify
import schedule
import time

app = Flask(__name__)

def clean_price(price):
    return int(price.replace('$', '').replace('.', ''))

def get_clean_price(product, title):
    try:
        price = clean_price(product.find('li', title=title).text)
    except:
        price = -1
    return price

url_base = 'https://simple.ripley.cl/deporte-y-aventura/zapatillas/todo-zapatillas?facet%5B0%5D=G%C3%A9nero%3AHombre&facet%5B1%5D=Marca%3AADIDAS&facet%5B2%5D=Marca%3ANIKE&facet%5B3%5D=Marca%3APUMA&facet%5B4%5D=Talla%3A39.5&facet%5B5%5D=Talla%3A40&facet%5B6%5D=Talla%3A40.5&facet%5B7%5D=Talla%3A41&facet%5B8%5D=Talla%3A41.5&orderBy=price_asc&s=mdco&source=search&term=apatillas&page='
agent = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'}

def scrape():
    # Get the web page to scrape
    data = []

    try:
        for pagina in range(1, 6):
            page = requests.get(url_base+str(pagina), headers=agent)
            soup = BeautifulSoup(page.content, 'html.parser')
            products = soup.find_all('div', class_='catalog-product-details')
            for product in products:
                # Get name
                name = product.find('div', class_='catalog-product-details__name').text
                # Get prices
                normal_price = get_clean_price(product, 'Precio Normal')
                internet_price = get_clean_price(product, 'Precio Internet')
                ripley_price = get_clean_price(product, 'Precio Ripley')
                color = product.find('div', class_='catalog-colors-option-outer').get('title')
                data.append({'name': name, 'normal_price': normal_price, 'internet_price': internet_price, 'ripley_price': ripley_price, 'color': color})
    except:
        pass

    # Return the data as a JSON response
    print(data)
    return jsonify(data)

@app.route('/crawl')
def crawl():
    return scrape()

# Schedule the scraping task to run every 30 minutes
schedule.every(30).minutes.do(scrape)

if __name__ == '__main__':
    # Start the Flask app
    app.run()

    # Start the scheduling loop
    while True:
        schedule.run_pending()
        time.sleep(1)