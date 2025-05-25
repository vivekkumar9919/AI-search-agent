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

sample_product = {
    "name": "Green Hoodie",
    "description": "Cozy hoodie for winter with front pockets.",
    "location": "A",
    "quantity": 90,
    "size": "L",
    "details": "Winter wear",
    "color": "Green",
    "category": "Clothing",
    "price": 5000
}

product_schema = {
    "name": "string",
    "description": "string",
    "location": "string",
    "quantity": "integer",
    "size": "string",
    "details": "string",
    "color": "string",
    "category": "string",
    "price": "integer"
}

field_values = {
    "category": ["Clothing", "Footwear", "Accessories"],
    "size": ["S", "M", "L", "9", "One Size"],
    "color": ["Red", "Blue", "Black", "Brown", "Green"]
}



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




output_format  = f"""Use the format below:{{
filter={{{{...}}}},
project={{{{...}}}},
limit=...,
sort=[("field", 1 or -1)]
}}"""


def build_query_prompt(user_input: str) -> str:
    return f"""
You are an intelligent MongoDB query assistant.

You will receive user input in natural language.
Your job is to convert it into a MongoDB query using only simple filter conditions (e.g., field equality or range).

{output_format}

Rules:
- Only use fields from the schema.
- Use equality conditions for values clearly specified by the user (e.g., color, category).
- Use range conditions (>, <) if the user says "above", "greater than", "less than", etc.
- Project ALL fields unless user explicitly asks for specific ones.
- Limit must be <= 10 (default to 10 if not specified).
- Use an empty `sort=[]` if no sort is mentioned.
- Use correct case for values (e.g., "Red", not "red").

Schema:
{product_schema}

Available Field Values:
{field_values}

Sample Product:
{sample_product}

Now based on this schema, values, and user input, generate the MongoDB query as described above.
Respond with a valid JSON object with keys filter, project, limit, and sort. Do not use Python syntax. Only return the JSON object without any explanation or comments.

User Input:
\"\"\"{user_input}\"\"\"
""".strip()




