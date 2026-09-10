"""Garden workspace: map, master-data management and crop/device data."""

import streamlit as st

from frontend.components.garden_map import show_garden_map
from frontend.pages.area_management import show_area_management


def show_garden() -> None:
    st.title("Bản đồ khu vườn")
    st.caption("Theo dõi khu vườn và quản lý toàn bộ dữ liệu liên quan đến khu vực.")

    map_tab, management_tab = st.tabs(["Bản đồ", "Quản lý dữ liệu"])
    with map_tab:
        show_garden_map()
    with management_tab:
        show_area_management()
