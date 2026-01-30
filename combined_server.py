#!/usr/bin/env python3
"""
Combined AlertAI Server
Serves both the web app (static files) and API endpoints on the same port
Perfect for single ngrok tunnel deployment
"""
from flask import Flask, request, jsonify, send_from_directory, send_file
from flask_cors import CORS
from datetime import datetime
import json
import os
import sys
from dotenv import load_dotenv, dotenv_values

# Load environment variables from server/.env - prioritize .env file over system environment
server_env_path = os.path.join('server', '.env')
load_dotenv(server_env_path)

# Get values from server/.env file directly (prioritize .env over system env)
server_env_values = dotenv_values(server_env_path)

# Override system environment with .env file values for critical variables
if server_env_values.get('GEMINI_API_KEY'):
    os.environ['GEMINI_API_KEY'] = server_env_values['GEMINI_API_KEY']
    print(f"🔑 Server using GEMINI_API_KEY from .env file: {server_env_values['GEMINI_API_KEY'][:20]}...")

# Import server utilities
sys.path.append('server')
from utils.db_utils import init_db, log_emergency_to_db, get_recent_emergencies, get_all_emergencies
from utils.users import get_nearby_users, load_users, register_user, update_user_location
from utils.notifications import send_alert_to_users
from utils.gemini_verification_local import gemini_verifier

app = Flask(__name__)
CORS(app)  # Enable CORS for web app connection

# Initialize database on startup
init_db()

# =============================================================================
# API ENDPOINTS (from server/app.py)
# =============================================================================

