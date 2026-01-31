#!/usr/bin/env python3
"""
AlertAI Fire Emergency Response Agent - Specialized Gemini 3
Expert fire safety guidance using Gemini 3 with specialized fire protocols
"""
print("🔥 Starting Fire Emergency Agent...")
import os
import sys
import subprocess
import tempfile
import time
import json
import requests
from datetime import datetime
from config import config
print("📦 All imports loaded successfully")

class FireEmergencyAgent:
    def __init__(self):
        self.name = "AlertAI Fire Emergency Specialist"
        self.user_location = None
        self.building_layout = {}
        self.conversation_history = []
        self.emergency_context = {}
        self.fire_assessment = {
            "size": "unknown",
            "type": "unknown", 
            "location": "unknown",
            "spreading": "unknown",
            "smoke_level": "unknown"
        }
        self.current_step = 1
        self.emergency_phase = "assessment"  # assessment, decision, action, safety
        self.fire_assessment = {
            "size": "unknown",
            "type": "unknown", 
            "location": "unknown",
            "spreading": "unknown",
            "smoke_level": "unknown",
            "user_proximity": "unknown"  # close, far, different_floor
        }
        
        # Server monitoring for fire emergencies - use default if not available
        self.server_url = getattr(config, 'ALERTAI_SERVER_URL', 'http://localhost:8000')
        self.is_monitoring = False
        self.current_fire_emergency = None
        
        # Check for Gemini API key - try both possible attribute names
        self.api_key = getattr(config, 'AI_API_KEY', None) or getattr(config, 'GEMINI_API_KEY', '')
        print(f"🔑 API Key loaded: {self.api_key[:20]}..." if self.api_key else "❌ No API key")
        if not self.api_key:
            print("❌ GEMINI_API_KEY not found in environment variables")
            sys.exit(1)
        
        # Fire emergency scenario for testing
        self.test_emergency = {
            "id": 1001,
            "emergency_type": "Fire",
            "building": "Medical Center Building A",
            "location": {"lat": 11.849010, "lon": 13.056751},
            "timestamp": datetime.now().isoformat(),
            "image_url": "test_images/fire_emergency.jpg",
            "floor_affected": "1st Floor"
        }
        
        # Load specialized fire safety data
        self.load_fire_safety_data()
        
        print(f"🔥 {self.name} initialized and ready!")
        print(f"🧠 Using Gemini 3 with specialized fire safety protocols")
        print(f"🚒 Expert knowledge: Fire suppression, evacuation, safety procedures")
    
    def load_fire_safety_data(self):
        """Load specialized fire safety data and building information"""
        self.building_layout = {
            "Medical Center Building A": {
                "floors": ["Ground Floor", "1st Floor", "2nd Floor"],
                "fire_extinguishers": {
                    "Ground Floor": [
                        {
                            "location": "Near main entrance", 
                            "type": "ABC Dry Chemical", 
                            "capacity": "10 lbs",
                            "effective_against": ["Class A (ordinary combustibles)", "Class B (flammable liquids)", "Class C (electrical)"],
                            "range": "15-20 feet",
                            "discharge_time": "10-25 seconds",
                            "last_inspection": "2024-01-15"
                        },
                        {
                            "location": "Kitchen area", 
                            "type": "Class K (Wet Chemical)", 
                            "capacity": "6 lbs",
                            "effective_against": ["Class K (cooking oils and fats)"],
                            "range": "10-12 feet", 
                            "discharge_time": "85 seconds",
                            "last_inspection": "2024-01-15"
                        },
                        {
                            "location": "Electrical room", 
                            "type": "CO2", 
                            "capacity": "15 lbs",
                            "effective_against": ["Class B (flammable liquids)", "Class C (electrical)"],
                            "range": "3-8 feet",
                            "discharge_time": "8-30 seconds", 
                            "last_inspection": "2024-01-10"
                        }
                    ],
                    "1st Floor": [
                        {
                            "location": "Corridor near elevator", 
                            "type": "ABC Dry Chemical", 
                            "capacity": "10 lbs",
                            "effective_against": ["Class A", "Class B", "Class C"],
                            "range": "15-20 feet",
                            "discharge_time": "10-25 seconds",
                            "last_inspection": "2024-01-15"
                        },
                        {
                            "location": "Emergency stairwell", 
                            "type": "ABC Dry Chemical", 
                            "capacity": "5 lbs",
                            "effective_against": ["Class A", "Class B", "Class C"],
                            "range": "8-12 feet",
                            "discharge_time": "8-15 seconds",
                            "last_inspection": "2024-01-12"
                        },
                        {
                            "location": "Office area", 
                            "type": "CO2", 
                            "capacity": "10 lbs",
                            "effective_against": ["Class B", "Class C"],
                            "range": "3-8 feet",
                            "discharge_time": "8-30 seconds",
                            "last_inspection": "2024-01-10"
                        }
                    ],
                    "2nd Floor": [
                        {
                            "location": "Near conference room", 
                            "type": "ABC Dry Chemical", 
                            "capacity": "10 lbs",
                            "effective_against": ["Class A", "Class B", "Class C"],
                            "range": "15-20 feet",
                            "discharge_time": "10-25 seconds",
                            "last_inspection": "2024-01-15"
                        },
                        {
                            "location": "Break room", 
                            "type": "ABC Dry Chemical", 
                            "capacity": "5 lbs",
                            "effective_against": ["Class A", "Class B", "Class C"],
                            "range": "8-12 feet", 
                            "discharge_time": "8-15 seconds",
                            "last_inspection": "2024-01-12"
                        },
                        {
                            "location": "Emergency exit", 
                            "type": "CO2", 
                            "capacity": "15 lbs",
                            "effective_against": ["Class B", "Class C"],
                            "range": "3-8 feet",
                            "discharge_time": "8-30 seconds",
                            "last_inspection": "2024-01-10"
                        }
                    ]
                },
                "fire_suppression_systems": {
                    "sprinkler_zones": {
                        "Ground Floor": ["Main lobby", "Kitchen", "Storage areas"],
                        "1st Floor": ["All patient rooms", "Corridors", "Nursing stations"],
                        "2nd Floor": ["Conference rooms", "Administrative offices", "Break areas"]
                    },
                    "smoke_detection": {
                        "Ground Floor": ["All rooms", "Corridors", "Electrical room"],
                        "1st Floor": ["Patient rooms", "Corridors", "Medical equipment rooms"],
                        "2nd Floor": ["All offices", "Conference rooms", "Storage areas"]
                    },
                    "fire_alarm_panels": {
                        "Ground Floor": "Main security desk",
                        "1st Floor": "Nursing station",
                        "2nd Floor": "Administrative office"
                    }
                },
                "evacuation_routes": {
                    "Ground Floor": {
                        "primary": "Main entrance (front)",
                        "secondary": "Back exit (parking lot)",
                        "capacity": "350 people total",
                        "estimated_time": "3-5 minutes"
                    },
                    "1st Floor": {
                        "primary": "Emergency stairwell A (east)",
                        "secondary": "Emergency stairwell B (west)", 
                        "capacity": "200 people total",
                        "estimated_time": "5-8 minutes"
                    },
                    "2nd Floor": {
                        "primary": "Emergency stairwell A (east)",
                        "secondary": "Emergency stairwell B (west)",
                        "tertiary": "Fire escape (north side)",
                        "capacity": "200 people total",
                        "estimated_time": "8-12 minutes"
                    }
                },
                "assembly_points": [
                    {
                        "name": "Primary Assembly Point - Parking Lot",
                        "capacity": "400 people",
                        "distance": "100m from building",
                        "safety_features": ["Open space", "Away from building", "Vehicle access for emergency services"],
                        "wind_considerations": "Upwind from building"
                    },
                    {
                        "name": "Secondary Assembly Point - Front Courtyard", 
                        "capacity": "200 people",
                        "distance": "50m from building",
                        "safety_features": ["Open space", "Near road access"],
                        "wind_considerations": "Check wind direction"
                    }
                ],
                "fire_hazards": {
                    "Ground Floor": [
                        {"hazard": "High voltage electrical equipment", "location": "Server room", "risk": "Electrical fire, explosion"},
                        {"hazard": "Natural gas lines", "location": "Kitchen area", "risk": "Gas explosion, flash fire"},
                        {"hazard": "Medical oxygen tanks", "location": "Storage room", "risk": "Accelerated combustion"}
                    ],
                    "1st Floor": [
                        {"hazard": "Medical oxygen supply system", "location": "Throughout floor", "risk": "Accelerated combustion"},
                        {"hazard": "Flammable chemicals", "location": "Chemical storage", "risk": "Toxic fumes, explosion"},
                        {"hazard": "Lithium batteries", "location": "Server room", "risk": "Thermal runaway, toxic gases"}
                    ],
                    "2nd Floor": [
                        {"hazard": "Diesel fuel", "location": "Generator room", "risk": "Fuel fire, explosion"},
                        {"hazard": "Propane tanks", "location": "Heating system", "risk": "Gas explosion"},
                        {"hazard": "Laboratory chemicals", "location": "Chemical lab", "risk": "Toxic fumes, chemical reactions"}
                    ]
                },
                "emergency_contacts": {
                    "fire_department": "911",
                    "building_security": "+234-800-SECURITY", 
                    "facility_manager": "+234-800-FACILITY",
                    "fire_safety_officer": "+234-800-FIRESAFE"
                }
            }
        }
        
        # Fire safety protocols
        self.fire_protocols = {
            "PASS_technique": {
                "P": "Pull the pin",
                "A": "Aim at the base of the fire", 
                "S": "Squeeze the handle",
                "S": "Sweep side to side"
            },
            "fire_size_assessment": {
                "small": "Smaller than a wastepaper basket - may attempt suppression",
                "medium": "Larger than wastepaper basket but smaller than a person - caution required",
                "large": "Larger than a person - evacuate immediately, do not attempt suppression"
            },
            "smoke_safety": {
                "stay_low": "Crawl below smoke level (heat and toxic gases rise)",
                "test_doors": "Feel door handles before opening (hot = fire behind)",
                "close_doors": "Close doors behind you to slow fire spread"
            }
        }
    
    def call_gemini(self, user_message):
        """Call Gemini 3 API with specialized fire safety context - GEMINI ONLY with retry logic"""
        max_retries = 3
        retry_delay = 2  # seconds
        
        for attempt in range(max_retries):
            try:
                # Build fire-specific context
                context_prompt = self.build_fire_context_prompt(user_message)
                
                # Create Python script for Gemini API call
                script_content = f'''
import google.genai as genai
import time

api_key = "{self.api_key}"
client = genai.Client(api_key=api_key)

prompt = """{context_prompt}"""

try:
    result = client.models.generate_content(
        model='models/gemini-3-flash-preview',
        contents=[prompt]
    )
    print(result.text.strip())
except Exception as e:
    print(f"GEMINI_ERROR: {{str(e)}}")
'''
                
                # Write script to temp file and execute
                with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as f:
                    f.write(script_content)
                    temp_script = f.name
                
                # Run script
                result = subprocess.run(
                    [sys.executable, temp_script],
                    capture_output=True,
                    text=True,
                    timeout=30,
                    cwd=os.getcwd()
                )
                
                # Clean up temp file
                os.unlink(temp_script)
                
                if result.returncode == 0:
                    response = result.stdout.strip()
                    if response and not response.startswith("GEMINI_ERROR:"):
                        return response
                    else:
                        # Check if it's a 503 overload error
                        if "503" in response or "overloaded" in response.lower():
                            if attempt < max_retries - 1:
                                print(f"🔄 Gemini overloaded, retrying in {retry_delay} seconds... (attempt {attempt + 1}/{max_retries})")
                                time.sleep(retry_delay)
                                retry_delay *= 2  # Exponential backoff
                                continue
                            else:
                                return f"🚨 GEMINI TEMPORARILY OVERLOADED: The AI system is experiencing high demand. Please wait a moment and try again, or call 911 for immediate emergency assistance."
                        else:
                            # Other Gemini error
                            error_msg = response.replace("GEMINI_ERROR: ", "") if response.startswith("GEMINI_ERROR:") else "Unknown Gemini error"
                            return f"🚨 GEMINI API ERROR: {error_msg}\n\n❌ Fire Emergency Agent requires Gemini 3 to function. Please resolve API issues."
                else:
                    if attempt < max_retries - 1:
                        print(f"🔄 Gemini connection failed, retrying... (attempt {attempt + 1}/{max_retries})")
                        time.sleep(retry_delay)
                        retry_delay *= 2
                        continue
                    else:
                        return f"🚨 GEMINI CONNECTION FAILED: {result.stderr}\n\n❌ Fire Emergency Agent is Gemini-powered only. Cannot provide guidance without Gemini."
                        
            except Exception as e:
                if attempt < max_retries - 1:
                    print(f"🔄 Gemini system error, retrying... (attempt {attempt + 1}/{max_retries})")
                    time.sleep(retry_delay)
                    retry_delay *= 2
                    continue
                else:
                    return f"🚨 GEMINI SYSTEM ERROR: {str(e)}\n\n❌ Fire Emergency Agent requires Gemini 3. Please check API configuration and quota."
        
        # This shouldn't be reached, but just in case
        return "🚨 GEMINI UNAVAILABLE: Unable to connect to AI system after multiple attempts. Please call 911 for emergency assistance."
    
    def build_fire_context_prompt(self, user_message):
        """Build specialized fire safety context prompt for Gemini"""
        
        # Fire emergency context
        emergency_info = f"""
FIRE EMERGENCY SITUATION:
- Type: {self.test_emergency['emergency_type']}
- Location: {self.test_emergency['building']}
- Floor Affected: {self.test_emergency.get('floor_affected', 'Unknown')}
- Time: {self.test_emergency['timestamp']}
- Status: ACTIVE FIRE - Immediate response required
"""
        
        # User location and fire assessment
        location_info = ""
        if self.user_location:
            location_info = f"""
USER LOCATION:
- Building: {self.user_location['building']}
- Floor: {self.user_location['floor']}
"""
        else:
            location_info = "USER LOCATION: Unknown - CRITICAL to determine for fire safety"
        
        # Fire assessment
        fire_assessment_info = f"""
FIRE ASSESSMENT:
- Size: {self.fire_assessment['size']}
- Type: {self.fire_assessment['type']}
- Location: {self.fire_assessment['location']}
- Spreading: {self.fire_assessment['spreading']}
- Smoke Level: {self.fire_assessment['smoke_level']}
"""
        
        # Building fire safety data
        building_data = f"""
FIRE SAFETY BUILDING DATA:
{json.dumps(self.building_layout, indent=2)}
"""
        
        # Fire safety protocols
        protocols_data = f"""
FIRE SAFETY PROTOCOLS:
{json.dumps(self.fire_protocols, indent=2)}
"""
        
        # Conversation history
        history_context = ""
        if self.conversation_history:
            recent_history = self.conversation_history[-8:]  # Last 8 exchanges for fire context
            history_context = f"""
CONVERSATION HISTORY:
{chr(10).join(recent_history)}
"""
        
        # Message analysis
        message_analysis = self.analyze_fire_message(user_message)
        
        # Full specialized fire prompt
        full_prompt = f"""You are AlertAI Fire Emergency Specialist providing STEP-BY-STEP interactive fire safety guidance. You must guide the user through ONE STEP AT A TIME, waiting for confirmation before proceeding.

{emergency_info}
{location_info}
{fire_assessment_info}
{building_data}
{protocols_data}
{history_context}

MESSAGE ANALYSIS:
{message_analysis}

CURRENT USER MESSAGE: "{user_message}"

STEP-BY-STEP GUIDANCE RULES:
1. **ONE STEP ONLY**: Give only ONE clear, specific action per response
2. **SHORT & FOCUSED**: Maximum 2-3 sentences with essential information only
3. **WAIT FOR CONFIRMATION**: Always end with "Confirm when done" or ask for status
4. **LOCATION-BASED LOGIC**: 
   - Step 1: Get user location only
   - If user is NOT on fire floor: Direct evacuation immediately
   - If user IS on fire floor: Then assess fire size and proximity
5. **USE BUILDING DATA**: Reference specific locations, equipment, routes from building data
6. **CRITICAL INFO ONLY**: Include only essential safety information for current step

INTELLIGENT STEP-BY-STEP FIRE EMERGENCY SEQUENCE:
Step 1: Get user location (floor and general area)
Step 2A: If user NOT on fire floor → Direct evacuation route immediately
Step 2B: If user ON fire floor → Assess fire size and proximity to user
Step 3A: If far from fire on same floor → Evacuation with caution
Step 3B: If close to fire → Suppress vs evacuate decision based on fire size
Step 4: Execute chosen action (evacuation or suppression)
Step 5: Safety confirmation and next action
Step 6: Final safety verification at assembly point

LOCATION LOGIC:
- Fire is on: {self.test_emergency.get('floor_affected', '1st Floor')}
- If user on different floor: Immediate evacuation guidance
- If user on same floor: Check proximity and fire size before deciding

RESPONSE FORMAT:
- Start with current step number
- Give ONE specific action with essential details
- End with confirmation request
- Keep response under 50 words when possible

EXAMPLE GOOD RESPONSES:
If first contact: "STEP 1: What floor are you on right now? Just tell me your floor - Ground Floor, 1st Floor, or 2nd Floor. Respond immediately."

If user NOT on fire floor: "STEP 2: You're safe from direct fire. Go to [specific stairwell] immediately and evacuate to parking lot. Do NOT use elevators. Confirm when moving."

If user ON fire floor: "STEP 2: You're on the fire floor. Can you see or smell the fire from where you are? How close does it seem? Respond quickly."

RESPOND WITH NEXT STEP ONLY:"""

        return full_prompt
    
    def analyze_fire_message(self, message):
        """Analyze user message for fire-specific context and urgency"""
        message_lower = message.lower()
        analysis = []
        
        # Fire fighting intent
        if any(word in message_lower for word in ["fight", "extinguish", "put out", "stop", "suppress", "tackle"]):
            analysis.append("🔥 INTENT: User wants to fight/suppress the fire")
        elif any(word in message_lower for word in ["evacuate", "leave", "exit", "escape", "get out", "run"]):
            analysis.append("🚨 INTENT: User wants to evacuate")
        elif any(word in message_lower for word in ["where", "location", "floor", "room"]):
            analysis.append("📍 INTENT: Location inquiry or providing location")
        elif any(word in message_lower for word in ["scared", "afraid", "panic", "help", "don't know", "confused"]):
            analysis.append("😰 INTENT: User is distressed - needs calm guidance")
        elif any(word in message_lower for word in ["extinguisher", "equipment", "tools", "hose"]):
            analysis.append("🧯 INTENT: Asking about fire suppression equipment")
        
        # Fire size assessment
        if any(word in message_lower for word in ["small", "tiny", "little", "wastepaper", "trash can"]):
            analysis.append("🔥 FIRE SIZE: Small - suppression may be possible")
            self.fire_assessment['size'] = "small"
        elif any(word in message_lower for word in ["big", "large", "huge", "spreading", "growing"]):
            analysis.append("🔥 FIRE SIZE: Large - evacuation recommended")
            self.fire_assessment['size'] = "large"
        elif any(word in message_lower for word in ["medium", "moderate", "person-sized"]):
            analysis.append("🔥 FIRE SIZE: Medium - caution required")
            self.fire_assessment['size'] = "medium"
        
        # Fire type detection
        if any(word in message_lower for word in ["electrical", "wires", "outlet", "computer", "equipment"]):
            analysis.append("⚡ FIRE TYPE: Electrical (Class C) - Use CO2 or ABC extinguisher")
            self.fire_assessment['type'] = "electrical"
        elif any(word in message_lower for word in ["grease", "oil", "kitchen", "cooking", "fat"]):
            analysis.append("🍳 FIRE TYPE: Grease/Oil (Class K) - Use Class K extinguisher")
            self.fire_assessment['type'] = "grease"
        elif any(word in message_lower for word in ["paper", "wood", "fabric", "trash", "ordinary"]):
            analysis.append("📄 FIRE TYPE: Ordinary combustibles (Class A) - Use ABC extinguisher")
            self.fire_assessment['type'] = "ordinary"
        elif any(word in message_lower for word in ["liquid", "gasoline", "alcohol", "solvent"]):
            analysis.append("🛢️ FIRE TYPE: Flammable liquid (Class B) - Use ABC or CO2 extinguisher")
            self.fire_assessment['type'] = "liquid"
        
        # Smoke level
        if any(word in message_lower for word in ["smoke", "smoky", "can't see", "visibility"]):
            analysis.append("💨 SMOKE DETECTED: Stay low, test doors, consider evacuation")
            self.fire_assessment['smoke_level'] = "present"
        
        # Location detection
        if any(word in message_lower for word in ["ground floor", "ground", "lobby", "entrance", "kitchen"]):
            analysis.append("📍 LOCATION: Ground Floor")
        elif any(word in message_lower for word in ["first floor", "1st floor", "floor 1", "patient", "medical"]):
            analysis.append("📍 LOCATION: 1st Floor")
        elif any(word in message_lower for word in ["second floor", "2nd floor", "floor 2", "office", "conference"]):
            analysis.append("📍 LOCATION: 2nd Floor")
        
        # Urgency assessment
        if any(word in message_lower for word in ["emergency", "urgent", "quickly", "fast", "now", "spreading", "getting worse"]):
            analysis.append("🚨 URGENCY: HIGH - Immediate action required")
        
        return "; ".join(analysis) if analysis else "General fire emergency inquiry"
    
    def speak(self, text):
        """Display fire specialist response and add to conversation history"""
        print(f"🔥 Fire Specialist: {text}")
        self.conversation_history.append(f"Fire Specialist: {text}")
    
    def get_user_input(self, prompt=""):
        """Get text input from user and add to conversation history"""
        if prompt:
            print(f"❓ {prompt}")
        try:
            user_input = input("👤 You: ").strip()
            self.conversation_history.append(f"User: {user_input}")
            return user_input
        except KeyboardInterrupt:
            return "quit"
        except Exception:
            return ""
    
    def parse_user_location(self, user_input):
        """Parse and store user location for fire safety context"""
        building = self.test_emergency['building']
        floor = "Ground Floor"  # default
        
        user_lower = user_input.lower()
        
        # Check for floor mentions
        if "first floor" in user_lower or "1st floor" in user_lower or "floor 1" in user_lower:
            floor = "1st Floor"
        elif "second floor" in user_lower or "2nd floor" in user_lower or "floor 2" in user_lower:
            floor = "2nd Floor"
        elif "ground floor" in user_lower or "ground" in user_lower:
            floor = "Ground Floor"
        
        self.user_location = {"building": building, "floor": floor}
        print(f"📍 Location confirmed: {building}, {floor}")
        
        # Provide immediate fire safety info for their floor
        self.provide_floor_fire_info(floor)
    
    def provide_floor_fire_info(self, floor):
        """Provide immediate fire safety information for user's floor"""
        if floor in self.building_layout["Medical Center Building A"]["fire_extinguishers"]:
            extinguishers = self.building_layout["Medical Center Building A"]["fire_extinguishers"][floor]
            print(f"🧯 Fire extinguishers on {floor}:")
            for ext in extinguishers:
                print(f"   • {ext['location']}: {ext['type']} ({ext['capacity']})")
        
        if floor in self.building_layout["Medical Center Building A"]["evacuation_routes"]:
            routes = self.building_layout["Medical Center Building A"]["evacuation_routes"][floor]
            print(f"🚪 Evacuation routes from {floor}:")
            print(f"   • Primary: {routes['primary']}")
            if 'secondary' in routes:
                print(f"   • Secondary: {routes['secondary']}")
    
    def start_fire_emergency_scenario(self):
        """Start the fire emergency scenario with specialized guidance"""
        emergency = self.test_emergency
        
        print(f"\n🔥 FIRE EMERGENCY DETECTED!")
        print(f"Building: {emergency['building']}")
        print(f"Floor Affected: {emergency.get('floor_affected', 'Unknown')}")
        print("🚨 FIRE SPECIALIST ACTIVATED")
        print("=" * 60)
        
        # Get initial step-by-step fire specialist response
        initial_message = f"FIRE EMERGENCY at {emergency['building']} on {emergency.get('floor_affected', 'unknown floor')}! Start step-by-step fire safety guidance immediately."
        
        print(f"👤 You: {initial_message}")
        response = self.call_gemini(initial_message)
        self.speak(response)
        
        # Start specialized fire conversation
        self.fire_conversation_loop()
    
    def fire_conversation_loop(self):
        """Specialized fire emergency conversation loop"""
        print("\n🔥 STEP-BY-STEP Fire Emergency Guidance Active")
        print("🚨 Follow each step carefully and confirm completion before next step")
        print("� Type your response to each step. Type 'quit' to exit, 'restart' for new scenario.")
        print("=" * 80)
        
        while True:
            try:
                # Get user input
                user_input = self.get_user_input()
                
                if user_input.lower() in ["quit", "exit", "stop"]:
                    final_message = "Ending fire emergency session. REMEMBER: Call 911, ensure you're safe, evacuate if fire is spreading."
                    response = self.call_gemini(final_message)
                    self.speak(response)
                    break
                
                if user_input.lower() in ["restart", "again", "new"]:
                    self.restart_fire_scenario()
                    break
                
                if not user_input.strip():
                    continue
                
                # Update location if mentioned
                if not self.user_location and any(word in user_input.lower() for word in ["floor", "building", "room", "area", "ground", "first", "second"]):
                    self.parse_user_location(user_input)
                
                # Get specialized fire response from Gemini
                response = self.call_gemini(user_input)
                self.speak(response)
                
            except KeyboardInterrupt:
                print("\n🛑 Fire emergency session interrupted")
                print("🚨 SAFETY REMINDER: If fire is present, evacuate immediately and call 911")
                break
            except Exception as e:
                print(f"❌ Error in fire emergency session: {e}")
                self.speak("🚨 GEMINI ERROR: Fire Emergency Agent requires Gemini 3 to function. Cannot provide guidance without AI.")
                break
    
    def restart_fire_scenario(self):
        """Restart the fire emergency scenario"""
        print("\n🔄 RESTARTING FIRE EMERGENCY SCENARIO...")
        
        # Reset fire assessment
        self.conversation_history = []
        self.user_location = None
        self.current_step = 1
        self.emergency_phase = "assessment"
        self.fire_assessment = {
            "size": "unknown",
            "type": "unknown", 
            "location": "unknown",
            "spreading": "unknown",
            "smoke_level": "unknown",
            "user_proximity": "unknown"
        }
        
        # Wait a moment
        time.sleep(2)
        
        # Start new fire scenario
        self.start_fire_emergency_scenario()
    
    def check_for_fire_emergencies(self):
        """Monitor AlertAI server for fire emergencies only"""
        try:
            response = requests.get(f"{self.server_url}/api/alerts/active", timeout=5)
            if response.status_code == 200:
                data = response.json()
                alerts = data.get('alerts', [])
                
                # Filter for fire emergencies only
                fire_alerts = [alert for alert in alerts if alert.get('emergency_type', '').lower() == 'fire']
                
                if fire_alerts:
                    # Check for new fire emergencies
                    for fire_alert in fire_alerts:
                        if not self.current_fire_emergency or fire_alert['id'] != self.current_fire_emergency.get('id'):
                            print(f"\n🔥 NEW FIRE EMERGENCY DETECTED FROM SERVER!")
                            print(f"ID: {fire_alert['id']}")
                            print(f"Type: {fire_alert['emergency_type']}")
                            print(f"Location: {fire_alert['building']}")
                            print(f"Time: {fire_alert['timestamp']}")
                            print("=" * 60)
                            
                            # Replace test emergency with real fire emergency
                            self.current_fire_emergency = fire_alert
                            self.test_emergency = fire_alert  # Use real data instead of test
                            return True
                else:
                    # No fire emergencies active
                    if self.current_fire_emergency:
                        print("🔥 Fire emergency resolved. Monitoring for new fire emergencies...")
                        self.current_fire_emergency = None
                        
        except Exception as e:
            print(f"❌ Error checking for fire emergencies: {e}")
        
        return False
    
    def start_monitoring_mode(self):
        """Start monitoring AlertAI server for fire emergencies"""
        print("🔥 FIRE EMERGENCY MONITORING MODE")
        print("=" * 60)
        print("🚒 Monitoring AlertAI server for FIRE emergencies only")
        print("🔄 Checking server every 10 seconds")
        print("🚨 Will activate fire specialist when fire is detected")
        print("💬 Press Ctrl+C to stop monitoring")
        print("=" * 60)
        
        self.is_monitoring = True
        
        while self.is_monitoring:
            try:
                # Check for fire emergencies
                if self.check_for_fire_emergencies():
                    # Fire emergency detected - start guidance
                    self.start_fire_emergency_scenario()
                    # After guidance session, continue monitoring
                    continue
                
                # Show monitoring status
                if not self.current_fire_emergency:
                    print("🔥 Monitoring for fire emergencies... (Ctrl+C to stop)")
                    time.sleep(10)
                    
            except KeyboardInterrupt:
                print("\n🛑 Fire emergency monitoring stopped by user")
                self.is_monitoring = False
                break
            except Exception as e:
                print(f"❌ Monitoring error: {e}")
                time.sleep(5)

