import hashlib
from backend.database import login, signup
from datetime import datetime
from fastapi import APIRouter
from pydantic import BaseModel
import traceback
import re

router = APIRouter()

class LoginRequest(BaseModel):
    ten_dang_nhap: str
    password: str

class SignupRequest(BaseModel):
    ten_dang_nhap: str
    password: str
    role: int
    ho_ten: str
    ngay_sinh: str
    gioi_tinh: str
    email: str
    so_dien_thoai: str
    anh_dai_dien: str
    created_at: str
    status: int

@router.post("/login")
def log_in(data: LoginRequest):
    print(">>> ĐÃ VÀO ENDPOINT LOGIN")
    print(">>> username:", repr(data.ten_dang_nhap))
    try:
        input_hash = hashlib.sha256(
            data.password.encode()
        ).hexdigest()
        
        user = login(data.ten_dang_nhap)
        if not user:
            return {
                "success": False,
                "message": "User not found"
        }
        
        stored_hash = user[2]
        
        if input_hash == stored_hash:
            return {
                "success": True,
                "ten_dang_nhap": data.ten_dang_nhap,
                "role": user[3]
            }
        else:
            return {
                "success": False,
                "message": "Wrong password"
            }
    except Exception as e:
        return {
            "success": False,
            "message": "Internal server error"
        }
#Kiểm tra độ mạnh của mật khẩu
def is_strong_password(password):
    return (
        len(password) >= 8 and
        re.search(r"[A-Z]", password) and      # chữ hoa
        re.search(r"[a-z]", password) and      # chữ thường
        re.search(r"[0-9]", password) and      # số
        re.search(r"[!@#$%^&*(),.?\":{}|<>]", password)  # ký tự đặc biệt
    )

@router.post("/signup")
def sign_up(data: SignupRequest):
    try:
        if is_strong_password(data.password):
        
            password_hash = hashlib.sha256(
                data.password.encode()
            ).hexdigest()

            user = signup(
                data.ten_dang_nhap,
                password_hash,
                data.role,
                data.ho_ten,
                data.ngay_sinh,
                data.gioi_tinh,
                data.email,
                data.so_dien_thoai,
                data.anh_dai_dien,
                data.created_at,
                data.status,
            )

            if user:
                return {
                    "success": True,
                    "message": "Đăng ký thành công",
                }
        else: 
            return {
                "success": False,
                "message": "Mật khẩu chưa hợp lệ"
            }
    except Exception as e:
        print(traceback.format_exc())    
