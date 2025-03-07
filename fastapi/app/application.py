from fastapi import FastAPI, HTTPException, Depends
from typing import Annotated, List
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.database import SessionLocal, engine
import app.db_models as db_models
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    
    "http://localhost:80",  # For local development
    "http://aws-finance-app-env.eba-ijbmy6jm.us-east-1.elasticbeanstalk.com"  # Production domain
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

class TransactionBase(BaseModel):
    amount: float
    category: str
    description: str  
    is_income: bool
    date: str

class TransactionModel(TransactionBase):
    id: int

    class Config:
        orm_mode = True

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()  

db_dependency = Annotated[Session, Depends(get_db)]

db_models.Base.metadata.create_all(bind=engine)

@app.post("/api/add_transactions/", response_model=TransactionModel)
async def create_transaction(transaction: TransactionBase, db: db_dependency):
    db_transaction = db_models.Transaction(**transaction.dict())
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

@app.get("/api/get_transactions/", response_model=List[TransactionModel])
async def read_transactions(db: db_dependency, skip: int = 0, limit: int = 100):
    transactions = db.query(db_models.Transaction).offset(skip).limit(limit).all()
    return transactions