from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.db_connection import get_db
from app.models import models
from app.core.security import checking_pasword, create_access_token
from app.schemas import schemas_token

router = APIRouter(tags = ["Authentication"])

@router.post("/login", response_model = schemas_token.Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    # form_data sẽ có 2 trường: username và password
    # Vì hệ thống mình dùng Email đăng nhập, nên ta lấy form_data.username đem so với cột Email trong DB
    user = db.query(models.User).filter(models.User.email == form_data.username).first()

    if not user or not checking_pasword(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email hoặc mật khẩu chưa chính xác!",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    access_token = create_access_token(
        data = {
            "data" : str(user.id),
            "sub": str(user.email)
        }
    )
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
