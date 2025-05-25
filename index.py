
from agent import agent
from promt import create_prompt, build_query_prompt
from model import deepseek_model
from mongo_query import query_mongo, insert_sample_products
import json
import re



# --- CHAT LOOP ---
if __name__ == "__main__":
    print("\nWelcome to Product AI Agent 🤖! (Type 'exit' to quit)\n")
    # while True:
    #     user_input = input("You: ")
    #     if user_input.lower() == "exit":
    #         print("Goodbye! 👋")
    #         break
    #     # user_input = "List all Green Hoodie products"
    #     agent_promt = create_prompt(user_input)
    #     tool_name, parameters = deepseek_model(agent_promt)
    #     print("tools name ->", tool_name)
    #     print("tools parameter ->", parameters)
    #     products = agent(tool_name, parameters)
    #     print(products)


# for testing only 
    user_input = "List all products have category Accessories"
    query_promt = build_query_prompt(user_input)
    # print(query_promt)
    # insert_sample_products("products")
    raw_response = deepseek_model(query_promt)
    print("raw_response from model ->>>", raw_response)
    # Remove markdown backticks and language identifiers like ```json
    cleaned_response = re.sub(r"^```(?:json)?|```$", "", raw_response.strip(), flags=re.MULTILINE).strip()
    try:
        response = json.loads(cleaned_response)
    except Exception as e:
        print("Error parsing response:", e)
        response = {}
    print("Cleaned response from model ->>>", response)
    search_product_query = {
        "filter": response.get("filter", {}),
        "project": response.get("project", {}),
        "limit": response.get("limit", 10),
        "sort": response.get("sort", []),
        "collection_name": "products"
    }
    product_data = query_mongo(search_product_query)
    print("filtered product ",product_data)
    # agent_promt = create_prompt(user_input)
    # tool_name, parameters = deepseek_model(agent_promt)
    # print("tools name ->", tool_name)
    # print("tools parameter ->", parameters)
    # products = agent(tool_name, parameters)
    # print(products)



