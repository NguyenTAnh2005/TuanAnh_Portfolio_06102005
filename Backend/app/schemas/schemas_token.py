from pydantic import BaseModel
from typing import Optional

# Với dự án portfolio này thì JWT ko quá khắt khe, chỉ admin thì chỉnh sửa TT
# Khi gửi email cũng không chắc là cần cần đăng ký tài khoản.  
# Schema này dùng để trả về cho Frontend ngay sau khi Login thành công
class Token(BaseModel):
    access_token : str
    token_type : str

# Schema này dùng để giải mã token (khi frontend gửi token lên để lấy dữ liệu)
class TokenPayload(BaseModel):
    data : Optional[int] = None # chứa id của User
    sub : Optional[str] = None # Chứa thông tin thêm như email 