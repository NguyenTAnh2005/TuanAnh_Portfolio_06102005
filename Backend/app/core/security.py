# Library for password 
from passlib.context import CryptContext
from datetime import datetime
#Library for JWT
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.db_connection import get_db
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from app.core.config import settings
from app.models import models
from app.schemas import schemas_token
from datetime import datetime, timedelta, timezone
#
from typing import Optional
import string



#================== PASSWORD 
pwd_context = CryptContext(schemes = ["bcrypt"], deprecated = "auto")
# Hashing Password 
def hashing_password(input):
    return pwd_context.hash(input)

# Checking Correct Password 
def checking_pasword(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Convert time String from Github response API to Datetime for PostgreSQL

def parse_github_date(date_str):
   """
   biến đổi chuỗi ở sau cùng và dùng hàm của thư viện biến đổi chuỗi ra object datetime để Máy tính hiểu đc
   """
   if not date_str: return datetime.now()
   return datetime.fromisoformat(date_str.replace("Z", "+00.00"))

#============================ JWT 
# Algrothim which used to hash header + payload + secretkey to create signature
ALGORTHIM = "HS256"
# API url to let Swagger know where to get token 
oauth_sheme = OAuth2PasswordBearer(tokenUrl="/login")


def get_current_user(
        db : Session = Depends(get_db),
        token : str = Depends(oauth_sheme) 
) -> models.User:
    credential_exception = HTTPException(
        status_code = status.HTTP_401_UNAUTHORIZED,
        detail = "Không thể xác thực thông tin đăng nhập!",
        headers = {"WWW-Authenticate" : "Bearer" }
    )

    try: 
        # Giả mã lấy user id
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms = ALGORTHIM)
        user_id: str = payload.get("data")
        email: str = payload.get("sub")
        if user_id is None:
            raise credential_exception
        token_data = schemas_token.TokenPayload(data = int(user_id), sub = email)
    except JWTError:
        raise credential_exception
    
    # Tìm user trong Database 
    user = db.query(models.User).filter(models.User.id == token_data.data).first()
    if not user:
        raise credential_exception
    return user 

def get_current_admin(
    current_user: models.User = Depends(get_current_user),
    )-> models.User:
    if current_user.role_id != 1:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Yêu cầu quyền truy cập Admin! Bạn không có quyền thực hiện hành động này!"
        )
    return current_user

def create_access_token(
        data: dict,
        expries_delta: Optional[timedelta] = None
):
    to_encode = data.copy()
    if expries_delta:
        expire = datetime.now(timezone.utc) + expries_delta
    
    else: 
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp" : expire})

    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm = ALGORTHIM)
    
    return encoded_jwt