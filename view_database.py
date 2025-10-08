import sqlite3
from datetime import datetime

def view_database():
    """View all contents of database.db"""
    try:
        conn = sqlite3.connect('database.db')
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        print("="*70)
        print("📊 DATABASE VIEWER - database.db")
        print("="*70)
        
        # Get all tables
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' 
            ORDER BY name
        """)
        tables = cursor.fetchall()
        
        if not tables:
            print("❌ No tables found in database!")
            conn.close()
            return
        
        print(f"\n📋 Found {len(tables)} table(s):")
        for table in tables:
            print(f"   - {table['name']}")
        
        # View each table
        for table in tables:
            table_name = table['name']
            print("\n" + "="*70)
            print(f"📁 TABLE: {table_name}")
            print("="*70)
            
            # Get column info
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()
            
            print("\n🔧 Structure:")
            for col in columns:
                print(f"   - {col['name']}: {col['type']}")
            
            # Get data
            cursor.execute(f"SELECT * FROM {table_name}")
            rows = cursor.fetchall()
            
            print(f"\n📊 Data ({len(rows)} rows):")
            
            if len(rows) == 0:
                print("   (empty table)")
            else:
                # Get column names
                col_names = [col['name'] for col in columns]
                
                # Print header
                print("\n   " + " | ".join(col_names))
                print("   " + "-" * (len(" | ".join(col_names)) + 10))
                
                # Print rows
                for row in rows:
                    values = []
                    for col in col_names:
                        val = row[col]
                        # Truncate long strings
                        if isinstance(val, str) and len(val) > 30:
                            val = val[:27] + "..."
                        values.append(str(val) if val is not None else "NULL")
                    print("   " + " | ".join(values))
        
        # Summary
        print("\n" + "="*70)
        print("📈 SUMMARY")
        print("="*70)
        for table in tables:
            table_name = table['name']
            cursor.execute(f"SELECT COUNT(*) as count FROM {table_name}")
            count = cursor.fetchone()['count']
            print(f"   {table_name}: {count} records")
        
        conn.close()
        print("\n✅ Database view complete!")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        if 'conn' in locals():
            conn.close()

def view_specific_table(table_name):
    """View specific table in detail"""
    try:
        conn = sqlite3.connect('database.db')
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Check if table exists
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name=?
        """, (table_name,))
        
        if not cursor.fetchone():
            print(f"❌ Table '{table_name}' not found!")
            conn.close()
            return
        
        print("="*70)
        print(f"📁 TABLE: {table_name}")
        print("="*70)
        
        # Get all data
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()
        
        if len(rows) == 0:
            print("❌ No data in this table")
        else:
            # Get column names
            col_names = rows[0].keys()
            
            # Print each row in detail
            for i, row in enumerate(rows, 1):
                print(f"\n📄 Record #{i}")
                print("-" * 50)
                for col in col_names:
                    print(f"   {col:20s}: {row[col]}")
        
        print(f"\n📊 Total: {len(rows)} records")
        conn.close()
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        if 'conn' in locals():
            conn.close()

def interactive_mode():
    """Interactive database viewer"""
    while True:
        print("\n" + "="*70)
        print("🔍 DATABASE VIEWER - INTERACTIVE MODE")
        print("="*70)
        print("1. View all tables")
        print("2. View specific table (users)")
        print("3. View specific table (classes)")
        print("4. View specific table (attendance)")
        print("5. View specific table (coordinates)")
        print("6. Exit")
        
        choice = input("\nYour choice (1-6): ").strip()
        
        if choice == '1':
            view_database()
        elif choice == '2':
            view_specific_table('users')
        elif choice == '3':
            view_specific_table('classes')
        elif choice == '4':
            view_specific_table('attendance')
        elif choice == '5':
            view_specific_table('coordinates')
        elif choice == '6':
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice!")

if __name__ == '__main__':
    # Uncomment one of these:
    
    # Option 1: View all database at once
    view_database()
    
    # Option 2: Interactive mode
    # interactive_mode()
    
    # Option 3: View specific table
    # view_specific_table('classes')