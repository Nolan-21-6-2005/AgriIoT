from datetime import date
import streamlit as st
from frontend.api import request

def show_login():
    st.title('🌱 AgrIoT'); st.subheader('Đăng nhập')
    with st.form('login'):
        u=st.text_input('Tên đăng nhập'); p=st.text_input('Mật khẩu',type='password'); ok=st.form_submit_button('Đăng nhập',use_container_width=True,type='primary')
    if ok:
        try:
            d=request('POST','/api/auth/login',json={'ten_dang_nhap':u,'password':p})
            if d.get('success'):
                st.session_state.update(user_id=d['user_id'],username=d['ten_dang_nhap'],role=d['role'],page='dashboard'); st.rerun()
            st.error(d.get('message','Đăng nhập thất bại'))
        except Exception as e: st.error(f'Backend không khả dụng: {e}')
    if st.button('Chưa có tài khoản? Đăng ký',use_container_width=True): st.session_state.page='signup'; st.rerun()

def show_signup():
    st.title('🌱 AgrIoT'); st.subheader('Đăng ký')
    with st.form('signup'):
        c1,c2=st.columns(2)
        with c1:
            u=st.text_input('Tên đăng nhập'); name=st.text_input('Họ và tên'); gender=st.selectbox('Giới tính',['Nam','Nữ','Khác']); p=st.text_input('Mật khẩu',type='password')
        with c2:
            email=st.text_input('Email'); phone=st.text_input('Số điện thoại'); birthday=st.date_input('Ngày sinh',date(2000,1,1)); cp=st.text_input('Nhập lại mật khẩu',type='password')
        ok=st.form_submit_button('Đăng ký',use_container_width=True,type='primary')
    if ok:
        if p!=cp: st.error('Mật khẩu không khớp'); return
        try:
            d=request('POST','/api/auth/signup',json={'ten_dang_nhap':u,'password':p,'ho_ten':name,'ngay_sinh':str(birthday),'gioi_tinh':gender,'email':email or None,'so_dien_thoai':phone or None})
            if d.get('success'): st.success('Đăng ký thành công'); st.session_state.page='login'; st.rerun()
            else: st.error(d.get('message','Đăng ký thất bại'))
        except Exception as e: st.error(str(e))
    if st.button('Quay lại đăng nhập',use_container_width=True): st.session_state.page='login'; st.rerun()
