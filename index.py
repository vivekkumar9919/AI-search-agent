
from promt import create_prompt, build_query_prompt, build_prompt
from model import deepseek_model
from mongo_query import query_mongo, insert_sample_products
from tool_dispatcher.product_tool_dispatcher import call_tool
import json
import re
from fastapi import FastAPI
from routers import search

app = FastAPI()
   

@app.get("/")
def read_root():
    return {"message": "Hello, World! 🚀"}


# Include routers
app.include_router(search.router)




