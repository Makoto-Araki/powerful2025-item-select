import os
import requests
import pandas as pd
from dotenv import load_dotenv
import time

# --- トークン読み込み ---
load_dotenv()
TOKEN = os.getenv("ACCESS_TOKEN")

# --- Shopify GraphQLエンドポイント ---
url = "https://powerful2025.myshopify.com/admin/api/2024-10/graphql.json"
headers = {
    "X-Shopify-Access-Token": TOKEN,
    "Content-Type": "application/json"
}

# --- GraphQLクエリ（1商品=1SKU想定、ページネーション対応） ---
query_template = """
query getProducts($cursor: String) {
  products(first: 100, after: $cursor) {
    edges {
      cursor
      node {
        id
        title
        variants(first: 1) {
          edges {
            node {
              id
              price
              inventoryQuantity
            }
          }
        }
      }
    }
    pageInfo {
      hasNextPage
      endCursor
    }
  }
}
"""

# --- 取得ループ ---
all_rows = []
cursor = None

print("✅ 商品データ取得中...")

while True:
    variables = {"cursor": cursor}
    res = requests.post(url, headers=headers, json={"query": query_template, "variables": variables})

    if res.status_code != 200:
        print("❌ APIエラー:", res.status_code, res.text)
        break

    data = res.json()

    # GraphQLエラー検出
    if "errors" in data:
        print("❌ GraphQLエラー:", data["errors"])
        break

    products_data = data["data"]["products"]
    edges = products_data["edges"]

    for edge in edges:
        product = edge["node"]
        variant_data = product["variants"]["edges"]
        if variant_data:
            variant = variant_data[0]["node"]
            all_rows.append({
                "product_id": product["id"],
                "product_title": product["title"],
                "price": variant["price"],
                "inventory_quantity": variant["inventoryQuantity"]
            })
        else:
            # もしバリアントが存在しない商品があれば空値を入れる
            all_rows.append({
                "product_id": product["id"],
                "product_title": product["title"],
                "price": None,
                "inventory_quantity": None
            })

    # ページネーション処理
    page_info = products_data["pageInfo"]
    if page_info["hasNextPage"]:
        cursor = page_info["endCursor"]
        time.sleep(0.3)  # レート制限回避
    else:
        break

print(f"✅ {len(all_rows)} 件の商品データを取得しました。")

# --- DataFrame化 ---
df = pd.DataFrame(all_rows)

# --- CSV出力 ---
csv_file = "output/shopify_products_single_variant.csv"
df.to_csv(csv_file, index=False, encoding="utf-8-sig")

print(f"📦 CSVファイルを出力しました: {csv_file}")
#print("💡 DataFrameの先頭5件:")
#print(df.head())
