import sqlite3
import os
from datetime import datetime

# Use absolute path for Railway deployment
DB_DIR = os.path.join(os.getcwd(), 'db')
DB_PATH = os.path.join(DB_DIR, 'database.db')

def init_db():
    """Initialize the database and create tables if they don't exist"""
    global DB_PATH
    
    # Create db directory if it doesn't exist
    os.makedirs(DB_DIR, exist_ok=True)
    
    # Ensure database file is writable
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Create emergencies table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS emergencies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                emergency_type TEXT NOT NULL,
                lat REAL NOT NULL,
                lon REAL NOT NULL,
                image_url TEXT NOT NULL,
                timestamp DATETIME NOT NULL,
                building TEXT NOT NULL,
                floor_affected TEXT,
                gemini_verified BOOLEAN DEFAULT 0,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create users table for web app registrations
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                phone TEXT NOT NULL,
                email TEXT NOT NULL,
                lat REAL NOT NULL,
                lon REAL NOT NULL,
                accuracy REAL,
                registered_at DATETIME NOT NULL,
                last_updated DATETIME NOT NULL
            )
        ''')
        
        conn.commit()
        conn.close()
        print(f"✅ Database initialized successfully at: {DB_PATH}")
        
    except Exception as e:
        print(f"❌ Database initialization error: {e}")
        # Fallback to in-memory database if file system issues
        print("⚠️  Falling back to in-memory database")
        DB_PATH = ':memory:'

def log_emergency_to_db(emergency_data, verified=True):
    """
    Stores the emergency data in the database
    Returns the emergency ID
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO emergencies (emergency_type, lat, lon, image_url, timestamp, building, floor_affected, gemini_verified)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        emergency_data['emergency_type'],
        emergency_data['location']['lat'],
        emergency_data['location']['lon'],
        emergency_data['image_url'],
        emergency_data['timestamp'],
        emergency_data['building'],
        emergency_data.get('floor_affected'),  # Optional field
        verified
    ))
    
    emergency_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    status = "VERIFIED" if verified else "REJECTED"
    print(f"Emergency logged to database with ID: {emergency_id} - Status: {status}")
    return emergency_id

def get_all_emergencies():
    """Get all emergency records from database"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM emergencies ORDER BY created_at DESC')
    rows = cursor.fetchall()
    
    emergencies = []
    for row in rows:
        emergencies.append({
            'id': row[0],
            'emergency_type': row[1],
            'lat': row[2],
            'lon': row[3],
            'image_url': row[4],
            'timestamp': row[5],
            'building': row[6],
            'floor_affected': row[7],
            'gemini_verified': bool(row[8]),
            'created_at': row[9]
        })
    
    conn.close()
    return emergencies
    
def get_recent_emergencies(hours=2):
    """Get recent verified emergencies for web app alerts"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Get emergencies from last X hours that were verified
    cursor.execute('''
        SELECT id, emergency_type, lat, lon, image_url, timestamp, building, floor_affected, created_at
        FROM emergencies 
        WHERE gemini_verified = 1 
        AND datetime(created_at) > datetime('now', '-{} hours')
        ORDER BY created_at DESC
    '''.format(hours))
    
    rows = cursor.fetchall()
    
    emergencies = []
    for row in rows:
        emergencies.append({
            'id': row[0],
            'emergency_type': row[1],
            'location': {'lat': row[2], 'lon': row[3]},
            'image_url': row[4],
            'timestamp': row[5],
            'building': row[6],
            'floor_affected': row[7],
            'created_at': row[8]
        })
    
    conn.close()
    return emergencies

def register_user_to_db(user_data):
    """Register a new user in the database"""
    import uuid
    
    user_id = str(uuid.uuid4())
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT OR REPLACE INTO users (user_id, name, phone, email, lat, lon, accuracy, registered_at, last_updated)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        user_id,
        user_data['name'],
        user_data['phone'],
        user_data['email'],
        user_data['location']['lat'],
        user_data['location']['lon'],
        user_data['location'].get('accuracy', 0),
        datetime.now().isoformat(),
        datetime.now().isoformat()
    ))
    
    conn.commit()
    conn.close()
    
    print(f"✅ User registered to database: {user_data['name']} ({user_id})")
    return user_id

def update_user_location_in_db(user_id, location):
    """Update user location in database"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        UPDATE users 
        SET lat = ?, lon = ?, accuracy = ?, last_updated = ?
        WHERE user_id = ?
    ''', (
        location['lat'],
        location['lon'],
        location.get('accuracy', 0),
        datetime.now().isoformat(),
        user_id
    ))
    
    if cursor.rowcount > 0:
        conn.commit()
        conn.close()
        print(f"📍 Location updated in database for user: {user_id}")
        return True
    else:
        conn.close()
        print(f"⚠️  User not found in database: {user_id}")
        return False

def get_user_from_db(user_id):
    """Get user from database"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return {
            'user_id': row[0],
            'name': row[1],
            'phone': row[2],
            'email': row[3],
            'location': {
                'lat': row[4],
                'lon': row[5],
                'accuracy': row[6]
            },
            'registered_at': row[7],
            'last_updated': row[8]
        }
    return None

def get_all_users_from_db():
    """Get all users from database"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM users ORDER BY registered_at DESC')
    rows = cursor.fetchall()
    conn.close()
    
    users = []
    for row in rows:
        users.append({
            'user_id': row[0],
            'name': row[1],
            'phone': row[2],
            'email': row[3],
            'location': {
                'lat': row[4],
                'lon': row[5],
                'accuracy': row[6]
            },
            'registered_at': row[7],
            'last_updated': row[8]
        })
    
    return users