@app.route('/emergency', methods=['POST'])
def receive_emergency():
    """
    Receives emergency data from edge device.
    Processes with Gemini verification and sends alerts if approved.
    """
    try:
        # Get JSON data with better error handling
        try:
            data = request.get_json()
            if not data:
                print("❌ No JSON data received")
                return jsonify({'error': 'No JSON data provided'}), 400
        except Exception as json_error:
            print(f"❌ JSON parsing error: {json_error}")
            return jsonify({'error': 'Invalid JSON format'}), 400
        
        # Validate required fields with detailed error messages
        required_fields = ['emergency_type', 'location', 'image_url', 'timestamp', 'building']
        missing_fields = []
        for field in required_fields:
            if field not in data:
                missing_fields.append(field)
        
        if missing_fields:
            error_msg = f"Missing required fields: {', '.join(missing_fields)}"
            print(f"❌ Validation error: {error_msg}")
            return jsonify({'error': error_msg}), 400
        
        # Validate location has lat/lon with detailed error messages
        if not isinstance(data['location'], dict):
            print("❌ Location must be an object with lat/lon")
            return jsonify({'error': 'Location must be an object with lat/lon'}), 400
            
        if 'lat' not in data['location'] or 'lon' not in data['location']:
            print("❌ Location missing lat/lon coordinates")
            return jsonify({'error': 'Location must contain lat and lon coordinates'}), 400
        
        # 🤖 GEMINI VERIFICATION - Verify emergency with AI
        print(f"\n🔍 GEMINI VERIFICATION STARTING...")
        print(f"Emergency Type: {data['emergency_type']}")
        print(f"Image URL: {data['image_url']}")
        
        try:
            is_verified = gemini_verifier.verify_emergency_with_gemini(
                data['image_url'], 
                data['emergency_type']
            )
        except Exception as gemini_error:
            print(f"❌ Gemini verification error: {gemini_error}")
            # For simulations, continue processing even if Gemini fails
            if data.get('simulation', False):
                print("⚠️ Simulation mode - bypassing Gemini verification failure")
                is_verified = True
            else:
                return jsonify({'error': 'Emergency verification failed', 'details': str(gemini_error)}), 500
        
        if not is_verified:
            # Log the rejected emergency but don't send alerts
            try:
                emergency_id = log_emergency_to_db(data, verified=False)
                print(f"❌ Emergency REJECTED - ID: {emergency_id}")
                return jsonify({'status': 'rejected', 'emergency_id': emergency_id, 'message': 'Emergency not verified by AI'}), 200
            except Exception as db_error:
                print(f"❌ Database error during rejection logging: {db_error}")
                return jsonify({'error': 'Database error during rejection logging'}), 500
        
        # Emergency verified - proceed with alerts
        print("✅ Emergency verified by Gemini - proceeding...")
        
        # Log emergency to database
        try:
            emergency_id = log_emergency_to_db(data, verified=True)
        except Exception as db_error:
            print(f"❌ Database error during emergency logging: {db_error}")
            return jsonify({'error': 'Database error during emergency logging'}), 500
        
        # Load users and filter by proximity
        try:
            users = load_users()
            nearby_users = get_nearby_users(data['location'], users)
        except Exception as user_error:
            print(f"❌ User loading error: {user_error}")
            return jsonify({'error': 'Error loading users for notification'}), 500
        
        # Send alerts to nearby users (including web app users)
        try:
            if nearby_users:
                send_alert_to_users(nearby_users, data, emergency_id)
                print(f"🚨 Emergency PROCESSED - ID: {emergency_id} - {len(nearby_users)} users alerted")
                return jsonify({
                    'status': 'success', 
                    'emergency_id': emergency_id, 
                    'users_alerted': len(nearby_users),
                    'message': 'Emergency processed and alerts sent'
                }), 200
            else:
                print(f"⚠️  Emergency PROCESSED - ID: {emergency_id} - No users nearby")
                return jsonify({
                    'status': 'success', 
                    'emergency_id': emergency_id, 
                    'users_alerted': 0,
                    'message': 'Emergency processed but no users nearby to alert'
                }), 200
        except Exception as alert_error:
            print(f"❌ Alert sending error: {alert_error}")
            
            # For simulations, don't fail completely if alert sending fails
            if data.get('simulation', False):
                print(f"⚠️ Simulation mode - alert sending failed but continuing: {alert_error}")
                return jsonify({
                    'status': 'success', 
                    'emergency_id': emergency_id, 
                    'users_alerted': 0,
                    'message': 'Simulation processed (alert sending failed but this is expected for testing)',
                    'warning': 'Alert sending failed but simulation was successful'
                }), 200
            else:
                return jsonify({'error': 'Error sending alerts to users', 'details': str(alert_error)}), 500
        
    except Exception as e:
        print(f"❌ Server error: {str(e)}")
        import traceback
        traceback.print_exc()  # Print full stack trace for debugging
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500

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

