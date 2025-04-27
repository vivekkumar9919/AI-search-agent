from transformers import pipeline
from huggingface_hub import login
import os
import logging
from dotenv import load_dotenv

from tools import search_products_by_word, total_quantity_for_size, filter_by_color

load_dotenv()
API_KEYS = os.getenv('API_KEYS')
print("api", API_KEYS)

os.environ["TOKENIZERS_PARALLELISM"] = "false"
logging.getLogger("transformers").setLevel(logging.ERROR)

# Log in with your token
login(token= API_KEYS)

print("Search by name", search_products_by_word("Red Cotton T-shirt"))

# Initialize the pipeline
generator = pipeline("text-generation", model="gpt2")

# Generate text
prompt = "What's is html"
response = generator(prompt, max_length=1024)
print(response[0]['generated_text'])
