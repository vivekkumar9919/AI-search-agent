
from tools import search_products_by_word, total_quantity_for_size, filter_by_color, products_in_location


def agent(tool_name, parameters):
    """
    Takes a tool_name, parameters 
    Call corresponding tool ,
    and returns products details based on filter.
    """
    tool_name = tool_name.lower()
    parma = parameters.split('=')[-1].replace('"', '').strip()
    print("Inside agent calling tools for ", tool_name, parameters, parma)

    try:
        if tool_name == "total_quantity_for_size":
            total = total_quantity_for_size(parma)
            return {"size": parma.upper(), "total_quantity": total}

        elif tool_name == "filter_by_color":
            filtered = filter_by_color(parma)
            return {"color": parma, "products": filtered} if filtered else {"message": "No products found."}

        elif tool_name == "products_in_location":
            products_loc = products_in_location(parma)
            return {"location": parma, "products": products_loc} if products_loc else {"message": "No products found."}

        elif tool_name == "search_products_by_word":
            result = search_products_by_word(parma)
            return {"word": parma, "products": result} if result else {"message": "No products found."}

        else:
            return "Sorry, I didn't understand your request."

    except Exception as e:
        print(f"Error occurred in agent: {e}")
        return "Something went wrong while processing your request."
