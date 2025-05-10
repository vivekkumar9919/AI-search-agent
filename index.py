
from agent import agent
from promt import create_prompt, create_query_promt
from model import deepseek_model
from mongo_query import query_mongo, insert_sample_products



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
    user_input = "List all Green Hoodie products"
    query_promt = create_query_promt(user_input)
    print(query_promt)
    # insert_sample_products("products")
    product_data = query_mongo(
        collection_name="products",
        filter={"color": "Red"},
        project={"_id": 0, "name": 1, "color": 1},
        limit=5,
        sort=[("name", 1)]
    )
    print(product_data)
    # agent_promt = create_prompt(user_input)
    # tool_name, parameters = deepseek_model(agent_promt)
    # print("tools name ->", tool_name)
    # print("tools parameter ->", parameters)
    # products = agent(tool_name, parameters)
    # print(products)



