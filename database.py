import sqlite3
import pandas as pd 

def get_users():
    user = pd.read_sql_query("""
        SELECT
            id,
            ten_dang_nhap,
            role,
            ho_ten,
            ngay_sinh,
            gioi_tinh,
            email,
            so_dien_thoai,
            created_at
        FROM Users
    """, conn)
    return user

def get_devices():
    device = pd.read_sql_query("""
        SELECT
            id,
            ten_dang_nhap,
            role,
            ho_ten,
            ngay_sinh,
            gioi_tinh,
            email,
            so_dien_thoai,
            created_at
        FROM Users
    """, conn)
    return device
    
