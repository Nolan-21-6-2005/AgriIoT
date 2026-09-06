import streamlit as st
from frontend.component.auth import show_sign_in, show_sign_up
from frontend.component.dashboard import show_user_dashboard, show_admin_dashboard

st.set_page_config(
    layout="wide",
    initial_sidebar_state="collapsed"
)

if 'role' not in st.session_state:
    st.session_state['role'] = ''

if st.session_state['page'] == 'login':
    show_sign_in()