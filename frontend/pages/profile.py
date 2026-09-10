import streamlit as st
from frontend.api import request
def show_profile():
    st.title('Hồ sơ cá nhân')
    st.caption('Thông tin tài khoản và thông tin liên hệ.')
    try: u=request('GET',f"/api/users/{st.session_state.user_id}")
    except Exception as e: st.error(str(e)); return
    with st.form('profile'):
        name=st.text_input('Họ tên',u['ho_ten']); birthday=st.text_input('Ngày sinh',u['ngay_sinh'] or ''); gender=st.selectbox('Giới tính',['Nam','Nữ','Khác'],index=['Nam','Nữ','Khác'].index(u['gioi_tinh']) if u['gioi_tinh'] in ['Nam','Nữ','Khác'] else 0); email=st.text_input('Email',u['email'] or ''); phone=st.text_input('Số điện thoại',u['so_dien_thoai'] or '')
        if st.form_submit_button('Lưu thay đổi'): request('PUT',f"/api/users/{u['id']}",json={'ho_ten':name,'ngay_sinh':birthday or None,'gioi_tinh':gender,'email':email or None,'so_dien_thoai':phone or None}); st.success('Đã cập nhật')
