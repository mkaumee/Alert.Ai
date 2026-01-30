from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import json
from utils.db_utils import init_db, log_emergency_to_db
from utils.users import get_nearby_users, load_users, register_user, update_user_location
from utils.notifications import send_alert_to_users
from utils.gemini_verification_local import gemini_verifier

app = Flask(__name__)
CORS(app)  # Enable CORS for web app connection

# Initialize database on startup
init_db()

@app.route('/emergency', methods=['POST'])
def receive_emergency():
    """
    Receives emergency data from edge device.
    Processes with Gemini verification and sends alerts if approved.
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['emergency_type', 'location', 'image_url', 'timestamp', 'building']
        for field in required_fields:
            if field not in data:
                return '', 400
        
        # Validate location has lat/lon
        if 'lat' not in data['location'] or 'lon' not in data['location']:
            return '', 400
        
        # 🤖 GEMINI VERIFICATION - Verify emergency with AI
        print(f"\n🔍 GEMINI VERIFICATION STARTING...")
        print(f"Emergency Type: {data['emergency_type']}")
        print(f"Image URL: {data['image_url']}")
        
        is_verified = gemini_verifier.verify_emergency_with_gemini(
            data['image_url'], 
            data['emergency_type']
        )
        
        if not is_verified:
            # Log the rejected emergency but don't send alerts
            emergency_id = log_emergency_to_db(data, verified=False)
            print(f"❌ Emergency REJECTED - ID: {emergency_id}")
            return '', 200
        
        # Emergency verified - proceed with alerts
        print("✅ Emergency verified by Gemini - proceeding...")
        
        # Log emergency to database
        emergency_id = log_emergency_to_db(data, verified=True)
        
        # Load users and filter by proximity
        users = load_users()
        nearby_users = get_nearby_users(data['location'], users)
        
        # Send alerts to nearby users (including web app users)
        if nearby_users:
            send_alert_to_users(nearby_users, data)
            print(f"🚨 Emergency PROCESSED - ID: {emergency_id} - {len(nearby_users)} users alerted")
        else:
            print(f"⚠️  Emergency PROCESSED - ID: {emergency_id} - No users nearby")
        
        return '', 200
        
    except Exception as e:
        print(f"❌ Server error: {str(e)}")
        return '', 500

# Web App API Endpoints
@app.route('/api/users/register', methods=['POST'])
def register_web_user():
    """Register a web app user"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'phone', 'email', 'location']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing field: {field}'}), 400
        
        # Register user
        user_id = register_user(data)
        
        return jsonify({
            'status': 'success',
            'user_id': user_id,
            'message': 'User registered successfully'
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/users/location', methods=['PUT'])
def update_location():
    """Update user location"""
    try:
        data = request.get_json()
        
        if 'user_id' not in data or 'location' not in data:
            return jsonify({'error': 'Missing user_id or location'}), 400
        
        # Update user location
        update_user_location(data['user_id'], data['location'])
        
        return jsonify({'status': 'success'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/alerts/active', methods=['GET'])
def get_active_alerts():
    """Get active emergency alerts for web app"""
    try:
        # Get recent verified emergencies (last 30 minutes only)
        from utils.db_utils import get_recent_emergencies
        alerts = get_recent_emergencies(hours=0.5)  # 30 minutes
        
        return jsonify({'alerts': alerts}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/building/<building_name>', methods=['GET'])
def get_building_data(building_name):
    """Get building layout and emergency resource data"""
    try:
        # Building data would normally come from database
        # For now, return comprehensive building data
        building_data = {
            building_name: {
                "floors": ["Ground Floor", "1st Floor", "2nd Floor"],
                "fire_extinguishers": {
                    "Ground Floor": [
                        {"location": "Near main entrance", "type": "ABC Dry Chemical", "capacity": "10 lbs", "last_inspection": "2024-01-15"},
                        {"location": "Kitchen area", "type": "Class K (Wet Chemical)", "capacity": "6 lbs", "last_inspection": "2024-01-15"},
                        {"location": "Electrical room", "type": "CO2", "capacity": "15 lbs", "last_inspection": "2024-01-10"}
                    ],
                    "1st Floor": [
                        {"location": "Corridor near elevator", "type": "ABC Dry Chemical", "capacity": "10 lbs", "last_inspection": "2024-01-15"},
                        {"location": "Emergency stairwell", "type": "ABC Dry Chemical", "capacity": "5 lbs", "last_inspection": "2024-01-12"},
                        {"location": "Office area", "type": "CO2", "capacity": "10 lbs", "last_inspection": "2024-01-10"}
                    ],
                    "2nd Floor": [
                        {"location": "Near conference room", "type": "ABC Dry Chemical", "capacity": "10 lbs", "last_inspection": "2024-01-15"},
                        {"location": "Break room", "type": "ABC Dry Chemical", "capacity": "5 lbs", "last_inspection": "2024-01-12"},
                        {"location": "Emergency exit", "type": "CO2", "capacity": "15 lbs", "last_inspection": "2024-01-10"}
                    ]
                },
                "emergency_exits": {
                    "Ground Floor": [
                        {"name": "Main entrance", "direction": "Front of building", "capacity": "200 people", "width": "Double doors"},
                        {"name": "Back exit near parking", "direction": "Rear parking lot", "capacity": "150 people", "width": "Single door"}
                    ],
                    "1st Floor": [
                        {"name": "Emergency stairwell A", "direction": "East side", "capacity": "100 people", "width": "Standard stairwell"},
                        {"name": "Emergency stairwell B", "direction": "West side", "capacity": "100 people", "width": "Standard stairwell"}
                    ],
                    "2nd Floor": [
                        {"name": "Emergency stairwell A", "direction": "East side", "capacity": "100 people", "width": "Standard stairwell"},
                        {"name": "Emergency stairwell B", "direction": "West side", "capacity": "100 people", "width": "Standard stairwell"},
                        {"name": "Fire escape", "direction": "North side", "capacity": "50 people", "width": "External ladder"}
                    ]
                },
                "assembly_points": [
                    {"name": "Parking lot area", "capacity": "300 people", "distance": "100m from building", "safety_features": ["Open space", "Away from building"]},
                    {"name": "Front courtyard", "capacity": "200 people", "distance": "50m from building", "safety_features": ["Open space", "Near road access"]}
                ],
                "special_hazards": {
                    "Ground Floor": ["High voltage electrical equipment in server room", "Natural gas lines in kitchen area", "Oxygen tanks in medical storage"],
                    "1st Floor": ["Medical oxygen supply system", "Chemical storage room with flammables", "Server room with lithium batteries"],
                    "2nd Floor": ["Backup generators with diesel fuel", "Propane tanks for heating system", "Chemical laboratory with various substances"]
                },
                "emergency_contacts": {
                    "fire_department": "911 or +234-911-FIRE",
                    "building_security": "+234-800-SECURITY",
                    "facility_manager": "+234-800-FACILITY",
                    "medical_emergency": "911 or +234-911-MEDICAL"
                },
                "building_info": {
                    "total_floors": 3,
                    "max_occupancy": 500,
                    "construction_type": "Steel frame with concrete",
                    "sprinkler_system": True,
                    "fire_alarm_system": True,
                    "emergency_lighting": True
                }
            }
        }
        
        return jsonify(building_data), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

@app.route('/emergencies', methods=['GET'])
def get_emergencies():
    """Get all emergency records for debugging/analysis"""
    from utils.db_utils import get_all_emergencies
    emergencies = get_all_emergencies()
    return jsonify({'emergencies': emergencies})

if __name__ == '__main__':
    print("Starting Emergency Alert Server...")
    print("Server running on http://localhost:5000")
    print("Health check: http://localhost:5000/health")
    app.run(debug=True, host='0.0.0.0', port=5000)