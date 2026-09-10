"""Common icon-only action buttons used by management cards."""

import streamlit as st


def edit_button(key: str) -> bool:
    return st.button(" ", icon=":material/edit:", help="Chỉnh sửa", key=key, width="content")


def delete_button(key: str) -> bool:
    return st.button(" ", icon=":material/delete:", help="Xóa", key=key, width="content")


def add_button(key: str, help_text: str = "Thêm mới") -> bool:
    return st.button(" ", icon=":material/add:", help=help_text, key=key, type="primary", width="content")
