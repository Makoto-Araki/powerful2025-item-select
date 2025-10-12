# powerful2025-item-select (商品一覧取得)
## 環境構築

### 前提条件
- Shopifyに開発ストアpowerful2025が存在
- 開発ストアのAPIトークン作成済
- リモートリポジトリ作成済

### ローカルリポジトリ設定からプログラム作成および実行
```bash
## パッケージ情報を更新
$ sudo apt update

## パッケージ本体を更新
$ sudo aptt upgrade

## パッケージインストール
$ sudo apt install python3-venv -y

## ディレクトリ作成
$ mkdir ~/powerful2025-item-select

## ディレクトリ移動
$ cd powerful2025-item-select

## ローカルリポジトリ初期化
$ git init

## ユーザー情報設定
$ git config --global user.email (自分のメールアドレス)
$ git config --global user.name Makoto-Araki

## リモートリポジトリ設定
$ git branch -M main
$ git remote add origin git@github.com:Makoto-Araki/powerful2025-item-select.git

## Pythonバージョン確認
$ python3 --version

## Python仮想環境作成
$ python3 -m venv venv

## Python仮想環境起動
$ source venv/bin/activate

## Pythonライブラリのインストール
$ pip install requests load_dotenv

## Pythonライブラリの一覧ファイル生成
$ pip freeze > requirements.txt

## APIトークンを設定ファイルに追記
$ echo 'ACCESS_TOKEN=(APIトークン)' >> .env

## 設定ファイルをリモートリポジトリのアップロード除外
$ echo 'venv/' >> .gitignore
$ echo '.env' >> .gitignore

## Pythonプログラム記述
$ vi main.py

コマンドの実行結果
----------------------------------------------------------------------
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
----------------------------------------------------------------------

## Pythonプログラム実行
$ python3 main.py

## コミットとリモートリポジトリにプッシュ
$ git add .
$ git commit -m 新規作成
$ git push origin main

## Python仮想環境終了
$ deactivate
```
