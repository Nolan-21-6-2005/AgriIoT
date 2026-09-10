"""Reusable device summary content."""

import streamlit as st
from frontend.components.layout import placeholder_space


def device_card(device: dict) -> None:
    """Render device information with stable vertical alignment."""
    left, middle, right = st.columns([2, 2, 1], vertical_alignment="top")
    left.subheader(device["ten_thiet_bi"])
    left.caption(device["loai_thiet_bi"])
    middle.write(f"Vị trí: {device['vi_tri']}")
    middle.write(f"Tưới mặc định: {device['duration_seconds']} giây")
    placeholder_space(2)
    if device["trang_thai"]:
        right.success("ONLINE")
    else:
        right.error("OFFLINE")
