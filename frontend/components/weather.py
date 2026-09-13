"""Weather widgets used by the dashboard."""

import pandas as pd
import streamlit as st

from frontend.api import request


WEATHER = {
    0: ("☀️", "Trời quang"), 1: ("🌤️", "Khá quang"), 2: ("⛅", "Có mây"), 3: ("☁️", "Âm u"),
    45: ("🌫️", "Sương mù"), 48: ("🌫️", "Sương mù"), 51: ("🌦️", "Mưa phùn"), 53: ("🌦️", "Mưa phùn"),
    55: ("🌦️", "Mưa phùn"), 61: ("🌧️", "Mưa nhẹ"), 63: ("🌧️", "Mưa"), 65: ("🌧️", "Mưa lớn"),
    80: ("🌦️", "Mưa rào"), 81: ("🌦️", "Mưa rào"), 82: ("🌧️", "Mưa rào lớn"), 95: ("⛈️", "Dông"),
}


def _weather_hour_card(time_value, temperature, humidity, rain_prob, code) -> None:
    """Render one hourly forecast as a native Streamlit card."""
    icon, status = WEATHER.get(code, ("❓", "Không xác định"))
    hour = pd.Timestamp(time_value).strftime("%H:%M")

    with st.container(border=True, key=f"weather_hour_{hour}"):
        st.markdown(f"<div class='weather-hour-title'>{hour}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='weather-hour-icon'>{icon}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='weather-hour-status'>{status}</div>", unsafe_allow_html=True)
        metrics = st.columns(3, gap="small")
        metrics[0].markdown(f"<div class='weather-hour-value'>🌡️<br><b>{temperature}°</b></div>", unsafe_allow_html=True)
        metrics[1].markdown(f"<div class='weather-hour-value'>💧<br><b>{humidity}%</b></div>", unsafe_allow_html=True)
        metrics[2].markdown(f"<div class='weather-hour-value'>☔<br><b>{rain_prob}%</b></div>", unsafe_allow_html=True)


def _irrigation_progress_card() -> None:
    """Show the number of areas successfully irrigated today as a circular progress bar."""
    try:
        progress = request("GET", "/api/irrigation/daily-progress")
    except Exception as exc:
        st.error(f"Không tải được tiến độ tưới: {exc}")
        return

    completed = int(progress.get("completed", 0))
    required = int(progress.get("required", 0))
    percent = int(progress.get("percent", 0))
    degree = percent * 3.6

    st.markdown(
        f"""
        <div class="irrigation-progress-wrap">
            <div class="circle-progress" style="--progress-degree:{degree}deg;">
                <div class="circle-progress-inner">
                    <div class="circle-progress-value">{completed}/{required}</div>
                    <div class="circle-progress-label">khu vực</div>
                </div>
            </div>
            <div class="circle-progress-caption">
                <b>Tiến độ tưới hôm nay</b>
                <span>{percent}% hoàn thành yêu cầu</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


@st.fragment(run_every="60s")
def show_weather() -> None:
    """Render current weather, hourly cards, and the humidity/temperature chart."""
    try:
        data = request("GET", "/api/weather/forecast")
    except Exception as exc:
        st.error(f"Không lấy được thời tiết: {exc}")
        return

    current = data["current"]
    hourly = data["hourly_forecast"]

    st.subheader(f"Thời tiết — {data['location']}")
    metric_1, metric_2, metric_3 = st.columns(3)
    metric_1.metric("Nhiệt độ", f"{current['temperature_2m']} °C")
    metric_2.metric("Độ ẩm", f"{current['relative_humidity_2m']} %")
    metric_3.metric("Gió", f"{current['wind_speed_10m']} km/h")

    st.markdown("### Dự báo theo giờ")
    current_time = pd.Timestamp(current["time"])
    times = pd.to_datetime(hourly["time"])
    index = times.searchsorted(current_time, side="left")
    index = max(0, min(int(index), len(times) - 6))

    forecast_cols = st.columns(6, gap="small")
    for offset, col in enumerate(forecast_cols):
        item_index = index + offset
        with col:
            _weather_hour_card(
                times[item_index],
                hourly["temperature"][item_index],
                hourly["humidity"][item_index],
                hourly["rain_prob"][item_index],
                hourly["weather_code"][item_index],
            )

    chart_col, progress_col = st.columns([2, 1], gap="small")
    weather_df = pd.DataFrame(
        {
            "Thời gian": times,
            "Nhiệt độ (°C)": hourly["temperature"],
            "Độ ẩm không khí (%)": hourly["humidity"],
        }
    ).set_index("Thời gian")

    with chart_col:
        with st.container(border=True, key="weather_chart_card"):
            st.markdown("#### Nhiệt độ và độ ẩm không khí")
            st.line_chart(weather_df[["Nhiệt độ (°C)", "Độ ẩm không khí (%)"]])

    with progress_col:
        with st.container(border=True, key="irrigation_progress_card", height = 399):
            _irrigation_progress_card()
