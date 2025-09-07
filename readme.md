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

# Development Plan 🎯

This document outlines the phased development roadmap for the AI Agent system. It focuses on intelligent product querying using natural language and tool-based execution logic.

---

## Phase 1: MongoDB Integration & Query Abstraction ( Completed )

The goal of Phase 1 is to replace the static JSON-based logic with real MongoDB-backed queries and build a scalable base for future NLP-to-query translations.

- [x] Replace static `products.json` with actual MongoDB collection.
- [x] Create a centralized MongoDB connection module.
    - e.g., `db.py` to handle `get_collection(collection_name)` access.
- [x] Refactor existing tools to perform MongoDB queries directly:
    - [x] `search_products_by_word`
    - [x] `total_quantity_for_size`
    - [x] `filter_by_color`
    - [x] `products_in_location`
- [x] Environment support for MongoDB URI (`.env`)
- [x] Document schema assumptions for the `products` collection.
- [x] Support prompt to MongoDB query generation logic (e.g., translate: “products with price < 500 and color red” → MongoDB filter).
- [x] Update the product schema so that it aligns with real-world product data
- [x] Add data seed file 
- [x] Create structure to define tools that require logic beyond MongoDB queries.
- [x] **Multi-tool execution support**
    - Allow chaining multiple tools if one query needs multiple steps.
    - Example: “List red shoes and their average price”
- [x] **Tool composition logic**
    - e.g., One tool extracts a list, another analyzes it.

    ## Supported Advanced Tools in Phase 1

    🔹 `calculate_average_price`
    Helps calculate the **average price** of products across categories, collections, or identifiers.

    **Example Queries:**
    - "What’s the average price of all my shirts?"
    - "Give me the typical price across products in Electronics."
    - "On average, how much are my sneakers priced?"

    ---

   🔹 `profit_margin_analyzer`
    Analyzes products by **profit margin** to identify the most and least profitable items or categories.

    **Example Queries:**
    - "Which products give me the highest profit margin?"
    - "Show me products with profit margin less than 20%."
    - "List top 5 categories by average profit margin."

    ---

   🔹 `low_stock_alert_with_velocity`
    Generates **low-stock alerts** by combining current inventory with sales velocity.  
    ⚠️ *Note: Velocity is currently hardcoded in this version.*

    **Example Queries:**
    - "Which products will run out soon if sales continue at current speed?"
    - "Show me items with low stock that may sell out in less than 10 days."
    - "Alert me for fast-moving items with less than 5 units left."

    ---

    🔹 `price_band_distribution`
    Provides insights into the **distribution of products by price ranges**.

    **Example Queries:**
    - "How many products fall between ₹1000–₹2000?"
    - "Show me distribution of products in price ranges of 500, 1000, and 2000."
    - "Which price band has the maximum number of products?"

---

##  Phase 2: Multi-Tool Logic & UX ( in-progress )

The focus of Phase 2 is to introduce multi-tool chaining, smarter decisioning, user-aware logic, and UX enhancements.

- [ ] **Decision making based on user-specific or historical data**
    - Purchase history
    - Inventory movement
    - Past preferences
- [x] **Create a API for frontend**
    - e.g., get products
- [ ] **Product search integration with backend**
    - Connect AI search with backend APIs
    - Ensure results are fetched in real-time
- [ ] **Tool metadata update for better agent decisions**
    - e.g., Tool description, expected inputs/outputs
- [ ] **Frontend/CLI enhancements**
    - Create a basic UI (React/HTML or CLI-based)
    - Allow step-by-step interaction with the agent
- [ ] **Better error handling and fallbacks**
    - Unknown tool
    - Missing parameters
    - Tool chaining failure

## Phase 3: Advanced Intelligence, Chatbot & Backend Integrations

The focus of Phase 3 is to introduce advanced intelligence with session memory, conversational context, chatbot capabilities, and deeper backend integrations.

- [ ] **Session memory or context**
    - Enable context retention for follow-up queries
    - Store temporary query results if needed
- [ ] **Conversational chatbot**
    - Interactive chat-based interface
    - Understands multi-turn queries
    - Returns results while maintaining context (e.g., "Show me jackets" → "Only in black" → "Under ₹3000")
- [ ] **Chatbot integration with backend**
    - Connect chatbot to backend APIs
    - Allow real-time responses (product availability, inventory, recommendations)

---
Made with ❤️ by **Vivek**

