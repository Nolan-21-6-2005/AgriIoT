import streamlit as st
import pandas as pd
from streamlit_extras.great_tables import *
from streamlit_extras.metric_cards import *
from database import get_users
import requests
import pandas as pd

def show_weather():

    st.set_page_config(page_title="Weather Forecaster", layout="wide", page_icon="🌤️")
    st.title("🌤️ Weather Forecasting Dashboard")

    # 1. New Text Box Input Group
    col1, col2 = st.columns([10, 1], vertical_alignment="bottom")

    with col1: 
        st.subheader("Location Selection")
    with col2: 
        btn = st.button("Fetch Forecast", type="primary")
    city_input = st.text_input("Enter City Name", value="New York", placeholder="e.g. Paris, Tokyo") #

    BASE_URL = "http://127.0.0.1:8000"

    if btn:
        with st.spinner("Locating city and pulling weather metrics..."):
            try:
                # Step A: Convert City Name to Coordinates via FastAPI
                geo_response = requests.get(f"{BASE_URL}/geocode", params={"city_name": city_input})
                
                if geo_response.status_code == 200:
                    geo_data = geo_response.json()
                    lat = geo_data["latitude"]
                    lon = geo_data["longitude"]
                    resolved_location = f"{geo_data['city']}, {geo_data['country']}"
                    
                    # Step B: Pass resolved coords into original weather endpoint
                    weather_response = requests.get(f"{BASE_URL}/weather", params={"latitude": lat, "longitude": lon})
                    
                    if weather_response.status_code == 200:
                        weather_data = weather_response.json()
                        current = weather_data["current"]
                        hourly = weather_data["hourly_forecast"]
                        
                        # Renders resolved target metadata
                        st.success(f"📍 Showing weather data for: **{resolved_location}** (Lat: {lat}, Lon: {lon})")
                        
                        # 2. Display Metrics Dashboard
                        st.subheader("⚠️ Current Conditions")
                        col1, col2, col3 = st.columns(3)
                        col1.metric("Temperature", f"{current['temperature']} °C", border = True)
                        col2.metric("Wind Speed", f"{current['windspeed']} km/h", border = True)
                        col3.metric("Observation Time", f"{current['time']}", border = True)
                        
                        # 3. Trends Compiled
                        st.subheader("📅 7-Day Hourly Trend Analysis")
                        df = pd.DataFrame({
                            "Time": pd.to_datetime(hourly["time"]),
                            "Temperature (°C)": hourly["temperature"],
                            "Humidity (%)": hourly["humidity"],
                            "Rain Probability (%)": hourly["rain_prob"]
                        }).set_index("Time")
                         
                        st.line_chart(df[["Temperature (°C)", "Humidity (%)"]])
                        st.area_chart(df["Rain Probability (%)"])
                        
                    else:
                        st.error(f"Weather Engine Error: {weather_response.json().get('detail')}")
                else:
                    st.error(f"Geocoding Error: {geo_response.json().get('detail')}")
                    
            except requests.exceptions.ConnectionError:
                st.error("Could not reach backend. Please verify your FastAPI app configuration server terminal.")

    st.subheader("🌱 Irrigation")
    st.write("Soil Moisture")
    st.write("Irrigation Status")


def show_user_management():
    try:
        from great_tables import GT
        # Ví dụ dữ liệu lấy từ SQLite
    
        users = get_users()
    
        users["role"] = users["role"].map({
            0: "Quản trị viên",
            1: "Giáo viên"
        })

        # Đổi tên cột để hiển thị đẹp hơn
        users = users.rename(columns={
            "id": "ID",
            "ten_dang_nhap": "Tên đăng nhập",
            "role": "Vai trò",
            "ho_ten": "Họ tên",
            "ngay_sinh": "Ngày sinh",
            "gioi_tinh": "Giới tính",
            "email": "Email"
        })
    
        table = (
            GT(users)
            .tab_header(
                title="Danh sách người dùng",
                subtitle=f"Tổng số: {len(users)} người dùng"
            )
        )
        great_tables(table, width="stretch")
    except ImportError:
        st.warning("This example requires the `great_tables` package. Install it with `pip install great-tables`.")
