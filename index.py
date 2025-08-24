
from promt import create_prompt, build_query_prompt, build_prompt
from model import deepseek_model
from mongo_query import query_mongo, insert_sample_products
from tool_dispatcher.product_tool_dispatcher import call_tool
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
    # user_input = "List all products with price greater then 2000 "
    # user_input = "What is the average price of all my shirts "
    # user_input = "Which products give me the highest profit margin"
    # user_input = "Show me items with low stock that may sell out in less than 10 days"
    user_input = "Which price band has the maximum number of products?"

    # query_promt = build_query_prompt(user_input)
    query_promt = build_prompt(user_input)
    # print(query_promt)
    # insert_sample_products("products")
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
    # agent_promt = create_prompt(user_input)
    # tool_name, parameters = deepseek_model(agent_promt)
    # print("tools name ->", tool_name)
    # print("tools parameter ->", parameters)
    # products = agent(tool_name, parameters)
    # print(products)



