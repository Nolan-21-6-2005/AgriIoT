from backend.database import fetch_one, fetch_all

def test_seed_users_exist():
    assert fetch_one('SELECT id FROM Users WHERE ten_dang_nhap=?', ('admin123',)) is not None

def test_devices_exist():
    assert len(fetch_all('SELECT id FROM Devices WHERE is_deleted=0')) >= 1
