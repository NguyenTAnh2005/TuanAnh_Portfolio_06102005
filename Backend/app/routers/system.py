from fastapi import APIRouter, HTTPException, status, Depends, Header
from app.models import models
from sqlalchemy.orm import Session
from app.crud import crud_user
from app.db_connection import get_db
from app.core.config import settings
from app.core.discord_notification import send_discord_alert


router = APIRouter(
    prefix = "/system",
    tags = ["System"]
)


@router.post("/maintenance/restore")
async def trigger_admin_recovery(
    x_recovery_key: str = Header(...,alias = "X-Recovery-Key"),
    db: Session = Depends(get_db)
):
    if x_recovery_key != settings.RECOVERY_KEY_ADMIN:
        await send_discord_alert(
            title="⚠️ CẢNH BÁO XÂM NHẬP",
            description="Có người vừa nhập sai Recovery Key để cố gắng chiếm quyền Admin!",
            color=15158332
        )
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Mã xác thực không hợp lệ, truy cập bị từ chối"
        )
    # If the key is valid, call function  to restore admin account
    try:
        result = crud_user.recovery_first_admin_account(db)
        await send_discord_alert(
            title="✅ KHÔI PHỤC THÀNH CÔNG",
            description="Hệ thống vừa khôi phục tài khoản Admin về trạng thái mặc định.",
            color=3066993
        )
        return result
    except Exception as e:
        await send_discord_alert(
            title="🔥 LỖI CRITICAL",
            description=f"Hàm recovery bị crash: {str(e)}",
            color=15844367
        )
        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = f" Lỗi hệ thống khi khôi phục: {str(e)}"
        )
