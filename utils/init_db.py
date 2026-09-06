import sqlite3
import os
import hashlib


DB_DIR = "data"
DB_PATH = os.path.join(DB_DIR, "agriot.db")


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def init_db():

    # =========================
    # 1. Tạo thư mục database
    # =========================

    os.makedirs(DB_DIR, exist_ok=True)

    conn = None

    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()

        # Bật Foreign Key
        c.execute("PRAGMA foreign_keys = ON;")

        # =========================
        # 2. USERS
        # =========================

        c.execute("""
            CREATE TABLE IF NOT EXISTS Users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,

                ten_dang_nhap TEXT UNIQUE NOT NULL,

                password TEXT NOT NULL,

                role INTEGER DEFAULT 1,

                ho_ten TEXT NOT NULL,

                ngay_sinh TEXT,

                gioi_tinh TEXT,

                email TEXT UNIQUE,

                so_dien_thoai TEXT,

                anh_dai_dien TEXT
                    DEFAULT 'data/avatars/default.png',

                created_at TIMESTAMP
                    DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # =========================
        # 3. DEVICES
        # =========================

        c.execute("""
            CREATE TABLE IF NOT EXISTS Devices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,

                ten_thiet_bi TEXT UNIQUE NOT NULL,

                loai_thiet_bi TEXT NOT NULL,

                trang_thai INTEGER DEFAULT 0,

                is_deleted INTEGER DEFAULT 0,

                vi_tri TEXT NOT NULL,

                created_at TIMESTAMP
                    DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # =========================
        # 4. IRRIGATION LOGS
        # =========================

        c.execute("""
            CREATE TABLE IF NOT EXISTS Irrigation_Logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,

                device_id INTEGER NOT NULL,

                ngay_tuoi_cay TIMESTAMP
                    DEFAULT CURRENT_TIMESTAMP,

                thoi_gian_tuoi INTEGER DEFAULT 0,

                do_am_dat REAL DEFAULT 50.0,

                trang_thai INTEGER DEFAULT 0,

                ai_decision INTEGER DEFAULT 0,

                created_at TIMESTAMP
                    DEFAULT CURRENT_TIMESTAMP,

                FOREIGN KEY(device_id)
                    REFERENCES Devices(id)
                    ON DELETE CASCADE
            )
        """)

        # =========================
        # 5. USERS DATA
        # =========================

        users = [
            (
                "admin123",
                hash_password("admin123"),
                0,
                "Lê Nam Sơn",
                "2005-06-21",
                "Nam",
                "minh.admin@vnua.edu.vn",
                "0912345678"
            ),

            (
                "GV123",
                hash_password("gv123"),
                1,
                "Nguyễn Văn A",
                "1985-05-20",
                "Nam",
                "gv.a@vnua.edu.vn",
                "0987654321"
            ),

            (
                "BV001",
                hash_password("bv123"),
                1,
                "Trần Thị B",
                "1990-10-15",
                "Nữ",
                "bv.b@vnua.edu.vn",
                "0123456789"
            )
        ]

        c.executemany("""
            INSERT OR IGNORE INTO Users
            (
                ten_dang_nhap,
                password,
                role,
                ho_ten,
                ngay_sinh,
                gioi_tinh,
                email,
                so_dien_thoai
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, users)

        # =========================
        # 6. DEVICES DATA
        # =========================

        devices = [
            (
                "PUMP-01",
                "Máy bơm tưới nước",
                1,
                0,
                "Khu A"
            ),

            (
                "PUMP-02",
                "Máy bơm tưới nước",
                1,
                0,
                "Khu B"
            ),

            (
                "PUMP-03",
                "Máy bơm tưới nước",
                0,
                0,
                "Khu C"
            ),

            (
                "SENSOR-01",
                "Cảm biến độ ẩm đất",
                1,
                0,
                "Khu A"
            ),

            (
                "SENSOR-02",
                "Cảm biến độ ẩm đất",
                1,
                0,
                "Khu B"
            ),

            (
                "SENSOR-03",
                "Cảm biến độ ẩm đất",
                0,
                0,
                "Khu C"
            )
        ]

        c.executemany("""
            INSERT OR IGNORE INTO Devices
            (
                ten_thiet_bi,
                loai_thiet_bi,
                trang_thai,
                is_deleted,
                vi_tri
            )
            VALUES (?, ?, ?, ?, ?)
        """, devices)

        # =========================
        # 7. LẤY ID THIẾT BỊ
        # =========================

        device_names = [
            "PUMP-01",
            "PUMP-02",
            "PUMP-03"
        ]

        device_ids = {}

        for name in device_names:

            c.execute("""
                SELECT id
                FROM Devices
                WHERE ten_thiet_bi = ?
            """, (name,))

            result = c.fetchone()

            if result:
                device_ids[name] = result[0]

        # =========================
        # 8. IRRIGATION LOGS
        # =========================

        irrigation_logs = [
            (
                device_ids["PUMP-01"],
                600,
                27.54,
                1,
                1
            ),

            (
                device_ids["PUMP-02"],
                300,
                51.0,
                1,
                0
            ),

            (
                device_ids["PUMP-03"],
                900,
                30.0,
                0,
                1
            )
        ]

        c.executemany("""
            INSERT INTO Irrigation_Logs
            (
                device_id,
                thoi_gian_tuoi,
                do_am_dat,
                trang_thai,
                ai_decision
            )
            VALUES (?, ?, ?, ?, ?)
        """, irrigation_logs)

        # =========================
        # 9. LƯU DATABASE
        # =========================

        conn.commit()

        print(f"Hoan thanh khoi tao tai: {DB_PATH}")

    except sqlite3.Error as e:

        print(f"Loi SQLite: {e}")

        if conn:
            conn.rollback()

    finally:

        if conn:
            conn.close()


if __name__ == "__main__":
    init_db()
