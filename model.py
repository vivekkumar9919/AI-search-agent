from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
API_KEYS = os.getenv('OPEN_ROUTER_API_KEYS')

# Initialize OpenAI client
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=API_KEYS,
)

def deepseek_model(prompt: str) -> str:
    """
    Takes a prompt, sends it to DeepSeek model via OpenRouter API,
    and returns the response.
    """
    try:
        print("calling model")
        completion = client.chat.completions.create(
            model="deepseek/deepseek-r1:free",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        response = completion.choices[0].message.content
        return response
    except Exception as e:
        print(f"Error occurred while fetching response: {e}")
        return None