"""Garden map and irrigation decision workspace."""

import streamlit as st
import plotly.graph_objects as go

from frontend.api import request


ZONE_BOUNDS = {
    "Khu A": (8, 45, 8, 42),
    "Khu B": (52, 89, 8, 42),
    "Khu C": (8, 89, 55, 92),
}


def _plants():
    """Fixed simulated crop positions used only for the visual garden map."""
    rows = [
        (15, 25), (24, 25), (33, 25), (62, 25), (71, 25), (80, 25),
        (15, 36), (24, 36), (33, 36), (62, 36), (71, 36), (80, 36),
        (18, 70), (28, 70), (38, 70), (50, 70), (60, 70), (70, 70),
        (18, 82), (28, 82), (38, 82), (50, 82), (60, 82), (70, 82),
    ]
    return rows


def _build_figure(devices):
    fig = go.Figure()
    fig.add_shape(type="rect", x0=2, y0=2, x1=98, y1=98, line=dict(color="#527a3b", width=2), fillcolor="#dfead7", layer="below")

    zone_styles = {"Khu A": "#edf5e7", "Khu B": "#eaf3e4", "Khu C": "#f0f6ea"}
    for name, (x0, x1, y0, y1) in ZONE_BOUNDS.items():
        fig.add_shape(type="rect", x0=x0, y0=y0, x1=x1, y1=y1, line=dict(color="#91ad7b", width=1.5), fillcolor=zone_styles[name], layer="below")
        fig.add_annotation(x=x0 + 2, y=y1 - 2, text=name, showarrow=False, xanchor="left", yanchor="top", font=dict(size=12, color="#4c6540"))

    plants = _plants()
    fig.add_trace(go.Scatter(x=[p[0] for p in plants], y=[p[1] for p in plants], mode="markers", marker=dict(size=14, symbol="circle", color="#5d9b4d", line=dict(width=1, color="#3e7133")), hovertemplate="Cây trồng<extra></extra>", name="Cây trồng"))

    pumps_x, pumps_y, pumps_text = [], [], []
    sensors_x, sensors_y, sensors_text = [], [], []
    for device in devices:
        x = float(device.get("vi_tri_x") or 50)
        y = float(device.get("vi_tri_y") or 50)
        status = "Online" if device.get("trang_thai") else "Offline"
        hover = f"<b>{device['ten_thiet_bi']}</b><br>Loại: {device['loai_thiet_bi']}<br>Khu vực: {device.get('vi_tri', '-')}<br>Trạng thái: {status}<br>Tọa độ: ({x:.0f}, {y:.0f})<extra></extra>"
        if "bơm" in device["loai_thiet_bi"].lower() or "pump" in device["loai_thiet_bi"].lower():
            pumps_x.append(x); pumps_y.append(y); pumps_text.append(hover)
        else:
            sensors_x.append(x); sensors_y.append(y); sensors_text.append(hover)

    if pumps_x:
        fig.add_trace(go.Scatter(x=pumps_x, y=pumps_y, mode="markers+text", text=["💧"] * len(pumps_x), textposition="middle center", marker=dict(size=38, color="#ffffff", line=dict(width=3, color="#2f80ed")), hovertemplate=pumps_text, name="Máy bơm"))
        for x, y in zip(pumps_x, pumps_y):
            fig.add_shape(type="circle", x0=x - 10, y0=y - 10, x1=x + 10, y1=y + 10, line=dict(color="#5aa9e6", width=1, dash="dot"), fillcolor="rgba(80,160,255,0.08)", layer="below")

    if sensors_x:
        fig.add_trace(go.Scatter(x=sensors_x, y=sensors_y, mode="markers+text", text=["●"] * len(sensors_x), textposition="middle center", marker=dict(size=28, color="#ffffff", line=dict(width=3, color="#f2b134")), hovertemplate=sensors_text, name="Cảm biến"))

    fig.update_xaxes(range=[0, 100], visible=False, fixedrange=True)
    fig.update_yaxes(range=[0, 100], visible=False, fixedrange=True, scaleanchor="x", scaleratio=1)
    fig.update_layout(height=570, margin=dict(l=10, r=10, t=10, b=10), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", legend=dict(orientation="h", y=1.02, x=0, bgcolor="rgba(255,255,255,0.7)"), hoverlabel=dict(bgcolor="white"))
    return fig


def _render_irrigation_simulator(devices):
    with st.container(border=True, key="irrigation_simulator_card"):
        st.markdown("#### Mô phỏng tưới")
        st.caption("Chọn máy bơm và độ ẩm đất để mô phỏng một lần tưới.")
        pumps = [d for d in devices if "bơm" in d["loai_thiet_bi"].lower() or "pump" in d["loai_thiet_bi"].lower()]
        if not pumps:
            st.info("Chưa có máy bơm để mô phỏng tưới.")
            return

        pump_names = [d["ten_thiet_bi"] for d in pumps]
        pump_name = st.selectbox("Máy bơm", pump_names, key="map_pump")
        pump = next(d for d in pumps if d["ten_thiet_bi"] == pump_name)
        soil = st.slider("Độ ẩm đất (%)", 0, 100, 28, key="map_sim_soil")

        if st.button("Chạy lệnh tưới", type="primary", icon=":material/water_drop:", key="map_execute_irrigation"):
            try:
                result = request("POST", "/api/irrigation/execute", json={"soil_moisture": soil, "device_id": pump["id"]})
                if result.get("success"):
                    st.success(f"Đã mô phỏng tưới {result.get('duration_seconds', 0)} giây.")
                else:
                    st.warning(result.get("message", "Không thể tưới."))
            except Exception as exc:
                st.error(str(exc))

def show_garden_map():
    st.subheader("Bản đồ khu vườn")
    st.caption("Bản đồ chỉ hiển thị trạng thái và vị trí giả lập. Quản lý dữ liệu nằm trong tab riêng.")

    try:
        devices = request("GET", "/api/devices/map")
    except Exception as exc:
        st.error(f"Không thể tải bản đồ: {exc}")
        return

    left, right = st.columns([3.2, 1], gap="large")
    with left:
        with st.container(border=True):
            st.plotly_chart(_build_figure(devices), use_container_width=True, config={"displayModeBar": False})

    with right:
        _render_irrigation_simulator(devices)