@app.route('/api/test-whatsapp', methods=['POST'])
def test_whatsapp_integration():
    """Test WhatsApp integration endpoint"""
    try:
        # Import the test function
        import sys
        import os
        
        # Add server utils to path
        server_utils_path = os.path.join(os.getcwd(), 'server', 'utils')
        if server_utils_path not in sys.path:
            sys.path.insert(0, server_utils_path)
        
        from twilio_whatsapp import test_whatsapp_integration
        
        success, message = test_whatsapp_integration()
        
        return jsonify({
            'success': success,
            'message': message,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'WhatsApp test failed'
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint with database status"""
    import sqlite3
    from server.utils.db_utils import DB_PATH
    
    health_status = {
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'database': {
            'status': 'unknown',
            'path': DB_PATH,
            'tables': []
        }
    }
    
    # Check database status
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Check if tables exist
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [table[0] for table in cursor.fetchall()]
        health_status['database']['tables'] = tables
        
        # Check if required tables exist
        required_tables = ['users', 'emergencies']
        missing_tables = [table for table in required_tables if table not in tables]
        
        if missing_tables:
            health_status['database']['status'] = 'missing_tables'
            health_status['database']['missing'] = missing_tables
            health_status['status'] = 'degraded'
        else:
            # Test table access
            cursor.execute("SELECT COUNT(*) FROM users")
            user_count = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM emergencies")
            emergency_count = cursor.fetchone()[0]
            
            health_status['database']['status'] = 'healthy'
            health_status['database']['counts'] = {
                'users': user_count,
                'emergencies': emergency_count
            }
        
        conn.close()
        
    except Exception as e:
        health_status['database']['status'] = 'error'
        health_status['database']['error'] = str(e)
        health_status['status'] = 'unhealthy'
    
    return jsonify(health_status)

@app.route('/init-db', methods=['POST'])
def manual_init_db():
    """Manual database initialization endpoint"""
    try:
        from server.utils.db_utils import init_db
        init_db()
        return jsonify({
            'status': 'success',
            'message': 'Database initialized successfully',
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Database initialization failed: {str(e)}',
            'timestamp': datetime.now().isoformat()
        }), 500

# =============================================================================
# CPR MONITOR INTEGRATION
# =============================================================================

@app.route('/cpr-monitor')
def cpr_monitor():
    """Serve the CPR PoseNet monitor interface"""
    return send_from_directory('cpr-posenet-monitor', 'index.html')

@app.route('/cpr-monitor/<path:filename>')
def cpr_monitor_assets(filename):
    """Serve CPR monitor static assets"""
    try:
        # Security check - prevent directory traversal
        if '..' in filename or filename.startswith('/'):
            return "Access denied", 403
        
        return send_from_directory('cpr-posenet-monitor', filename)
    except FileNotFoundError:
        return f"CPR monitor file not found: {filename}", 404

@app.route('/emergencies', methods=['GET'])
def get_emergencies():
    """Get all emergency records for debugging/analysis"""
    emergencies = get_all_emergencies()
    return jsonify({'emergencies': emergencies})

@app.route('/api/guidance-agent', methods=['POST'])
def guidance_agent_chat():
    """Handle guidance agent chat requests"""
    try:
        data = request.get_json()
        emergency_type = data.get('emergency_type', 'Fire')
        user_message = data.get('message', '')
        conversation_history = data.get('history', [])
        
        if not user_message:
            return jsonify({'error': 'No message provided'}), 400
        
        # Import and use the appropriate agent
        import sys
        import os
        
        # Add the alertai-agent directory to Python path
        agent_path = os.path.join(os.getcwd(), 'alertai-agent')
        if agent_path not in sys.path:
            sys.path.insert(0, agent_path)
        
        # Temporarily change to agent directory for imports
        original_cwd = os.getcwd()
        try:
            os.chdir('alertai-agent')
            
            if emergency_type.lower() == 'fire':
                from fire_emergency_agent import FireEmergencyAgent
                agent = FireEmergencyAgent()
                agent_name = "Fire Specialist"
                
            elif emergency_type.lower() == 'blood':
                from blood_emergency_agent import BloodEmergencyAgent
                agent = BloodEmergencyAgent()
                agent_name = "Blood Emergency Specialist"
                
            elif emergency_type.lower() == 'fallen person':
                from fallen_person_agent import FallenPersonAgent
                agent = FallenPersonAgent()
                agent_name = "Medical Specialist"
                
            elif emergency_type.lower() == 'smoke':
                from smoke_emergency_agent import SmokeEmergencyAgent
                agent = SmokeEmergencyAgent()
                agent_name = "Smoke Safety Specialist"
                
            elif emergency_type.lower() == 'gun':
                from gun_emergency_agent import GunEmergencyAgent
                agent = GunEmergencyAgent()
                agent_name = "Security Response Specialist"
                
            else:
                # Fallback for unknown emergency types
                return jsonify({
                    'success': True,
                    'response': f"I'm the {emergency_type} Emergency Specialist. I'm here to help you through this emergency step by step. Please tell me your current location and what you can see.",
                    'agent_type': f'{emergency_type} Emergency Specialist',
                    'conversation_history': conversation_history + [f"User: {user_message}"]
                })
        
        finally:
            # Always restore original working directory
            os.chdir(original_cwd)
        
        # Set conversation history if provided - convert from web format to agent format
        if conversation_history:
            # Convert from web format [{sender: 'user', message: 'text'}, ...] to agent format ['User: text', ...]
            agent_history = []
            for item in conversation_history:
                if isinstance(item, dict):
                    sender = item.get('sender', 'user')
                    message = item.get('message', '')
                    if sender == 'user':
                        agent_history.append(f"User: {message}")
                    elif sender == 'agent':
                        agent_history.append(f"{agent_name}: {message}")
                elif isinstance(item, str):
                    # Already in agent format
                    agent_history.append(item)
            
            agent.conversation_history = agent_history
        
        # Get response from Gemini via the agent
        response = agent.call_gemini(user_message)
        
        # Add to conversation history
        agent.conversation_history.append(f"User: {user_message}")
        agent.conversation_history.append(f"{agent_name}: {response}")
        
        return jsonify({
            'success': True,
            'response': response,
            'agent_type': f'{emergency_type} Emergency Specialist',
            'conversation_history': agent.conversation_history
        })
        
    except Exception as e:
        print(f"❌ Guidance agent error: {e}")
        import traceback
        traceback.print_exc()  # Print full stack trace for debugging
        return jsonify({
            'success': False,
            'error': str(e),
            'response': f"I'm experiencing technical difficulties. For immediate help, please call emergency services at 911."
        }), 500

@app.route('/api/launch-agent', methods=['POST'])
def launch_terminal_agent():
    """Launch terminal guidance agent for debugging"""
    try:
        data = request.get_json()
        emergency_type = data.get('emergency_type')
        launch_terminal = data.get('launch_terminal', False)
        
        if not emergency_type or not launch_terminal:
            return jsonify({
                'success': False, 
                'error': 'Missing parameters',
                'message': 'Emergency type and launch_terminal flag are required'
            }), 400
        
        # Map emergency types to agent scripts
        agent_scripts = {
            'Fire': 'alertai-agent/fire_emergency_agent.py',
            'Smoke': 'alertai-agent/smoke_emergency_agent.py',
            'Fallen Person': 'alertai-agent/fallen_person_agent.py',
            'Gun': 'alertai-agent/gun_emergency_agent.py',
            'Blood': 'alertai-agent/blood_emergency_agent.py'
        }
        
        script_path = agent_scripts.get(emergency_type)
        if not script_path:
            return jsonify({
                'success': False, 
                'error': f'No agent available for {emergency_type}',
                'available_types': list(agent_scripts.keys())
            }), 400
        
        # Check if script file exists
        if not os.path.exists(script_path):
            return jsonify({
                'success': False,
                'error': f'Agent script not found: {script_path}',
                'message': 'The agent file may be missing or moved'
            }), 404
        
        # Try to launch terminal agent
        try:
            import subprocess
            import sys
            
            # For Windows - open new command prompt with the agent
            if sys.platform == "win32":
                # Use start command to open new terminal window
                cmd = f'start "AlertAI {emergency_type} Agent" cmd /k "python {script_path}"'
                process = subprocess.Popen(cmd, shell=True)
                
                print(f"🖥️ Launched terminal agent: {emergency_type} (PID: {process.pid})")
                return jsonify({
                    'success': True, 
                    'message': f'{emergency_type} terminal agent launched successfully',
                    'command': f'python {script_path}',
                    'platform': 'Windows',
                    'process_id': process.pid
                })
            else:
                # For Linux/Mac - try different terminal emulators
                terminal_commands = [
                    ['gnome-terminal', '--', 'python3', script_path],
                    ['xterm', '-e', f'python3 {script_path}'],
                    ['konsole', '-e', f'python3 {script_path}'],
                    ['mate-terminal', '-e', f'python3 {script_path}']
                ]
                
                process = None
                used_terminal = None
                
                for cmd in terminal_commands:
                    try:
                        process = subprocess.Popen(cmd)
                        used_terminal = cmd[0]
                        break
                    except FileNotFoundError:
                        continue
                
                if process:
                    print(f"🖥️ Launched terminal agent: {emergency_type} via {used_terminal}")
                    return jsonify({
                        'success': True,
                        'message': f'{emergency_type} terminal agent launched via {used_terminal}',
                        'command': f'python3 {script_path}',
                        'platform': 'Unix',
                        'terminal': used_terminal,
                        'process_id': process.pid
                    })
                else:
                    # Fallback - run in background without terminal
                    process = subprocess.Popen([sys.executable, script_path])
                    print(f"🖥️ Launched background agent: {emergency_type} (no terminal available)")
                    return jsonify({
                        'success': True,
                        'message': f'{emergency_type} agent launched in background (no terminal available)',
                        'command': f'python3 {script_path}',
                        'platform': 'Unix',
                        'mode': 'background',
                        'process_id': process.pid
                    })
                
        except Exception as e:
            print(f"❌ Failed to launch terminal agent: {e}")
            return jsonify({
                'success': False, 
                'error': f'Failed to launch terminal: {str(e)}',
                'manual_command': f'python {script_path}',
                'message': 'You can run the agent manually using the provided command'
            }), 500
        
    except Exception as e:
        print(f"❌ Launch agent endpoint error: {e}")
        return jsonify({
            'success': False, 
            'error': str(e),
            'message': 'Internal server error while launching agent'
        }), 500

# =============================================================================
# WEB APP STATIC FILE SERVING
# =============================================================================

@app.route('/')
def serve_index():
    """Serve the main web app"""
    return send_from_directory('alertai-webapp', 'alertai.html')

@app.route('/<path:filename>')
def serve_static_files(filename):
    """Serve static files from alertai-webapp directory"""
    try:
        # Security check - prevent directory traversal
        if '..' in filename or filename.startswith('/'):
            return "Access denied", 403
        
        # Serve files from alertai-webapp directory
        return send_from_directory('alertai-webapp', filename)
    except FileNotFoundError:
        return f"File not found: {filename}", 404

# =============================================================================
# FIRE DATASET IMAGE SERVING (for Gemini verification)
# =============================================================================

@app.route('/fire_dataset/<path:filename>')
def serve_fire_dataset(filename):
    """Serve fire dataset images for Gemini verification"""
    try:
        # Security check
        if '..' in filename or filename.startswith('/'):
            return "Access denied", 403
        
        return send_from_directory('fire_dataset', filename)
    except FileNotFoundError:
        return f"Fire dataset file not found: {filename}", 404

# =============================================================================
# SERVER TEST IMAGES (fallback)
# =============================================================================

@app.route('/test_images/<path:filename>')
def serve_test_images(filename):
    """Serve test images from server directory"""
    try:
        # Security check
        if '..' in filename or filename.startswith('/'):
            return "Access denied", 403
        
        return send_from_directory('server/test_images', filename)
    except FileNotFoundError:
        return f"Test image not found: {filename}", 404

if __name__ == '__main__':
    # Railway deployment configuration
    port = int(os.environ.get("PORT", 8000))
    debug_mode = os.environ.get("FLASK_ENV", "production") == "development"
    
    print("🚀 STARTING COMBINED ALERTAI SERVER")
    print("=" * 60)
    print(f"🌐 Web App: http://0.0.0.0:{port}")
    print(f"📡 API Server: http://0.0.0.0:{port}/api/")
    print(f"🔍 Health Check: http://0.0.0.0:{port}/health")
    print("=" * 60)
    print("📝 FEATURES:")
    print("✅ Web App (AlertAI interface)")
    print("✅ API Server (Emergency alerts)")
    print("✅ Gemini Verification")
    print("✅ Fire Dataset Images")
    print("✅ Railway deployment ready")
    print("=" * 60)
    print(f"🚀 Environment: {'Development' if debug_mode else 'Production'}")
    print(f"🔌 Port: {port}")
    print("=" * 60)
    
    app.run(debug=debug_mode, host='0.0.0.0', port=port)