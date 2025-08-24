
from utilities.product_info import product_schema, product_field_values
from sample_data.product_data import sample_product

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

advanced_tools = [
    {
        "name": "calculate_average_price",
        "type": "advanced",
        "description": "Compute the average price of the list of products returned from MongoDB.",
        "when_to_use": [
            "User asks for average/mean/typical price of any set of products",
            "User asks to summarize pricing for results"
        ],
        "parameters": [],  
        "returns": {"type": "number", "description": "Average price as a float"}
    },
        {
        "name": "profit_margin_analyzer",
        "type": "advanced",
        "description": "Calculate the profit margin percentage for products based on (price - final_price) / price * 100. Useful for analyzing discount-driven profit margins.",
        "when_to_use": [
            "User asks for average/median/highest/lowest profit margin across a set of products",
            "User wants to compare margins across categories or brands",
            "User is analyzing which products give the best discount-based margin"
        ],
        "parameters": [],
        "returns": {"type": "number", "description": "Average profit margin percentage across the products"}
    },
    {
        "name": "low_stock_with_velocity",
        "type": "advanced",
        "description": "Identify products that are low in stock compared to their sales velocity (units sold per day). Helps sellers detect which products may go out of stock soon.",
        "when_to_use": [
            "User asks 'which products are selling fast but have low stock?'",
            "User wants alerts for products at risk of stockout",
            "User wants to plan reordering decisions based on demand vs stock"
        ],
        "parameters": [
            {"name": "stock_threshold", "type": "integer", "description": "Stock level below which a product is considered low"},
            {"name": "days_window", "type": "integer", "description": "Number of days to calculate sales velocity"}
        ],
        "returns": {"type": "list", "description": "List of products at risk of stockout with their stock and velocity"}
    },
    {
        "name": "price_band_distribution",
        "type": "advanced",
        "description": "Categorize products into predefined price bands (e.g., 0–500, 500–1000, 1000–2000, etc.) and compute how many products fall into each band. Useful for understanding product positioning.",
        "when_to_use": [
            "User asks for product distribution across price ranges",
            "User wants to know which price bands have the most/least products",
            "User is analyzing pricing strategy across categories"
        ],
        "parameters": [
            {"name": "bands", "type": "list", "description": "List of tuples defining price ranges e.g., [(0,500),(500,1000)]"}
        ],
        "returns": {"type": "dict", "description": "Dictionary of price bands and product counts"}
    },
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
{product_field_values}

Sample Product:
{sample_product}

Now based on this schema, values, and user input, generate the MongoDB query as described above.
Respond with a valid JSON object with keys filter, project, limit, and sort. Do not use Python syntax. Only return the JSON object without any explanation or comments.

User Input:
\"\"\"{user_input}\"\"\"
""".strip()



# --------------------------------------------------------------------------------#

OUTPUT_FORMAT_PROMT = """
Return a VALID JSON object with EXACTLY these keys:

{
  "query_part": {
    "filter": { ... },               // simple equality/range/regex only
    "project": { ... },              // project ALL fields unless user asked specific ones
    "limit": <int <= 10>,            // default 10
    "sort": [ ["field", 1 or -1] ]   // empty array [] if no sort
  },
  "analysis_required": true | false, // true if additional processing beyond direct Mongo filter is needed
  "advanced_tool": "tool_name_or_null", // if analysis_required=true, set to an available tool name; else null
  "advanced_parameters": { }         // optional object; use {} if no extra params needed
}

STRICT RULES:
- OUTPUT JSON ONLY. No code fences. No comments. No trailing commas.
- Use ONLY fields from the schema.
- Equality: color/category/location/size by exact value from product_field_values when clearly stated.
- Range: use $lt/$lte/$gt/$gte when phrases like "below/under", "above/over" are used.
- Keyword text match: use case-insensitive $regex for simple contains on name/description.
- Project ALL fields unless the user explicitly limits which fields to show.
- Use correct case for values from product_field_values (e.g., "Red", not "red").
- If analysis is clearly required (e.g., 'average price'), set analysis_required=true and advanced_tool accordingly.
"""


def build_prompt(user_input: str) -> str:
    return f"""
You are an AI planner that (1) builds a simple MongoDB query and (2) decides if an advanced analysis tool is needed.

SCHEMA:
{product_schema}

ALLOWED FIELD VALUES:
{product_field_values}

SAMPLE PRODUCT:
{sample_product}

AVAILABLE TOOLS:
{advanced_tools}

WHAT TO DO:
1) Parse the user's request.
2) Build a simple MongoDB query (filters only; no aggregation).
3) Decide if analysis is needed (e.g., computing average price).
4) If needed, select an appropriate advanced tool and set analysis_required=true; otherwise false.

{OUTPUT_FORMAT_PROMT}

User Input:
\"\"\"{user_input}\"\"\"
""".strip()

