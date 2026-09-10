import streamlit as st
from streamlit_option_menu import option_menu

from frontend.auth import show_login, show_signup
from frontend.pages.dashboard import show_dashboard
from frontend.pages.users import show_users
from frontend.pages.profile import show_profile
from frontend.pages.settings import show_settings
from frontend.pages.garden import show_garden
from frontend.pages.logs import show_logs
from frontend.style import apply_styles

st.set_page_config(
    page_title="AgrIoT",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded",
)
apply_styles()

st.session_state.setdefault("page", "login")
st.session_state.setdefault("role", None)
st.session_state.setdefault("user_id", None)
st.session_state.setdefault("username", None)

if st.session_state.page == "login":
    show_login()
elif st.session_state.page == "signup":
    show_signup()
else:
    pages = {
        "Dashboard": show_dashboard,
        "Bản đồ": show_garden,
        "Nhật ký": show_logs,
        "Hồ sơ": show_profile,
        "Cài đặt": show_settings,
    }
    if st.session_state.role == 0:
        pages["Người dùng"] = show_users

    icon_map = {
        "Dashboard": "speedometer2",
        "Bản đồ": "map",
        "Nhật ký": "journal-text",
        "Người dùng": "people",
        "Hồ sơ": "person",
        "Cài đặt": "gear",
    }

    with st.sidebar:
        st.markdown("### 🌱 AgrIoT")
        st.caption("Quản lý sản xuất nông nghiệp")

        selected = option_menu(
            None,
            list(pages.keys()),
            icons=[icon_map[name] for name in pages],
            default_index=0,
            orientation="vertical",
            styles={
                "container": {
                    "padding": "0.35rem 0",
                    "margin": "0",
                    "background-color": "transparent",
                },
                "icon": {
                    "font-size": "23px",
                    "margin-right": "10px",
                },
                "nav-link": {
                    "font-size": "13px",
                    "font-weight": "550",
                    "text-align": "left",
                    "margin": "3px 0",
                    "padding": "10px 12px",
                    "border-radius": "0.55rem",
                    "--hover-color": "#EEF5EC",
                },
                "nav-link-selected": {
                    "background-color": "#2E7D32",
                    "color": "#FFFFFF",
                },
            },
        )

    top_left, top_right = st.columns([8, 1])
    with top_left:
        st.caption(f"Đăng nhập: **{st.session_state.username}**")
    with top_right:
        if st.button("Đăng xuất", use_container_width=True):
            st.session_state.clear()
            st.session_state.page = "login"
            st.rerun()

    pages[selected]()
