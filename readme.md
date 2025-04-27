# 🚲 AI Agent for Product Querying

## 📖 Project Overview

This project is a basic AI agent that understands user queries related to products and calls the correct internal tool (function) to fetch data accordingly.  
It acts like a lightweight intelligent backend service for e-commerce-like search operations.

The agent determines which tool to call and what parameters to pass, using the DeepSeek model.

## ❓ Why This is Required

- Simplifies user interactions without needing complex manual filters.
- Automates tool selection based on free-form user text.
- Acts as a stepping stone towards building more intelligent agents.
- Reduces hardcoding of conditions and makes the system extendable.

## 🤖 Model Used

- **Model:** `deepseek/deepseek-r1:free` via OpenRouter API.
- **Why DeepSeek:** It's a free, capable model perfect for parsing structured outputs like tool names and parameters.

## 📁 File Descriptions:

- **`index.py`**: This is the entry point for the project. It gets user input, constructs a prompt, and invokes the agent to fetch the required data.
  
- **`prompt.py`**: This file creates a prompt based on the user's query and the available tools. The prompt is passed to the model to determine which tool to use.

- **`model.py`**: Contains the client code for interacting with the DeepSeek model. It sends the constructed prompt and receives the response containing the tool name and parameters.

- **`agent.py`**: This file decides which tool to call based on the model's output (`tool_name`) and executes the corresponding function from `tools.py`.

- **`tools.py`**: Contains functions to filter products based on different criteria like color, size, and location. Each function corresponds to one of the tools mentioned above.

- **`products.json`**: Contains dummy product data (could be replaced with real database queries in the future). It’s used to simulate the output of the various tool functions.

## 🔍 Currently Supported Tools (Functions)

| Tool Name               | Purpose                                         |
| ------------------------ | ----------------------------------------------- |
| `search_products_by_word`| Search products based on a keyword in name/description |
| `total_quantity_for_size`| Get total quantity available for a specific size |
| `filter_by_color`        | Get products filtered by color                 |
| `products_in_location`   | Get products available in a specific warehouse/location |

## ✏️ Example User Queries

| User Query                        | Tool Selected             | Parameters          |
| ---------------------------------- | -------------------------- | -------------------- |
| "List products with the color red."| `filter_by_color`          | `color = "red"`      |
| "What is the total quantity of size M?"| `total_quantity_for_size` | `size = "M"`         |
| "Show me products containing 'jeans'."| `search_products_by_word` | `word = "jeans"`     |
| "List products in warehouse A."    | `products_in_location`     | `location = "A"`     |

## 🚀 Future Scope

- **Adding More Tools:** New actions like filtering by price, category, discount percentage, etc.
- **Using Database Instead of JSON:** Connect to a real database (like MongoDB, PostgreSQL) instead of static JSON.
- **Complex Search Filters:** Allow multi-condition queries like "Red shoes in Warehouse B under ₹1000."
- **Conversation Memory:** Remember previous queries and allow follow-up questions.
- **User Authentication & Authorization:** Add token-based access to different tools based on user roles.
- **Front-end Integration:** Build a simple UI to interact with the agent via web.

Made with ❤️ by **Vivek**

