
from agent import agent
from promt import create_prompt
from model import deepseek_model



# --- CHAT LOOP ---
if __name__ == "__main__":
    print("\nWelcome to Product AI Agent 🤖! (Type 'exit' to quit)\n")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            print("Goodbye! 👋")
            break
        # user_input = "List all Green Hoodie products"
        agent_promt = create_prompt(user_input)
        tool_name, parameters = deepseek_model(agent_promt)
        print("tools name ->", tool_name)
        print("tools parameter ->", parameters)
        products = agent(tool_name, parameters)
        print(products)



