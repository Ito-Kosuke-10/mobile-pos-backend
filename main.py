from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import get_db, create_tables, insert_sample_data, ProductMaster, Transaction, TransactionDetail
from models import ProductSearchRequest, ProductSearchResponse, ProductInfo, PurchaseRequest, PurchaseResponse, PurchaseItem
from config import CORS_ORIGINS
from datetime import datetime

app = FastAPI(title="POS API", version="1.0.0")

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ルートエンドポイント
@app.get("/")
async def root():
    return {"message": "Mobile POS API", "version": "1.0.0", "docs": "/docs", "health": "/health"}

# ヘルスチェック（ルートレベル）
@app.get("/health")
async def health_check_root():
    return {"status": "ok", "message": "POS API is running"}

# データベース初期化
@app.on_event("startup")
async def startup_event():
    create_tables()
    insert_sample_data()

# 商品マスタ検索API
@app.post("/api/products/search", response_model=ProductSearchResponse)
async def search_product(request: ProductSearchRequest, db: Session = Depends(get_db)):
    try:
        # 商品コードで検索
        product = db.query(ProductMaster).filter(ProductMaster.code == request.code).first()
        
        if product:
            product_info = ProductInfo(
                prd_id=product.prd_id,
                code=product.code,
                name=product.name,
                price=product.price
            )
            return ProductSearchResponse(product_info=product_info)
        else:
            return ProductSearchResponse(message="商品がマスタ未登録です")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"検索エラー: {str(e)}")

# 購入API
@app.post("/api/purchase", response_model=PurchaseResponse)
async def purchase(request: PurchaseRequest, db: Session = Depends(get_db)):
    try:
        # 1-1: 取引テーブルへ登録
        transaction = Transaction(
            emp_cd=request.emp_cd,
            store_cd=request.store_cd,
            pos_no=request.pos_no,
            total_amt=0
        )
        db.add(transaction)
        db.flush()  # 取引IDを取得するためにflush
        
        trd_id = transaction.trd_id
        
        # 1-2: 取引明細へ登録
        total_amount = 0
        for i, item in enumerate(request.items, 1):
            transaction_detail = TransactionDetail(
                trd_id=trd_id,
                dtl_id=i,
                prd_id=item.prd_id,
                prd_code=item.code,
                prd_name=item.name,
                prd_price=item.price
            )
            db.add(transaction_detail)
            total_amount += item.price
        
        # 1-3: 合計金額を計算（既に上記で計算済み）
        
        # 1-4: 取引テーブルを更新
        transaction.total_amt = total_amount
        
        db.commit()
        
        return PurchaseResponse(
            success=True,
            total_amount=total_amount,
            message="購入が完了しました"
        )
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"購入エラー: {str(e)}")

# ヘルスチェック
@app.get("/api/health")
async def health_check():
    return {"status": "ok", "message": "POS API is running"}

if __name__ == "__main__":
    import uvicorn
    import os
    
    # Azure App Service用の設定
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
