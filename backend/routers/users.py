from datetime import date
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from backend.database import fetch_all, fetch_one, update
from backend.security import hash_password, verify_password, strong_password
router=APIRouter()
class UserUpdate(BaseModel):
    ho_ten:str; ngay_sinh:date|None=None; gioi_tinh:str|None=None; email:EmailStr|None=None; so_dien_thoai:str|None=None
class PasswordUpdate(BaseModel):
    old_password:str; new_password:str
@router.get('')
def list_users(): return fetch_all('SELECT id,ten_dang_nhap,role,ho_ten,ngay_sinh,gioi_tinh,email,so_dien_thoai,created_at FROM Users ORDER BY id')
@router.get('/{user_id}')
def get_user(user_id:int):
    u=fetch_one('SELECT id,ten_dang_nhap,role,ho_ten,ngay_sinh,gioi_tinh,email,so_dien_thoai,anh_dai_dien,created_at FROM Users WHERE id=?',(user_id,))
    if not u: raise HTTPException(404,'Không tìm thấy người dùng')
    return u
@router.put('/{user_id}')
def update_user(user_id:int,data:UserUpdate):
    if not fetch_one('SELECT id FROM Users WHERE id=?',(user_id,)): raise HTTPException(404,'Không tìm thấy người dùng')
    update('UPDATE Users SET ho_ten=?,ngay_sinh=?,gioi_tinh=?,email=?,so_dien_thoai=? WHERE id=?',(data.ho_ten,str(data.ngay_sinh) if data.ngay_sinh else None,data.gioi_tinh,str(data.email) if data.email else None,data.so_dien_thoai,user_id))
    return {'success':True}
@router.delete('/{user_id}')
def delete_user(user_id:int):
    if not fetch_one('SELECT id FROM Users WHERE id=?',(user_id,)): raise HTTPException(404,'Không tìm thấy người dùng')
    update('DELETE FROM Users WHERE id=?',(user_id,)); return {'success':True}
@router.put('/{user_id}/password')
def password(user_id:int,data:PasswordUpdate):
    u=fetch_one('SELECT password FROM Users WHERE id=?',(user_id,))
    if not u or not verify_password(data.old_password,u['password']): return {'success':False,'message':'Mật khẩu hiện tại không đúng'}
    if not strong_password(data.new_password): return {'success':False,'message':'Mật khẩu mới chưa đủ mạnh'}
    update('UPDATE Users SET password=? WHERE id=?',(hash_password(data.new_password),user_id)); return {'success':True}
