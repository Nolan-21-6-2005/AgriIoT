from datetime import date
from fastapi import APIRouter
from pydantic import BaseModel, EmailStr
from backend.database import fetch_one, execute
from backend.security import hash_password, verify_password, strong_password

router = APIRouter()
class LoginRequest(BaseModel):
    ten_dang_nhap: str
    password: str
class SignupRequest(BaseModel):
    ten_dang_nhap: str
    password: str
    ho_ten: str
    ngay_sinh: date | None = None
    gioi_tinh: str | None = None
    email: EmailStr | None = None
    so_dien_thoai: str | None = None

@router.post('/login')
def login(data: LoginRequest):
    user = fetch_one('SELECT id,ten_dang_nhap,password,role,ho_ten FROM Users WHERE ten_dang_nhap=?', (data.ten_dang_nhap.strip(),))
    if not user or not verify_password(data.password, user['password']):
        return {'success': False, 'message': 'Sai tên đăng nhập hoặc mật khẩu'}
    return {'success': True, 'user_id': user['id'], 'ten_dang_nhap': user['ten_dang_nhap'], 'ho_ten': user['ho_ten'], 'role': user['role']}

@router.post('/signup')
def signup(data: SignupRequest):
    if not strong_password(data.password):
        return {'success': False, 'message': 'Mật khẩu phải có ít nhất 8 ký tự, chữ hoa, chữ thường, số và ký tự đặc biệt'}
    if fetch_one('SELECT id FROM Users WHERE ten_dang_nhap=?', (data.ten_dang_nhap.strip(),)):
        return {'success': False, 'message': 'Tên đăng nhập đã tồn tại'}
    try:
        execute('INSERT INTO Users (ten_dang_nhap,password,role,ho_ten,ngay_sinh,gioi_tinh,email,so_dien_thoai) VALUES (?,?,?,?,?,?,?,?)',
                (data.ten_dang_nhap.strip(), hash_password(data.password), 1, data.ho_ten.strip(), str(data.ngay_sinh) if data.ngay_sinh else None, data.gioi_tinh, str(data.email) if data.email else None, data.so_dien_thoai))
    except Exception as exc:
        return {'success': False, 'message': str(exc)}
    return {'success': True, 'message': 'Đăng ký thành công'}
