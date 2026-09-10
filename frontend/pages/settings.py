import streamlit as st
from frontend.api import request
def show_settings():
    st.title('Cài đặt')
    st.caption('Bảo mật tài khoản và tùy chọn ứng dụng.')
    a,b=st.tabs(['Bảo mật','Ứng dụng'])
    with a:
        with st.form('password'):
            old=st.text_input('Mật khẩu hiện tại',type='password'); new=st.text_input('Mật khẩu mới',type='password')
            if st.form_submit_button('Đổi mật khẩu'):
                r=request('PUT',f"/api/users/{st.session_state.user_id}/password",json={'old_password':old,'new_password':new}); st.success('Đã đổi mật khẩu') if r.get('success') else st.error(r.get('message'))
    with b: st.info('Địa điểm thời tiết cố định: Hà Nội. Forecast UI làm mới mỗi 60 giây.')
