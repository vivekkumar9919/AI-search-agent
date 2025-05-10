from db import get_collection
import logging
import json

# Load product data
with open('products.json', 'r') as file:
    products = json.load(file)


def query_mongo(
    collection_name: str,
    filter: dict = {},
    project: dict = None,
    limit: int = 0,
    sort: list = None
):
    try:
        collection = get_collection(collection_name)
        cursor = collection.find(filter, projection=project)

        if sort:
            cursor = cursor.sort(sort)
        if limit:
            cursor = cursor.limit(limit)

        return list(cursor)
    except Exception as e:
        logging.error(f"Error querying {collection_name}: {e}")
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


