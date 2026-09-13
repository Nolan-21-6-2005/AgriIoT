import pandas as pd
import streamlit as st
import datetime
from frontend.api import request


def show_logs():
    st.title("Nhật ký tưới")
    st.caption("Lịch sử các lần tưới và quyết định của hệ thống.")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        source_filter = st.datetime_input(
            "Từ ngày",
            datetime.datetime(2025, 11, 19, 16, 45),
            key = "source_date"
        )
    with col2:
        destionation_filter = st.datetime_input(
            "Đến ngày",
            datetime.datetime(2025, 11, 19, 16, 45),
            key = "destination_date"
        )
    with col3:
        result = st.selectbox(
            "Kết quả",
            ("Thành công", "Thất bại")
        )
    with col4:
        st.button("Submit", key = "submit_button", type="primary")
    
    
    try:
        logs = request("GET", "/api/irrigation/logs")
    except Exception as e:
        st.error(str(e))
        return

    if not logs:
        st.info("Chưa có lịch sử tưới.")
        return

    df = pd.DataFrame(logs)
    df = df.rename(columns={
        "id": "ID",
        "ten_thiet_bi": "Thiết bị",
        "ngay_tuoi_cay": "Thời điểm",
        "thoi_gian_tuoi": "Thời gian (giây)",
        "do_am_dat": "Độ ẩm đất (%)",
        "trang_thai": "Kết quả",
        "ai_decision": "Quyết định hệ thống",
    })
    if "Kết quả" in df:
        df["Kết quả"] = df["Kết quả"].map({1: "Thành công", 0: "Thất bại"}).fillna("Không rõ")
    if "Quyết định hệ thống" in df:
        df["Quyết định hệ thống"] = df["Quyết định hệ thống"].map({1: "Tưới", 0: "Không tưới"}).fillna("Không rõ")
    st.dataframe(df, use_container_width=True, hide_index=True)
