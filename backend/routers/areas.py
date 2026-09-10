"""CRUD API for garden areas/zones."""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from backend.database import execute, fetch_all, fetch_one, update

router = APIRouter()


class AreaCreate(BaseModel):
    ten_khu_vuc: str
    mo_ta: str = ""
    dien_tich: float = Field(default=0, ge=0)
    trang_thai: str = "Đang hoạt động"


class AreaUpdate(AreaCreate):
    pass


@router.get("")
def list_areas():
    return fetch_all(
        """SELECT id, ten_khu_vuc, mo_ta, dien_tich, trang_thai, created_at
        FROM Areas WHERE is_deleted=0 ORDER BY id"""
    )


@router.get("/{area_id}")
def get_area(area_id: int):
    area = fetch_one("SELECT * FROM Areas WHERE id=? AND is_deleted=0", (area_id,))
    if not area:
        raise HTTPException(404, "Không tìm thấy khu vực")
    return area


@router.post("")
def create_area(data: AreaCreate):
    try:
        area_id = execute(
            """INSERT INTO Areas (ten_khu_vuc, mo_ta, dien_tich, trang_thai, is_deleted)
            VALUES (?,?,?,?,0)""",
            (data.ten_khu_vuc, data.mo_ta, data.dien_tich, data.trang_thai),
        )
        return {"success": True, "id": area_id}
    except Exception as exc:
        raise HTTPException(400, str(exc)) from exc


@router.put("/{area_id}")
def update_area(area_id: int, data: AreaUpdate):
    if not fetch_one("SELECT id FROM Areas WHERE id=? AND is_deleted=0", (area_id,)):
        raise HTTPException(404, "Không tìm thấy khu vực")

    update(
        """UPDATE Areas SET ten_khu_vuc=?, mo_ta=?, dien_tich=?, trang_thai=?
        WHERE id=?""",
        (data.ten_khu_vuc, data.mo_ta, data.dien_tich, data.trang_thai, area_id),
    )
    return {"success": True}


@router.delete("/{area_id}")
def delete_area(area_id: int):
    if not fetch_one("SELECT id FROM Areas WHERE id=? AND is_deleted=0", (area_id,)):
        raise HTTPException(404, "Không tìm thấy khu vực")
    update("UPDATE Areas SET is_deleted=1 WHERE id=?", (area_id,))
    return {"success": True}
