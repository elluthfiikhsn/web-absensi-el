import sqlite3

DB_NAME = "database.db"  # ganti sesuai nama database kamu

def clear_data_and_reset():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # daftar tabel (urutkan manual biar aman kalau ada relasi)
    tables = [
        "attendance_logs",
        "attendance",
        "classes",
        "coordinates",
        "face_data",
        "settings",
        "users"
    ]
    
    # hapus isi tabel
    for table in tables:
        try:
            cursor.execute(f"DELETE FROM {table}")
            print(f"✅ Cleared data from {table}")
        except Exception as e:
            print(f"⚠️ Error clearing {table}: {e}")
    
    # reset autoincrement counter
    try:
        cursor.execute("DELETE FROM sqlite_sequence")
        print("🔄 Reset autoincrement counters")
    except Exception as e:
        print(f"⚠️ Error resetting autoincrement: {e}")

    conn.commit()
    conn.close()
    print("\n🎉 Done! Database cleared successfully.")

if __name__ == "__main__":
    clear_data_and_reset()
