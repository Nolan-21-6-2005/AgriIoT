from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from backend.database import fetch_all, fetch_one, execute, update

router = APIRouter()


class DeviceCreate(BaseModel):
    ten_thiet_bi: str
    loai_thiet_bi: str
    vi_tri: str
    duration_seconds: int = Field(default=600, ge=0)
    max_duration_seconds: int = Field(default=1200, ge=0)
    vi_tri_x: float = Field(default=50, ge=0, le=100)
    vi_tri_y: float = Field(default=50, ge=0, le=100)


class DeviceUpdate(DeviceCreate):
    trang_thai: int = 0


class DevicePosition(BaseModel):
    x: float = Field(ge=0, le=100)
    y: float = Field(ge=0, le=100)


@router.get("")
def devices():
    return fetch_all(
        """SELECT id, ten_thiet_bi, loai_thiet_bi, trang_thai, is_deleted,
        vi_tri, duration_seconds, max_duration_seconds, last_seen,
        vi_tri_x, vi_tri_y, created_at
        FROM Devices WHERE is_deleted=0 ORDER BY id"""
    )


@router.get("/map")
def map_devices():
    return fetch_all(
        """SELECT id, ten_thiet_bi, loai_thiet_bi, trang_thai, vi_tri,
        duration_seconds, max_duration_seconds, last_seen, vi_tri_x, vi_tri_y
        FROM Devices WHERE is_deleted=0 ORDER BY id"""
    )


@router.put("/{device_id}/position")
def update_position(device_id: int, position: DevicePosition):
    if not fetch_one("SELECT id FROM Devices WHERE id=? AND is_deleted=0", (device_id,)):
        raise HTTPException(404, "Không tìm thấy thiết bị")
    update(
        "UPDATE Devices SET vi_tri_x=?, vi_tri_y=? WHERE id=?",
        (position.x, position.y, device_id),
    )
    return {"success": True, "device_id": device_id, "x": position.x, "y": position.y}


@router.get("/{device_id}")
def device(device_id: int):
    d = fetch_one("SELECT * FROM Devices WHERE id=? AND is_deleted=0", (device_id,))
    if not d:
        raise HTTPException(404, "Không tìm thấy thiết bị")
    return d


@router.post("")
def create(data: DeviceCreate):
    try:
        i = execute(
            """INSERT INTO Devices
            (ten_thiet_bi, loai_thiet_bi, trang_thai, is_deleted, vi_tri,
             duration_seconds, max_duration_seconds, vi_tri_x, vi_tri_y)
            VALUES (?,?,0,0,?,?,?,?,?)""",
            (
                data.ten_thiet_bi,
                data.loai_thiet_bi,
                data.vi_tri,
                data.duration_seconds,
                data.max_duration_seconds,
                data.vi_tri_x,
                data.vi_tri_y,
            ),
        )
        return {"success": True, "id": i}
    except Exception as e:
        raise HTTPException(400, str(e))


@router.put("/{device_id}")
def edit(device_id: int, data: DeviceUpdate):
    if not fetch_one("SELECT id FROM Devices WHERE id=? AND is_deleted=0", (device_id,)):
        raise HTTPException(404, "Không tìm thấy thiết bị")
    update(
        """UPDATE Devices SET ten_thiet_bi=?, loai_thiet_bi=?, vi_tri=?,
        trang_thai=?, duration_seconds=?, max_duration_seconds=?,
        vi_tri_x=?, vi_tri_y=? WHERE id=?""",
        (
            data.ten_thiet_bi,
            data.loai_thiet_bi,
            data.vi_tri,
            data.trang_thai,
            data.duration_seconds,
            data.max_duration_seconds,
            data.vi_tri_x,
            data.vi_tri_y,
            device_id,
        ),
    )
    return {"success": True}


@router.delete("/{device_id}")
def remove(device_id: int):
    if not fetch_one("SELECT id FROM Devices WHERE id=? AND is_deleted=0", (device_id,)):
        raise HTTPException(404, "Không tìm thấy thiết bị")
    update("UPDATE Devices SET is_deleted=1 WHERE id=?", (device_id,))
    return {"success": True}


@router.post("/{device_id}/heartbeat")
def heartbeat(device_id: int):
    update("UPDATE Devices SET trang_thai=1,last_seen=CURRENT_TIMESTAMP WHERE id=?", (device_id,))
    return {"success": True}
