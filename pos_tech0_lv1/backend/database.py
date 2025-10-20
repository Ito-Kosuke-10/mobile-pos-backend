from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, CHAR, VARCHAR, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
from config import DATABASE_URL

# SQLiteの場合は特殊な設定が必要
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 商品マスタテーブル
class ProductMaster(Base):
    __tablename__ = "product_master"
    
    prd_id = Column(Integer, primary_key=True, index=True)  # 商品一意キー
    code = Column(CHAR(13), unique=True, nullable=False)    # 商品コード
    name = Column(VARCHAR(50), nullable=False)             # 商品名称
    price = Column(Integer, nullable=False)                # 商品単価
    
    # リレーション
    transaction_details = relationship("TransactionDetail", back_populates="product")

# 取引テーブル
class Transaction(Base):
    __tablename__ = "transaction"
    
    trd_id = Column(Integer, primary_key=True, index=True)  # 取引一意キー
    datetime = Column(TIMESTAMP, default=datetime.now)     # 取引日時
    emp_cd = Column(CHAR(10), default="9999999999")        # レジ担当者コード
    store_cd = Column(CHAR(5), default="30")               # 店舗コード
    pos_no = Column(CHAR(3), default="90")                 # POS機ID
    total_amt = Column(Integer, default=0)                 # 合計金額
    
    # リレーション
    transaction_details = relationship("TransactionDetail", back_populates="transaction")

# 取引明細テーブル
class TransactionDetail(Base):
    __tablename__ = "transaction_detail"
    
    trd_id = Column(Integer, ForeignKey("transaction.trd_id"), primary_key=True)  # 取引一意キー
    dtl_id = Column(Integer, primary_key=True)                                    # 取引明細一意キー
    prd_id = Column(Integer, ForeignKey("product_master.prd_id"))                # 商品一意キー
    prd_code = Column(CHAR(13), nullable=False)                                  # 商品コード
    prd_name = Column(VARCHAR(50), nullable=False)                               # 商品名称
    prd_price = Column(Integer, nullable=False)                                  # 商品単価
    
    # リレーション
    transaction = relationship("Transaction", back_populates="transaction_details")
    product = relationship("ProductMaster", back_populates="transaction_details")

# データベーステーブル作成
def create_tables():
    Base.metadata.create_all(bind=engine)

# サンプルデータの挿入
def insert_sample_data():
    db = SessionLocal()
    try:
        # 既存データをチェック
        if db.query(ProductMaster).count() > 0:
            return
        
        # サンプル商品データ
        sample_products = [
            ProductMaster(code="12345678901", name="おーいお茶", price=150),
            ProductMaster(code="12345678902", name="ソフラン", price=300),
            ProductMaster(code="12345678903", name="福島産ほうれん草", price=188),
            ProductMaster(code="12345678904", name="タイガー歯ブラシ青", price=200),
            ProductMaster(code="12345678905", name="四ツ谷サイダー", price=160),
        ]
        
        for product in sample_products:
            db.add(product)
        
        db.commit()
        print("サンプルデータを挿入しました")
    except Exception as e:
        print(f"サンプルデータ挿入エラー: {e}")
        db.rollback()
    finally:
        db.close()

# データベース接続の取得
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
