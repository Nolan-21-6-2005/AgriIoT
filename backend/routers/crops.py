from datetime import date

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from backend.database import execute, fetch_all, fetch_one, update

router = APIRouter()


class CropCreate(BaseModel):
    ten_cay: str
    loai_cay: str
    khu_vuc: str
    ngay_trong: date | None = None
    trang_thai: str = "Đang sinh trưởng"


class CropUpdate(CropCreate):
    pass


@router.get("")
def list_crops():
    return fetch_all(
        """SELECT id, ten_cay, loai_cay, khu_vuc, ngay_trong, trang_thai, created_at
        FROM Crops WHERE is_deleted=0 ORDER BY id"""
    )


@router.get("/{crop_id}")
def get_crop(crop_id: int):
    crop = fetch_one("SELECT * FROM Crops WHERE id=? AND is_deleted=0", (crop_id,))
    if not crop:
        raise HTTPException(404, "Không tìm thấy cây trồng")
    return crop


@router.post("")
def create_crop(data: CropCreate):
    try:
        crop_id = execute(
            """INSERT INTO Crops (ten_cay, loai_cay, khu_vuc, ngay_trong, trang_thai, is_deleted)
            VALUES (?,?,?,?,?,0)""",
            (
                data.ten_cay,
                data.loai_cay,
                data.khu_vuc,
                str(data.ngay_trong) if data.ngay_trong else None,
                data.trang_thai,
            ),
        )
        return {"success": True, "id": crop_id}
    except Exception as exc:
        raise HTTPException(400, str(exc)) from exc


@router.put("/{crop_id}")
def update_crop(crop_id: int, data: CropUpdate):
    if not fetch_one("SELECT id FROM Crops WHERE id=? AND is_deleted=0", (crop_id,)):
        raise HTTPException(404, "Không tìm thấy cây trồng")

    update(
        """UPDATE Crops SET ten_cay=?, loai_cay=?, khu_vuc=?, ngay_trong=?, trang_thai=?
        WHERE id=?""",
        (
            data.ten_cay,
            data.loai_cay,
            data.khu_vuc,
            str(data.ngay_trong) if data.ngay_trong else None,
            data.trang_thai,
            crop_id,
        ),
    )
    return {"success": True}


@router.delete("/{crop_id}")
def delete_crop(crop_id: int):
    if not fetch_one("SELECT id FROM Crops WHERE id=? AND is_deleted=0", (crop_id,)):
        raise HTTPException(404, "Không tìm thấy cây trồng")
    update("UPDATE Crops SET is_deleted=1 WHERE id=?", (crop_id,))
    return {"success": True}
