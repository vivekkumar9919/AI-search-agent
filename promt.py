tools = [
    {
        "name": "search_products_by_word",
        "description": "This tool searches products by a keyword found in their name or description.",
        "parameters": [
            {
                "name": "word",
                "type": "string",
                "description": "The keyword to search for in product name or description."
            }
        ],
        "return_type": "list",
        "return_description": "A list of products matching the keyword."
    },
    {
        "name": "total_quantity_for_size",
        "description": "This tool returns the total quantity of products available in a specific size.",
        "parameters": [
            {
                "name": "size",
                "type": "string",
                "description": "The size to query (e.g., 'S', 'M', 'L')."
            }
        ],
        "return_type": "int",
        "return_description": "An integer representing the total quantity of the given size."
    },
    {
        "name": "filter_by_color",
        "description": "This tool filters products by color.",
        "parameters": [
            {
                "name": "color",
                "type": "string",
                "description": "The color to filter by."
            }
        ],
        "return_type": "list",
        "return_description": "A list of products with the specified color."
    },
    {
        "name": "products_in_location",
        "description": "This tool filters products by location.",
        "parameters": [
            {
                "name": "location",
                "type": "string",
                "description": "The location to filter by."
            }
        ],
        "return_type": "list",
        "return_description": "A list of products with the specified locations."
    }
]

def create_prompt(user_input):
    """
    Takes a user_input and convert into promt,
    and returns promt.
    """
    # List of tools and their descriptions
    tool_descriptions = "\n".join(
        [f"{tool['name']}: {tool['description']} with parameters {tool['parameters']}" for tool in tools]
    )
    
    prompt = f"""
    User input: "{user_input}"
    Tools available: 
    {tool_descriptions}

    Determine which tool best matches the user's query from Tools available. You should extract the tool name and parameters from the user input. Only respond with the tool name and parameters in the format below:

    Tool: <tool_name>
    Parameters: <parameter_value>

    Your response should not contain any extra text. Please ensure the format is exactly as shown in the example.

    Example:
    Input: "What is the total quantity of size M?"
    Tool: total_quantity_for_size
    Parameters: size = "M"

    Input: "List products with the color blue."
    Tool: filter_by_color
    Parameters: color = "blue"

    """
    return prompt

def create_query_promt(user_input):
    """
    This functions are used of creating promt query to convert natural language into mongo queries
    Take user input 
    return mongo queries
    """
    print(user_input)
    return "query_promt"


