import sqlite3

# Kết nối tới cơ sở dữ liệu (nó sẽ tạo file data.db nếu chưa tồn tại)
conn = sqlite3.connect('data.db')
cursor = conn.cursor()

# Tạo bảng nếu chưa tồn tại
cursor.execute('''
CREATE TABLE IF NOT EXISTS comments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    comment TEXT
)
''')

# Lưu thay đổi và đóng kết nối
conn.commit()
conn.close()
