
from promt import create_prompt, build_query_prompt, build_prompt
from model import deepseek_model
from mongo_query import query_mongo, insert_sample_products
from tool_dispatcher.product_tool_dispatcher import call_tool
import json
import re
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import search

app = FastAPI()

# Allow origins (set "*" to allow all)
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Or ["*"] to allow all
    allow_credentials=True,
    allow_methods=["*"],    # ["GET", "POST", "PUT", "DELETE"]
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Hello, World! 🚀"}


# Include routers
app.include_router(search.router)




