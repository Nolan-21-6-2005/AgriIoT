from meteostat import Point, hourly
from datetime import datetime

location = Point(21.0285, 105.8542)

data = hourly(
    location,
    start=datetime(2025, 1, 1),
    end=datetime(2025, 12, 31)
)

df = data.fetch()

print(type(df))
print(df)

if df is not None:
    df.to_csv("weather_data.csv")
    print(df.head())
else:
    print("Không lấy được dữ liệu từ Meteostat.")
