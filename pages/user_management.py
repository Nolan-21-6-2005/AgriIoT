import streamlit as st
import pandas as pd
from streamlit_extras.great_tables import *
from database import get_users
def show_user_management():
    try:
        from great_tables import GT
        # Ví dụ dữ liệu lấy từ SQLite
    
        users = get_users()
    
        users["role"] = users["role"].map({
            0: "Quản trị viên",
            1: "Giáo viên"
        })

        # Đổi tên cột để hiển thị đẹp hơn
        users = users.rename(columns={
            "id": "ID",
            "ten_dang_nhap": "Tên đăng nhập",
            "role": "Vai trò",
            "ho_ten": "Họ tên",
            "ngay_sinh": "Ngày sinh",
            "gioi_tinh": "Giới tính",
            "email": "Email"
        })
    
        table = (
            GT(users)
            .tab_header(
                title="Danh sách người dùng",
                subtitle=f"Tổng số: {len(users)} người dùng"
            )
        )
        great_tables(table, width="stretch")
    except ImportError:
        st.warning("This example requires the `great_tables` package. Install it with `pip install great-tables`.")
