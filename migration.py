# migration.py
import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Cek apakah kolom email masih ada
cursor.execute("PRAGMA table_info(users)")
columns = [column[1] for column in cursor.fetchall()]

if 'email' in columns and 'class_id' not in columns:
    print("Migrating database...")
    
    # Backup old table
    cursor.execute('''
        CREATE TABLE users_backup AS SELECT * FROM users
    ''')
    
    # Drop old table
    cursor.execute('DROP TABLE users')
    
    # Create new table dengan class_id
    cursor.execute('''
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            full_name TEXT NOT NULL,
            class_id INTEGER,
            role TEXT DEFAULT 'user',
            active INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (class_id) REFERENCES classes (id) ON DELETE SET NULL
        )
    ''')
    
    # Copy data (email akan NULL/diabaikan)
    cursor.execute('''
        INSERT INTO users (id, username, password, full_name, role, active, created_at, updated_at)
        SELECT id, username, password, full_name, role, active, created_at, updated_at
        FROM users_backup
    ''')
    
    # Drop backup
    cursor.execute('DROP TABLE users_backup')
    
    conn.commit()
    print("Migration completed!")

conn.close()