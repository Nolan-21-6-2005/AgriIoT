"""Dashboard page."""

import streamlit as st

from frontend.api import request
from frontend.components.garden_map import _build_figure
from frontend.components.weather import show_weather
from frontend.components.layout import placeholder_space


def show_dashboard() -> None:
    st.title("AgrIoT Dashboard")
    st.caption("Tổng quan thiết bị và điều kiện thời tiết của khu vườn.")

    try:
        devices = request("GET", "/api/devices")
        pumps = [d for d in devices if "bơm" in d["loai_thiet_bi"].lower() or "pump" in d["loai_thiet_bi"].lower()]
        metric_1, metric_2, metric_3 = st.columns(3, vertical_alignment="top")
        metric_1.metric("Thiết bị", len(devices))
        online_count = sum(d["trang_thai"] for d in pumps)
        metric_2.metric("Bơm online", online_count)
        metric_3.metric("Bơm offline", len(pumps) - online_count)
    except Exception:
        pass

    show_weather()

    with st.container(border=True, key = "garden_overview"):
        st.subheader("Tổng quan khu vườn")
        try:
            map_devices = request("GET", "/api/devices/map")
            st.plotly_chart(_build_figure(map_devices), width='content', config={"displayModeBar": False})
        except Exception as exc:
            st.error(f"Không tải được tổng quan khu vườn: {exc}")
