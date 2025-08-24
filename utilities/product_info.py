product_schema = {
    "product_id": "string",          # Unique product identifier
    "name": "string",                # Product name
    "description": "string",         # Full description
    "category": "string",            # Clothing, Footwear, Accessories etc.
    "sub_category": "string",        # Jackets, Sneakers, Bags etc.
    "brand": "string",               # Nike, Adidas, Levi’s
    "color": "string",               # Red, Blue, Black, etc.
    "size": "string",                # S, M, L, XL, 9, One Size
    "material": "string",            # Cotton, Leather, Polyester
    "gender": "string",              # Men, Women, Unisex, Kids
    "price": "float",                # Base price
    "discount": "float",             # Discount percentage or amount
    "final_price": "float",          # Price after discount
    "currency": "string",            # INR, USD, EUR
    "quantity": "integer",           # Stock available
    "location": "string",            # Warehouse / Store location
    "sku": "string",                 # Seller Stock Keeping Unit
    "seller_id": "string",           # Seller reference
    "details": "string",             # Short details (e.g. Winter wear)
    "images": ["string"],            # List of image URLs
    "rating": "float",               # Avg. customer rating
    "reviews_count": "integer",      # Number of reviews
    "tags": ["string"],              # Search tags
    "created_at": "datetime",        # When product was added
    "updated_at": "datetime"         # Last updated time
}


product_field_values = {
    "category": ["Clothing", "Footwear", "Accessories"],
    "sub_category": [
        "T-Shirts", "Shirts", "Hoodies", "Sneakers", "Sandals",
        "Backpacks", "Watches", "Belts"
    ],
    "brand": ["Nike", "Adidas", "Puma", "Levi's", "H&M", "Zara"],
    "size": ["XS", "S", "M", "L", "XL", "XXL", "6", "7", "8", "9", "10", "One Size"],
    "color": ["Red", "Blue", "Black", "Brown", "Green", "White", "Grey"],
    "material": ["Cotton", "Leather", "Polyester", "Denim", "Wool"],
    "gender": ["Men", "Women", "Unisex", "Kids"],
    "currency": ["INR", "USD", "EUR"],
    "tags": ["Winter", "Summer", "Casual", "Formal", "Trending", "New Arrival"]
}
