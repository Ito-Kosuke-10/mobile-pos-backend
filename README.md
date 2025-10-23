# Mobile POS App - Backend

FastAPIを使用したモバイルPOSアプリのバックエンドAPI

## 機能

- 商品マスタ検索API
- 購入処理API
- SQLite/MySQL対応

## 技術スタック

- FastAPI
- SQLAlchemy
- SQLite (ローカル開発)
- Azure Database for MySQL (本番)

## セットアップ

### 1. 依存関係のインストール

```bash
pip install -r requirements.txt
```

### 2. 環境変数の設定

```bash
# .envファイルを作成
DATABASE_URL=sqlite:///./pos_app.db
```

### 3. サーバーの起動

```bash
python main.py
```

## API仕様

- **ヘルスチェック**: `GET /health`
- **商品検索**: `POST /api/products/search`
- **購入処理**: `POST /api/purchase`
- **API仕様書**: `GET /docs`

## デプロイ

Azure Container InstancesまたはAzure App Serviceでデプロイ可能

詳細は `../azure-deploy.md` を参照
