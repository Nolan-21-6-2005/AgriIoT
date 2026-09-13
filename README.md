# AgrIoT

Bài tập lớn: hệ thống quản lý và hỗ trợ quyết định tưới tiêu nông nghiệp.

## Chức năng

- Đăng nhập / đăng ký.
- Dashboard thời tiết Hà Nội.
- 6 card forecast theo 6 giờ quanh thời điểm hiện tại; icon lớn bằng HTML/CSS.
- Dữ liệu thời tiết lấy qua FastAPI từ Open-Meteo; không có geocoding vì phạm vi chỉ là Hà Nội.
- Quản lý thiết bị: xem, thêm, sửa, xóa mềm; trạng thái online/offline mô phỏng.
- Thời gian tưới lưu bằng giây (`duration_seconds`).
- AI quyết định tưới: Random Forest nếu có `ai_model/irrigation_rf.joblib`; nếu chưa có model thì fallback mô phỏng được ghi rõ trên UI.
- Mô phỏng thực thi lệnh tưới và lưu `Irrigation_Logs`.
- Quản lý người dùng cho admin.
- Hồ sơ và đổi mật khẩu.

## Chạy

```bash
pip install -r requirements.txt
python -m utils.init_db
uvicorn backend_app:app --reload --port 8000
```

Terminal thứ hai:

```bash
streamlit run app.py
```

Tài khoản mẫu: `admin123/admin123`, `GV123/gv123`.

## Train AI

Dataset cần có các cột:

`temperature, humidity, rain, wind_speed, soil_moisture, irrigation`

Sau khi có dataset:

```bash
python -m ai.train data/training_dataset.csv
```

Model được lưu ở `ai_model/irrigation_rf.joblib`.

## Kiến trúc

```text
Streamlit
   │ HTTP
   ▼
FastAPI
   ├── Auth
   ├── Weather ── Open-Meteo
   ├── Users ──── SQLite
   ├── Devices ── SQLite
   └── Irrigation ── AI / Device
                       │
                       ▼
                 Irrigation_Logs
```

Thiết bị IoT là mô phỏng bằng database trong phiên bản bài tập lớn; không giả vờ là phần cứng thật.
