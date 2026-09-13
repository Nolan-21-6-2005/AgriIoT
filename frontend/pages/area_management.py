"""Management workspace for areas, crops and devices."""

from datetime import date

import streamlit as st

from frontend.api import request
from frontend.components.action_buttons import add_button, delete_button, edit_button
from frontend.components.device_card import device_card
from frontend.components.pagination import paginate_items


AREA_STATUS = ["Đang hoạt động", "Tạm dừng", "Đã đóng"]
CROP_STATUS = ["Đang sinh trưởng", "Sắp thu hoạch", "Đã thu hoạch", "Ngừng theo dõi"]


@st.dialog("Thêm khu vực", width="medium")
def add_area_dialog() -> None:
    with st.form("add_area_form"):
        name = st.text_input("Tên khu vực")
        description = st.text_area("Mô tả")
        area_size = st.number_input("Diện tích (m²)", min_value=0.0, value=100.0, step=10.0)
        status = st.selectbox("Trạng thái", AREA_STATUS)
        if st.form_submit_button("Lưu", type="primary", width="stretch"):
            try:
                request("POST", "/api/areas", json={"ten_khu_vuc": name, "mo_ta": description, "dien_tich": area_size, "trang_thai": status})
                st.rerun()
            except Exception as exc:
                st.error(str(exc))


@st.dialog("Chỉnh sửa khu vực", width="medium")
def edit_area_dialog(area: dict) -> None:
    with st.form(f"edit_area_{area['id']}"):
        name = st.text_input("Tên khu vực", area["ten_khu_vuc"])
        description = st.text_area("Mô tả", area.get("mo_ta") or "")
        area_size = st.number_input("Diện tích (m²)", min_value=0.0, value=float(area.get("dien_tich") or 0), step=10.0)
        current = area.get("trang_thai") or AREA_STATUS[0]
        status = st.selectbox("Trạng thái", AREA_STATUS, index=AREA_STATUS.index(current) if current in AREA_STATUS else 0)
        if st.form_submit_button("Lưu thay đổi", type="primary", width="stretch"):
            try:
                request("PUT", f"/api/areas/{area['id']}", json={"ten_khu_vuc": name, "mo_ta": description, "dien_tich": area_size, "trang_thai": status})
                st.rerun()
            except Exception as exc:
                st.error(str(exc))


@st.dialog("Thêm cây trồng", width="medium")
def add_crop_dialog() -> None:
    areas = request("GET", "/api/areas")
    area_names = [a["ten_khu_vuc"] for a in areas] or [""]
    with st.form("add_crop_form"):
        name = st.text_input("Tên cây")
        crop_type = st.text_input("Loại cây")
        area = st.selectbox("Khu vực", area_names)
        planting_date = st.date_input("Ngày trồng", date.today())
        status = st.selectbox("Trạng thái", CROP_STATUS)
        if st.form_submit_button("Lưu", type="primary", width="stretch"):
            try:
                request("POST", "/api/crops", json={"ten_cay": name, "loai_cay": crop_type, "khu_vuc": area, "ngay_trong": str(planting_date), "trang_thai": status})
                st.rerun()
            except Exception as exc:
                st.error(str(exc))


@st.dialog("Chỉnh sửa cây trồng", width="medium")
def edit_crop_dialog(crop: dict) -> None:
    areas = request("GET", "/api/areas")
    area_names = [a["ten_khu_vuc"] for a in areas] or [crop.get("khu_vuc", "")]
    current_area = crop.get("khu_vuc", area_names[0])
    if current_area not in area_names:
        area_names.append(current_area)
    current_status = crop.get("trang_thai") or CROP_STATUS[0]
    with st.form(f"edit_crop_{crop['id']}"):
        name = st.text_input("Tên cây", crop["ten_cay"])
        crop_type = st.text_input("Loại cây", crop["loai_cay"])
        area = st.selectbox("Khu vực", area_names, index=area_names.index(current_area))
        planting_date = st.date_input("Ngày trồng", date.fromisoformat(crop["ngay_trong"]) if crop.get("ngay_trong") else date.today())
        status = st.selectbox("Trạng thái", CROP_STATUS, index=CROP_STATUS.index(current_status) if current_status in CROP_STATUS else 0)
        if st.form_submit_button("Lưu thay đổi", type="primary", width="stretch"):
            try:
                request("PUT", f"/api/crops/{crop['id']}", json={"ten_cay": name, "loai_cay": crop_type, "khu_vuc": area, "ngay_trong": str(planting_date), "trang_thai": status})
                st.rerun()
            except Exception as exc:
                st.error(str(exc))


@st.dialog("Thêm thiết bị", width="medium")
def add_device_dialog() -> None:
    areas = request("GET", "/api/areas")
    area_names = [a["ten_khu_vuc"] for a in areas] or [""]
    with st.form("add_device_form"):
        name = st.text_input("Tên thiết bị")
        device_type = st.text_input("Loại thiết bị")
        location = st.selectbox("Khu vực", area_names)
        duration = st.number_input("Thời gian tưới mặc định (giây)", 0, 3600, 600)
        if st.form_submit_button("Lưu", type="primary", width="stretch"):
            try:
                request("POST", "/api/devices", json={"ten_thiet_bi": name, "loai_thiet_bi": device_type, "vi_tri": location, "duration_seconds": duration, "max_duration_seconds": max(duration, 1200)})
                st.rerun()
            except Exception as exc:
                st.error(str(exc))


