from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, Column, Integer, String, Float
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from typing import List

app = FastAPI()

# Define SQLAlchemy engine and session for SQLite3
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# SQLAlchemy model for SQLite3
Base = declarative_base()

class Addresse(Base):
    __tablename__ = "addresses"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)

# Create the SQLite3 database and tables
Base.metadata.create_all(bind=engine)

# Pydantic model for input data
from pydantic import BaseModel

class AddressCreate(BaseModel):
    name: str
    latitude: float
    longitude: float

# CRUD operations
@app.post("/addresses/", response_model=AddressCreate)
def create_address(address: AddressCreate, db: Session = Depends(get_db)):
    db_address = Addresse(**address.dict())
    db.add(db_address)
    db.commit()
    db.refresh(db_address)
    return db_address

@app.get("/addresses/", response_model=List[AddressCreate])
def read_addresses(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(Addresse).offset(skip).limit(limit).all()

@app.put("/addresses/{address_id}", response_model=AddressCreate)
def update_address(address_id: int, address: AddressCreate, db: Session = Depends(get_db)):
    db_address = db.query(Addresse).filter(Addresse.id == address_id).first()
    if db_address is None:
        raise HTTPException(status_code=404, detail="Address not found")
    for key, value in address.dict().items():
        setattr(db_address, key, value)
    db.commit()
    db.refresh(db_address)
    return db_address

@app.delete("/addresses/{address_id}", response_model=AddressCreate)
def delete_address(address_id: int, db: Session = Depends(get_db)):
    db_address = db.query(Addresse).filter(Addresse.id == address_id).first()
    if db_address is None:
        raise HTTPException(status_code=404, detail="Address not found")
    db.delete(db_address)
    db.commit()
    return db_address
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)