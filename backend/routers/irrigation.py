from fastapi import APIRouter
from pydantic import BaseModel

from ai.predict import predict_irrigation
from backend.database import execute, fetch_all, fetch_one

router = APIRouter()


class IrrigationRequest(BaseModel):
    temperature: float
    humidity: float
    rain: float = 0
    wind_speed: float = 0
    soil_moisture: float
    device_id: int | None = None


@router.post("/predict")
def predict(data: IrrigationRequest):
    return predict_irrigation(data.model_dump())


@router.get("/logs")
def logs():
    return fetch_all(
        """SELECT l.*, d.ten_thiet_bi
        FROM Irrigation_Logs l JOIN Devices d ON d.id=l.device_id
        ORDER BY l.id DESC LIMIT 100"""
    )


@router.get("/unwatered-areas")
def unwatered_areas():
    """Return crop zones whose pump has not successfully watered today."""
    return fetch_all(
        """SELECT
            d.vi_tri AS khu_vuc,
            d.ten_thiet_bi AS may_bom,
            MAX(CASE WHEN date(l.ngay_tuoi_cay)=date('now','localtime') AND l.trang_thai=1
                     THEN l.ngay_tuoi_cay END) AS lan_tuoi_gan_nhat
        FROM Devices d
        LEFT JOIN Irrigation_Logs l ON l.device_id=d.id
        WHERE d.is_deleted=0 AND (d.loai_thiet_bi LIKE '%bơm%' OR d.loai_thiet_bi LIKE '%pump%')
        GROUP BY d.id, d.vi_tri, d.ten_thiet_bi
        ORDER BY d.id"""
    )


@router.get("/daily-progress")
def daily_progress():
    """Return today's irrigation completion against active garden areas."""
    row = fetch_one(
        """SELECT
            (SELECT COUNT(*) FROM Areas WHERE is_deleted=0 AND trang_thai='Đang hoạt động') AS required,
            COUNT(DISTINCT CASE
                WHEN date(l.ngay_tuoi_cay)=date('now','localtime')
                     AND l.trang_thai=1
                     AND a.id IS NOT NULL
                THEN a.id
            END) AS completed
        FROM Irrigation_Logs l
        JOIN Devices d ON d.id=l.device_id AND d.is_deleted=0
        LEFT JOIN Areas a ON a.ten_khu_vuc=d.vi_tri AND a.is_deleted=0
        WHERE l.trang_thai=1
        """
    ) or {"required": 0, "completed": 0}

    required = int(row.get("required") or 0)
    completed = min(int(row.get("completed") or 0), required)
    percent = round(completed / required * 100) if required else 0
    return {"completed": completed, "required": required, "percent": percent}


@router.post("/execute")
def execute_irrigation(data: IrrigationRequest):
    prediction = predict_irrigation(data.model_dump())
    if not prediction["irrigation"]:
        return {"success": True, "message": "AI không yêu cầu tưới", "prediction": prediction}

    pump = (
        fetch_one(
            "SELECT id,duration_seconds FROM Devices WHERE loai_thiet_bi LIKE '%bơm%' AND trang_thai=1 AND is_deleted=0 ORDER BY id LIMIT 1"
        )
        if data.device_id is None
        else fetch_one(
            "SELECT id,duration_seconds FROM Devices WHERE id=? AND trang_thai=1 AND is_deleted=0",
            (data.device_id,),
        )
    )
    if not pump:
        return {"success": False, "message": "Không có máy bơm online", "prediction": prediction}

    log_id = execute(
        """INSERT INTO Irrigation_Logs
        (device_id,thoi_gian_tuoi,do_am_dat,trang_thai,ai_decision)
        VALUES (?,?,?,?,1)""",
        (pump["id"], pump["duration_seconds"], data.soil_moisture, 1),
    )
    return {
        "success": True,
        "message": "Đã mô phỏng lệnh tưới",
        "log_id": log_id,
        "duration_seconds": pump["duration_seconds"],
        "prediction": prediction,
    }