@st.dialog("Chỉnh sửa thiết bị", width="medium")
def edit_device_dialog(device: dict) -> None:
    areas = request("GET", "/api/areas")
    area_names = [a["ten_khu_vuc"] for a in areas] or [device.get("vi_tri", "")]
    current_area = device.get("vi_tri", area_names[0])
    if current_area not in area_names:
        area_names.append(current_area)
    with st.form(f"edit_device_{device['id']}"):
        name = st.text_input("Tên thiết bị", device["ten_thiet_bi"])
        device_type = st.text_input("Loại thiết bị", device["loai_thiet_bi"])
        location = st.selectbox("Khu vực", area_names, index=area_names.index(current_area))
        duration = st.number_input("Thời gian tưới mặc định (giây)", 0, 3600, int(device.get("duration_seconds") or 0))
        online = st.checkbox("Thiết bị đang online", bool(device.get("trang_thai")))
        if st.form_submit_button("Lưu thay đổi", type="primary", width="stretch"):
            try:
                request("PUT", f"/api/devices/{device['id']}", json={"ten_thiet_bi": name, "loai_thiet_bi": device_type, "vi_tri": location, "trang_thai": int(online), "duration_seconds": duration, "max_duration_seconds": max(duration, 1200), "vi_tri_x": device.get("vi_tri_x", 50), "vi_tri_y": device.get("vi_tri_y", 50)})
                st.rerun()
            except Exception as exc:
                st.error(str(exc))


def _delete(path: str, success_message: str) -> None:
    try:
        request("DELETE", path)
        st.rerun()
    except Exception as exc:
        st.error(f"{success_message}: {exc}")


def _management_card_grid(items: list[dict], kind: str) -> None:
    """Render master-data records as a responsive three-column card grid."""
    if not items:
        st.info("Chưa có dữ liệu.")
        return

    columns = st.columns(3, gap="medium")
    for index, item in enumerate(items):
        with columns[index % 3]:
            with st.container(border=True, key=f"{kind}_card_{item['id']}"):
                if kind == "area":
                    st.markdown(f"### {item['ten_khu_vuc']}")
                    st.caption(item.get("mo_ta") or "Không có mô tả")
                    st.write(f"Diện tích: {item.get('dien_tich', 0):g} m²")
                    st.write(f"Trạng thái: {item.get('trang_thai', '-')}")
                    st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)
                    action_cols = st.columns(2, gap="small")
                    with action_cols[0]:
                        if edit_button(f"edit_area_{item['id']}"):
                            edit_area_dialog(item)
                    with action_cols[1]:
                        if delete_button(f"delete_area_{item['id']}"):
                            _delete(f"/api/areas/{item['id']}", "Không thể xóa khu vực")

                elif kind == "crop":
                    st.markdown(f"### {item['ten_cay']}")
                    st.caption(item.get("loai_cay") or "Chưa xác định loại cây")
                    st.write(f"Khu vực: {item.get('khu_vuc') or '-'}")
                    st.write(f"Ngày trồng: {item.get('ngay_trong') or '-'}")
                    st.write(f"Trạng thái: {item.get('trang_thai') or '-'}")
                    st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)
                    action_cols = st.columns(2, gap="small")
                    with action_cols[0]:
                        if edit_button(f"edit_crop_{item['id']}"):
                            edit_crop_dialog(item)
                    with action_cols[1]:
                        if delete_button(f"delete_crop_{item['id']}"):
                            _delete(f"/api/crops/{item['id']}", "Không thể xóa cây trồng")

                else:
                    st.markdown(f"### {item['ten_thiet_bi']}")
                    device_card(item)
                    st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)
                    action_cols = st.columns(2, gap="small")
                    with action_cols[0]:
                        if edit_button(f"edit_device_{item['id']}"):
                            edit_device_dialog(item)
                    with action_cols[1]:
                        if delete_button(f"delete_device_{item['id']}"):
                            _delete(f"/api/devices/{item['id']}", "Không thể xóa thiết bị")


def show_area_management() -> None:
    """Render the three related master-data interfaces as card views."""
    st.subheader("Quản lý dữ liệu khu vườn")
    st.caption("Quản lý khu vực, cây trồng và thiết bị trong cùng một không gian.")

    area_tab, crop_tab, device_tab = st.tabs(["Khu vực", "Cây trồng", "Thiết bị"])

    with area_tab:
        header, action = st.columns([8, 1])
        header.markdown("#### Cơ sở dữ liệu khu vực")
        if action.button(" ", icon=":material/add:", help="Thêm khu vực", key="add_area_button", type="primary"):
            add_area_dialog()
        try:
            areas = request("GET", "/api/areas")
        except Exception as exc:
            st.error(str(exc)); areas = []
        _management_card_grid(areas, "area")

    with crop_tab:
        header, action = st.columns([8, 1])
        header.markdown("#### Quản lý cây trồng")
        if action.button(" ", icon=":material/add:", help="Thêm cây trồng", key="add_crop_button", type="primary"):
            add_crop_dialog()
        try:
            crops = request("GET", "/api/crops")
        except Exception as exc:
            st.error(str(exc)); crops = []
        _management_card_grid(paginate_items(crops, key="garden_crop_pagination"), "crop")

    with device_tab:
        header, action = st.columns([8, 1])
        header.markdown("#### Quản lý thiết bị")
        if action.button(" ", icon=":material/add:", help="Thêm thiết bị", key="add_device_button", type="primary"):
            add_device_dialog()
        try:
            devices = request("GET", "/api/devices")
        except Exception as exc:
            st.error(str(exc)); devices = []
        _management_card_grid(paginate_items(devices, key="garden_device_pagination"), "device")
