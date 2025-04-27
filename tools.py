
import json

# Load product data
with open('products.json', 'r') as file:
    products = json.load(file)

# print("product json", products)

# --- TOOL 1: Search products by a keyword ---
def search_products_by_word(word):
    results = []
    for product in products:
        if word.lower() in product['name'].lower() or word.lower() in product['description'].lower():
            results.append(product)
    return results

# --- TOOL 2: Get total quantity for a given size ---
def total_quantity_for_size(size):
    total = 0
    for product in products:
        if product['size'].lower() == size.lower():
            total += product['quantity']
    return total

# --- TOOL 3: Filter products by color ---
def filter_by_color(color):
    return [product for product in products if product['color'].lower() == color.lower()]