from promt import create_prompt, build_query_prompt, build_prompt
from model import deepseek_model
from mongo_query import query_mongo, insert_sample_products
from tool_dispatcher.product_tool_dispatcher import call_tool
import json
import re
from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from bson import ObjectId

from models.request_models import SearchRequest

router = APIRouter()

@router.post("/search")
def search_items(request: SearchRequest):
    user_input = request.search_message
    page = request.page_info.page
    limit = request.page_info.limit
    # user_input = "List all products with price greater then 2000"

    # query_promt = build_query_prompt(user_input)
    query_promt = build_prompt(user_input)
    raw_response = deepseek_model(query_promt)
    print("raw_response from model ->>>", raw_response)

    cleaned_response = re.sub(r"^```(?:json)?|```$", "", raw_response.strip(), flags=re.MULTILINE).strip()
    response = {}
    try:
        response = json.loads(cleaned_response)
    except Exception as e:
        print("Error parsing response:", e)
        response = {}
    print("Cleaned response from model ->>>", response)
    query_part = response.get('query_part')
    search_product_query = {
        "filter": query_part.get("filter", {}),
        "project": query_part.get("project", {}),
        "limit": query_part.get("limit", 10),
        "sort": query_part.get("sort", []),
        "collection_name": "products"
    }
    product_data = query_mongo(search_product_query)
    tool_response = {}
    if(response.get('analysis_required')):
        print("calling advanced tools", response.get('advanced_tool'), response.get('advanced_parameters'), len(product_data))
        tool_response = call_tool(
            response.get('advanced_tool'),
            product_data,
            **(response.get('advanced_parameters') or {})
        )

        print("\n tool response ", tool_response)
    else :
        print("\n\n")
        print("filtered product ",len(product_data))


    # Pagination
    start = (page - 1) * limit
    end = start + limit

    total = len(product_data)
    total_pages = (total + limit - 1) // limit  

    return {
        "page_info": {
            "total_items": total,
            "page": page,
            "limit": limit,
            "total_pages": total_pages,
            "has_next": page < total_pages,
            "has_prev": page > 1,
        },
        "product": jsonable_encoder(product_data, custom_encoder={ObjectId: str}),
        "tools_response": jsonable_encoder(tool_response, custom_encoder={ObjectId: str})
    }
