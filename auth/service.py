from sqlalchemy.orm import Session
from fastapi import HTTPException
from auth.models import User
from auth.dto import AuthRequest

def register_user(req: AuthRequest, db: Session):
    existing_user = db.query(User).filter(User.username == req.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="This username is already registered.")
    
    new_user = User(username=req.username, password_hash=req.password)
    db.add(new_user)
    db.commit()
    return {"message": "User registered successfully. You can now login."}

def login_user(req: AuthRequest, db: Session):
    user = db.query(User).filter(User.username == req.username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found. Please register first.")
    
    if user.password_hash != req.password:
        raise HTTPException(status_code=401, detail="Incorrect password.")
        
    return {"message": "Login successful", "user_id": user.id}