from db import get_collection
import logging
import json

# Load product data
with open('products.json', 'r') as file:
    products = json.load(file)


def query_mongo(search_product_query):
    try:
        print("Mongo queries", search_product_query)
        collection = get_collection(search_product_query["collection_name"])
        cursor = collection.find(
            search_product_query["filter"], 
            projection=search_product_query["project"]
        )

        if search_product_query.get("sort"):
            cursor = cursor.sort(search_product_query["sort"])
        if search_product_query.get("limit"):
            cursor = cursor.limit(search_product_query["limit"])

        return list(cursor)
    except Exception as e:
        logging.error(f"Error querying {search_product_query.get('collection_name', 'unknown')}: {e}")
        return []

    


def insert_sample_products(collection_name: str = "products"):
    data = products
    try:
        collection = get_collection(collection_name)
        result = collection.insert_many(data)
        logging.info(f"Inserted {len(result.inserted_ids)} documents into '{collection_name}'")
        return result.inserted_ids
    except Exception as e:
        logging.error(f"Failed to insert products: {e}")
        return []


