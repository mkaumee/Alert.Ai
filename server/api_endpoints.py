"""
API endpoints for AlertAI web app integration
"""
from flask import Blueprint, request, jsonify
from datetime import datetime
import sqlite3
import json

api = Blueprint('api', __name__, url_prefix='/api')

# Database path
DB_PATH = 'db/database.db'

def init_users_db():
    """Initialize users table for web app"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            email TEXT NOT NULL,
            lat REAL NOT NULL,
            lon REAL NOT NULL,
            fcm_token TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            last_location_update DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

@api.route('/users/register', methods=['POST'])
def register_user():
    """Register a new user from web app"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'phone', 'email', 'location']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        location = data['location']
        if 'lat' not in location or 'lon' not in location:
            return jsonify({'error': 'Location must contain lat and lon'}), 400
        
        # Insert user into database
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO users (name, phone, email, lat, lon, fcm_token)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            data['name'],
            data['phone'], 
            data['email'],
            location['lat'],
            location['lon'],
            data.get('fcm_token', '')
        ))
        
        user_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        print(f"✅ User registered: {data['name']} (ID: {user_id})")
        
        return jsonify({
            'status': 'success',
            'user_id': user_id,
            'message': 'User registered successfully'
        }), 201
        
    except Exception as e:
        print(f"❌ User registration error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@api.route('/users/<int:user_id>/location', methods=['PUT'])
def update_user_location(user_id):
    """Update user location"""
    try:
        data = request.get_json()
        
        if 'location' not in data:
            return jsonify({'error': 'Location data required'}), 400
        
        location = data['location']
        if 'lat' not in location or 'lon' not in location:
            return jsonify({'error': 'Location must contain lat and lon'}), 400
        
        # Update user location
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE users 
            SET lat = ?, lon = ?, last_location_update = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (location['lat'], location['lon'], user_id))
        
        if cursor.rowcount == 0:
            conn.close()
            return jsonify({'error': 'User not found'}), 404
        
        conn.commit()
        conn.close()
        
        return jsonify({
            'status': 'success',
            'message': 'Location updated successfully'
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api.route('/users', methods=['GET'])
def get_all_users():
    """Get all registered users (for admin/debugging)"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, name, phone, email, lat, lon, created_at, last_location_update
            FROM users 
            ORDER BY created_at DESC
        ''')
        
        users = []
        for row in cursor.fetchall():
            users.append({
                'id': row[0],
                'name': row[1],
                'phone': row[2],
                'email': row[3],
                'location': {'lat': row[4], 'lon': row[5]},
                'created_at': row[6],
                'last_location_update': row[7]
            })
        
        conn.close()
        
        return jsonify({
            'users': users,
            'total': len(users)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api.route('/alerts/acknowledge', methods=['POST'])
def acknowledge_alert():
    """Acknowledge an emergency alert"""
    try:
        data = request.get_json()
        
        required_fields = ['user_id', 'alert_id']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Log acknowledgment (you can expand this to track user responses)
        print(f"✅ Alert {data['alert_id']} acknowledged by user {data['user_id']}")
        
        return jsonify({
            'status': 'success',
            'message': 'Alert acknowledged'
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api.route('/emergencies/recent', methods=['GET'])
def get_recent_emergencies():
    """Get recent emergencies for web app display"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, emergency_type, lat, lon, image_url, timestamp, building, gemini_verified, created_at
            FROM emergencies 
            WHERE gemini_verified = 1
            ORDER BY created_at DESC 
            LIMIT 10
        ''')
        
        emergencies = []
        for row in cursor.fetchall():
            emergencies.append({
                'id': row[0],
                'emergency_type': row[1],
                'location': {'lat': row[2], 'lon': row[3]},
                'image_url': row[4],
                'timestamp': row[5],
                'building': row[6],
                'gemini_verified': bool(row[7]),
                'created_at': row[8]
            })
        
        conn.close()
        
        return jsonify({
            'emergencies': emergencies,
            'total': len(emergencies)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Initialize users database when module is imported
init_users_db()