from streamlit_option_menu import option_menu
from style_option_menu import OPTION_MENU_STYLES
import streamlit as st

def get_admin_selection():
    selected = option_menu(
            None, [
                "Thống kê", "Thiết bị", "Người dùng", "Cài đặt"
            ],
            icons = [
                'bar-chart', 'device', 'people', 'setting'
            ], 
            menu_icon="cast", 
            default_index=0,
            orientation="horizontal",
            styles = OPTION_MENU_STYLES
        )
    return selected
    
def get_user_selection():
    selected = option_menu(
            None, [
                "Thống kê báo cáo", "Quản lý thiết bị", "Hồ sơ cá nhân"
            ],
            icons = [
                'bar-chart', 'device', 'people'
            ], 
            menu_icon="cast", 
            default_index=0,
            orientation="horizontal",
            styles = OPTION_MENU_STYLES
        )
    return selected
