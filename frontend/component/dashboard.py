import streamlit as st
from component.admin_topbar import get_selection
from view_weather import show_weather
from user_management import show_user_management

def show_user_dashboard():
    col1, col2 = st.columns([1, 5])
    with col1:
        selection = get_selection()
    with col2:
        if selected == "Thống kê":
            show_weather()
        elif selected == "Thiết bị":
            show_user_management()
        #elif selected == "Setting":
            #show_settings()
    return selection

def show_admin_dashboard():
    col1, col2 = st.columns([1, 5])
    with col1:
        selection = get_selection()
    with col2:
        if selected == "Thống kê":
            show_weather()
        elif selected == "Thiết bị":
            show_user_management()
        #elif selected == "Setting":
            #show_settings()
    return selection
