import random
from faker import Faker
from datetime import datetime
from db import get_collection

# Initialize Faker
fake = Faker()

products_collection = get_collection("products")

# Product schema categories
CATEGORIES = {
    "Clothing": ["T-Shirts", "Jeans", "Jackets", "Dresses", "Shirts"],
    "Footwear": ["Sneakers", "Boots", "Sandals", "Flip-Flops"],
    "Accessories": ["Bags", "Belts", "Wallets", "Sunglasses", "Watches"],
}

BRANDS = ["Nike", "Adidas", "Puma", "Levi's", "Zara", "H&M", "Ray-Ban", "Fossil"]
COLORS = ["Red", "Blue", "Black", "White", "Green", "Grey", "Yellow"]
SIZES = ["XS", "S", "M", "L", "XL", "XXL", "One Size", "6", "7", "8", "9", "10", "11"]
MATERIALS = ["Cotton", "Leather", "Polyester", "Wool", "Silk", "Denim"]
GENDERS = ["Men", "Women", "Unisex", "Kids"]
CURRENCIES = ["INR", "USD", "EUR"]

def generate_product():
    category = random.choice(list(CATEGORIES.keys()))
    sub_category = random.choice(CATEGORIES[category])
    brand = random.choice(BRANDS)
    color = random.choice(COLORS)
    size = random.choice(SIZES)
    material = random.choice(MATERIALS)
    gender = random.choice(GENDERS)
    price = round(random.uniform(500, 10000), 2)
    discount = round(random.uniform(0, 50), 2)  # percentage
    final_price = round(price - (price * discount / 100), 2)
    currency = random.choice(CURRENCIES)
    quantity = random.randint(0, 500)

    product = {
        "product_id": fake.uuid4(),
        "name": f"{brand} {sub_category} {color}",
        "description": fake.text(max_nb_chars=50),
        "category": category,
        "sub_category": sub_category,
        "brand": brand,
        "color": color,
        "size": size,
        "material": material,
        "gender": gender,
        "price": price,
        "discount": discount,
        "final_price": final_price,
        "currency": currency,
        "quantity": quantity,
        "location": fake.city(),
        "sku": fake.bothify(text="SKU-####??"),
        "seller_id": fake.uuid4(),
        "details": random.choice(["Casual wear", "Winter wear", "Formal wear", "Sportswear"]),
        "images": [fake.image_url(width=400, height=400) for _ in range(random.randint(1, 4))],
        "rating": round(random.uniform(1, 5), 1),
        "reviews_count": random.randint(0, 5000),
        "tags": [fake.word() for _ in range(random.randint(2, 6))],
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    return product

def seed_products(n=50):
    products = [generate_product() for _ in range(n)]
    products_collection.insert_many(products)
    print(f"Inserted {n} products successfully!")

if __name__ == "__main__":
    seed_products(20)  