def main():
    """Main function to start Fire Emergency Agent"""
    print("🔥 ALERTAI FIRE EMERGENCY SPECIALIST - GEMINI 3")
    print("=" * 70)
    print("🚒 Expert fire safety guidance and suppression protocols")
    print("🧯 Specialized fire extinguisher and evacuation knowledge")
    print("🏢 Building-specific fire safety data integration")
    print("🚨 PASS technique, fire classification, and safety procedures")
    print("=" * 70)
    
    try:
        print("🔄 Initializing Fire Emergency Agent...")
        agent = FireEmergencyAgent()
        print("✅ Agent initialized successfully!")
        
        # Choose mode
        print("\n🔥 FIRE EMERGENCY AGENT MODES:")
        print("1. 🧪 Test Mode - Use hardcoded fire scenario")
        print("2. 📡 Monitor Mode - Monitor AlertAI server for real fire emergencies")
        
        while True:
            try:
                choice = input("\nSelect mode (1 or 2): ").strip()
                if choice == "1":
                    print("🧪 Starting test fire emergency scenario...")
                    agent.start_fire_emergency_scenario()
                    break
                elif choice == "2":
                    print("📡 Starting fire emergency monitoring...")
                    agent.start_monitoring_mode()
                    break
                else:
                    print("❌ Invalid choice. Please enter 1 or 2.")
            except KeyboardInterrupt:
                print("\n👋 Fire Emergency Agent stopped by user")
                break
                
    except KeyboardInterrupt:
        print("\n👋 Fire emergency session ended by user")
        print("🚨 SAFETY REMINDER: Always call 911 for fire emergencies")
    except Exception as e:
        print(f"❌ Failed to start fire emergency agent: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()