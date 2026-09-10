"""User management page."""

import streamlit as st

from frontend.api import request


ROLE_NAMES = {0: "Quản trị viên", 1: "Giáo viên"}


@st.dialog("Chỉnh sửa người dùng", width="medium")
def edit_user_dialog(user: dict) -> None:
    """Edit user profile fields in a modal dialog."""
    with st.form(f"edit_user_form_{user['id']}"):
        full_name = st.text_input("Họ tên", user.get("ho_ten") or "")
        birthday = st.text_input("Ngày sinh", user.get("ngay_sinh") or "")
        gender = st.selectbox("Giới tính", ["Nam", "Nữ", "Khác"], index=["Nam", "Nữ", "Khác"].index(user.get("gioi_tinh") or "Khác"))
        email = st.text_input("Email", user.get("email") or "")
        phone = st.text_input("Số điện thoại", user.get("so_dien_thoai") or "")
        submitted = st.form_submit_button("Lưu thay đổi", type="primary", use_container_width=True)

    if submitted:
        try:
            request(
                "PUT",
                f"/api/users/{user['id']}",
                json={
                    "ho_ten": full_name,
                    "ngay_sinh": birthday or None,
                    "gioi_tinh": gender,
                    "email": email or None,
                    "so_dien_thoai": phone or None,
                },
            )
            st.success("Đã cập nhật người dùng.")
            st.rerun()
        except Exception as exc:
            st.error(str(exc))


def delete_user(user: dict) -> None:
    try:
        request("DELETE", f"/api/users/{user['id']}")
        st.success("Đã xóa người dùng.")
        st.rerun()
    except Exception as exc:
        st.error(str(exc))


def show_users() -> None:
    st.title("Quản lý người dùng")
    st.caption("Quản lý tài khoản và phân quyền người dùng.")

    try:
        users = request("GET", "/api/users")
    except Exception as exc:
        st.error(str(exc))
        return

    if not users:
        st.info("Chưa có người dùng.")
        return

    current_user_id = st.session_state.get("user_id")
    for user in users:
        with st.container(border=True):
            left, right = st.columns([5, 2])
            with left:
                st.subheader(user["ho_ten"])
                st.caption(f"@{user['ten_dang_nhap']}")
                st.write(f"**Vai trò:** {ROLE_NAMES.get(user['role'], 'Khác')}")
                st.write(f"**Email:** {user.get('email') or '-'}")
                st.write(f"**Số điện thoại:** {user.get('so_dien_thoai') or '-'}")
            with right:
                if user["id"] == current_user_id:
                    st.caption("Tài khoản hiện tại")
                else:
                    if st.button("Chỉnh sửa", key=f"edit_user_{user['id']}", use_container_width=True):
                        edit_user_dialog(user)
                    if st.button("Xóa", key=f"delete_user_{user['id']}", use_container_width=True):
                        delete_user(user)
