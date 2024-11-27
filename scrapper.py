
import requests
from bs4 import BeautifulSoup
import csv

def clean_price(price_text):
    """Limpia el texto del precio eliminando símbolos y espacios innecesarios."""
    if price_text:
        return price_text.replace('$', '').replace(' ', '').replace('.', '').replace(',', '.')
    return None

def scrape_products(search_term):
    base_url = 'https://www.ragged.com.co'
    search_url = f'{base_url}/{search_term}?_q={search_term}&map=ft'
    page = 1
    products = []
    max_pages = 10  # Puedes ajustar este número según sea necesario

    while page <= max_pages:
        url = f'{search_url}&page={page}'
        print(f'Extrayendo datos de la página {page}: {url}')
        response = requests.get(url)
        if response.status_code != 200:
            print('No se pudo obtener la página.')
            break
        soup = BeautifulSoup(response.content, 'html.parser')

        # Encontrar todos los contenedores de productos
        product_divs = soup.find_all('div', class_=lambda x: x and 'vtex-search-result-3-x-galleryItem' in x)
        if not product_divs:
            print('No se encontraron más productos.')
            break

        for product in product_divs:
            # Extraer el nombre del producto
            name_tag = product.find('span', class_='vtex-product-summary-2-x-productBrand')
            if name_tag:
                name = name_tag.get_text(strip=True)
            else:
                name = 'No disponible'

            # Extraer el precio actual
            current_price_tag = product.find('span', class_='vtex-store-components-3-x-sellingPriceValue')
            if current_price_tag:
                current_price = clean_price(current_price_tag.get_text(strip=True))
            else:
                current_price = 'No disponible'

            # Extraer el precio anterior
            previous_price_tag = product.find('span', class_='vtex-store-components-3-x-listPriceValue')
            if previous_price_tag:
                previous_price = clean_price(previous_price_tag.get_text(strip=True))
            else:
                previous_price = 'No disponible'

            # Extraer el enlace del producto
            link_tag = product.find('a', href=True)
            if link_tag:
                product_link = base_url + link_tag['href']
            else:
                product_link = 'No disponible'

            # Agregar los datos del producto a la lista
            products.append({
                'Nombre del Producto': name,
                'Precio Actual': current_price,
                'Precio Anterior': previous_price,
                'Enlace del Producto': product_link
            })

        page += 1

    # Guardar los productos en un archivo CSV
    if products:
        keys = products[0].keys()
        with open(f'{search_term}_productos.csv', 'w', newline='', encoding='utf-8') as output_file:
            dict_writer = csv.DictWriter(output_file, keys, delimiter=';')
            dict_writer.writeheader()
            dict_writer.writerows(products)
        print(f'Se extrajeron {len(products)} productos.')
    else:
        print('No se encontraron productos.')

if __name__ == '__main__':
    termino_busqueda = 'vestidos'  # Puedes cambiar el término de búsqueda
    scrape_products(termino_busqueda)
