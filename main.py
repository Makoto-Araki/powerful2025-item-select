import os
import requests
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("ACCESS_TOKEN")

url = f"https://powerful2025.myshopify.com/admin/api/2024-10/products.json"
headers = {"X-Shopify-Access-Token": TOKEN}
res = requests.get(url, headers=headers)
print(res.status_code)
print(res.json())

