import pandas as pd
import streamlit as st
from frontend.api import request


def show_logs():
    st.title("Nhật ký tưới")
    st.caption("Lịch sử các lần tưới trong khu vườn.")
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
    })
    if "Kết quả" in df:
        df["Kết quả"] = df["Kết quả"].map({1: "Thành công", 0: "Thất bại"}).fillna("Không rõ")
    st.dataframe(df, use_container_width=True, hide_index=True)
