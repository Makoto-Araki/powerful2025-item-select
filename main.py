import os
import requests
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("ACCESS_TOKEN")

# Admin API URL
url = f"https://powerful2025.myshopify.com/admin/api/2024-10/graphql.json"

# Header
headers = {
    "X-Shopify-Access-Token": TOKEN,
    "Content-Type": "application/json"
}

# Query
query = """
{
    products(first:10) {
        edges {
            node {
                id
                title
            }
        }
    }
}
"""

# Execute GraphQL
res = requests.post(url, headers=headers, json={"query": query})

# Print Results
if res.status_code == 200:
    data = res.json()
    products = data["data"]["products"]["edges"]
    for p in products:
        product = p["node"]
        print(f"商品ID: {product['id']}")
        print(f"商品名: {product['title']}")
else:
    print("Error:", res.status_code, res.text)
