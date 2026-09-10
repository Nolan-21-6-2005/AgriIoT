import sqlite3, hashlib
from pathlib import Path
BASE=Path(__file__).resolve().parent.parent; DB_PATH=BASE/'data'/'agriot.db'
def hp(p): return hashlib.sha256(p.encode()).hexdigest()
def init_db():
    DB_PATH.parent.mkdir(exist_ok=True); conn=sqlite3.connect(DB_PATH); c=conn.cursor(); c.execute('PRAGMA foreign_keys=ON')
    c.executescript('''
    CREATE TABLE IF NOT EXISTS Users(id INTEGER PRIMARY KEY AUTOINCREMENT,ten_dang_nhap TEXT UNIQUE NOT NULL,password TEXT NOT NULL,role INTEGER DEFAULT 1,ho_ten TEXT NOT NULL,ngay_sinh TEXT,gioi_tinh TEXT,email TEXT UNIQUE,so_dien_thoai TEXT,anh_dai_dien TEXT DEFAULT 'data/avatars/default.png',created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
    CREATE TABLE IF NOT EXISTS Devices(id INTEGER PRIMARY KEY AUTOINCREMENT,ten_thiet_bi TEXT UNIQUE NOT NULL,loai_thiet_bi TEXT NOT NULL,trang_thai INTEGER DEFAULT 0,is_deleted INTEGER DEFAULT 0,vi_tri TEXT NOT NULL,created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
    CREATE TABLE IF NOT EXISTS Crops(id INTEGER PRIMARY KEY AUTOINCREMENT,ten_cay TEXT NOT NULL,loai_cay TEXT NOT NULL,khu_vuc TEXT NOT NULL,ngay_trong TEXT,trang_thai TEXT DEFAULT 'Đang sinh trưởng',is_deleted INTEGER DEFAULT 0,created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP); CREATE TABLE IF NOT EXISTS Areas(id INTEGER PRIMARY KEY AUTOINCREMENT,ten_khu_vuc TEXT UNIQUE NOT NULL,mo_ta TEXT DEFAULT '',dien_tich REAL DEFAULT 0,trang_thai TEXT DEFAULT 'Đang hoạt động',is_deleted INTEGER DEFAULT 0,created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP); CREATE TABLE IF NOT EXISTS Irrigation_Logs(id INTEGER PRIMARY KEY AUTOINCREMENT,device_id INTEGER NOT NULL,ngay_tuoi_cay TIMESTAMP DEFAULT CURRENT_TIMESTAMP,thoi_gian_tuoi INTEGER DEFAULT 0,do_am_dat REAL DEFAULT 50.0,trang_thai INTEGER DEFAULT 0,ai_decision INTEGER DEFAULT 0,created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,FOREIGN KEY(device_id) REFERENCES Devices(id) ON DELETE CASCADE);
    ''')
    cols={r[1] for r in c.execute('PRAGMA table_info(Devices)')}
    for name,typ in [('duration_seconds','INTEGER DEFAULT 600'),('max_duration_seconds','INTEGER DEFAULT 1200'),('last_seen','TIMESTAMP'),('vi_tri_x','REAL DEFAULT 50'),('vi_tri_y','REAL DEFAULT 50')]:
        if name not in cols: c.execute(f'ALTER TABLE Devices ADD COLUMN {name} {typ}')
    users=[('admin123',hp('admin123'),0,'Lê Nam Sơn','2005-06-21','Nam','minh.admin@vnua.edu.vn','0912345678'),('GV123',hp('gv123'),1,'Nguyễn Văn A','1985-05-20','Nam','gv.a@vnua.edu.vn','0987654321'),('BV001',hp('bv123'),1,'Trần Thị B','1990-10-15','Nữ','bv.b@vnua.edu.vn','0123456789')]
    c.executemany('INSERT OR IGNORE INTO Users(ten_dang_nhap,password,role,ho_ten,ngay_sinh,gioi_tinh,email,so_dien_thoai) VALUES(?,?,?,?,?,?,?,?)',users)
    devices=[('PUMP-01','Máy bơm tưới nước',1,0,'Khu A',600,1200,22,30),('PUMP-02','Máy bơm tưới nước',1,0,'Khu B',300,1200,72,30),('PUMP-03','Máy bơm tưới nước',0,0,'Khu C',900,1200,48,73),('SENSOR-01','Cảm biến độ ẩm đất',1,0,'Khu A',0,0,35,42),('SENSOR-02','Cảm biến độ ẩm đất',1,0,'Khu B',0,0,78,42),('SENSOR-03','Cảm biến độ ẩm đất',0,0,'Khu C',0,0,78,76)]
    c.executemany('INSERT OR IGNORE INTO Devices(ten_thiet_bi,loai_thiet_bi,trang_thai,is_deleted,vi_tri,duration_seconds,max_duration_seconds,vi_tri_x,vi_tri_y) VALUES(?,?,?,?,?,?,?,?,?)',devices)
    areas=[('Khu A','Khu trồng cà chua',120,'Đang hoạt động'),('Khu B','Khu trồng dưa chuột',150,'Đang hoạt động'),('Khu C','Khu trồng rau cải',100,'Đang hoạt động')]
    c.executemany('INSERT OR IGNORE INTO Areas(ten_khu_vuc,mo_ta,dien_tich,trang_thai,is_deleted) VALUES(?,?,?,?,0)',areas)

    crops=[('Cà chua A1','Cà chua','Khu A','2026-08-15','Đang sinh trưởng'),('Cà chua A2','Cà chua','Khu A','2026-08-18','Đang sinh trưởng'),('Dưa chuột B1','Dưa chuột','Khu B','2026-08-20','Đang sinh trưởng'),('Dưa chuột B2','Dưa chuột','Khu B','2026-08-21','Đang sinh trưởng'),('Rau cải C1','Rau cải','Khu C','2026-08-25','Đang sinh trưởng'),('Rau cải C2','Rau cải','Khu C','2026-08-26','Đang sinh trưởng')]
    if c.execute('SELECT COUNT(*) FROM Crops').fetchone()[0] == 0:
        c.executemany('INSERT INTO Crops(ten_cay,loai_cay,khu_vuc,ngay_trong,trang_thai,is_deleted) VALUES(?,?,?,?,?,0)',crops)

    positions={'PUMP-01':(22,30),'PUMP-02':(72,30),'PUMP-03':(48,73),'SENSOR-01':(35,42),'SENSOR-02':(78,42),'SENSOR-03':(78,76)}
    for device_name,(x,y) in positions.items():
        c.execute('UPDATE Devices SET vi_tri_x=?, vi_tri_y=? WHERE ten_thiet_bi=? AND (vi_tri_x IS NULL OR vi_tri_y IS NULL OR (vi_tri_x=50 AND vi_tri_y=50))',(x,y,device_name))
    conn.commit(); conn.close(); print(f'Database ready: {DB_PATH}')
if __name__=='__main__': init_db()
