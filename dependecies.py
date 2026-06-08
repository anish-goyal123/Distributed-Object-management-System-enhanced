from fastapi import Header, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
from auth.models import User

def get_current_user(x_user_id: int = Header(...), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == x_user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized. Please register or login.")
    return user