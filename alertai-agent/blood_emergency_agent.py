#!/usr/bin/env python3
"""
AlertAI Blood Emergency Agent - Specialized Gemini 3
Expert bleeding control and trauma response using Gemini 3 with specialized medical protocols
"""
print("🩸 Starting Blood Emergency Agent...")
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

class BloodEmergencyAgent:
    def __init__(self):
        self.name = "AlertAI Blood Emergency Specialist"
        self.user_location = None
        self.building_layout = {}
        self.conversation_history = []
        self.emergency_context = {}
        self.medical_assessment = {
            "bleeding_severity": "unknown",
            "bleeding_location": "unknown", 
            "bleeding_type": "unknown",
            "consciousness": "unknown",
            "shock_signs": "unknown",
            "pressure_applied": "unknown",
            "medical_help_called": "unknown"
        }
        self.current_step = 1
        self.emergency_phase = "dispatch"  # dispatch, assessment, control, monitoring
        self.user_at_scene = False
        
        # Server monitoring for blood emergencies
        self.server_url = getattr(config, 'ALERTAI_SERVER_URL', 'http://localhost:8000')
        self.is_monitoring = False
        self.current_blood_emergency = None
        
        # Check for Gemini API key
        self.api_key = getattr(config, 'AI_API_KEY', '') or getattr(config, 'GEMINI_API_KEY', '')
        print(f"🔑 API Key loaded: {self.api_key[:20]}..." if self.api_key else "❌ No API key")
        if not self.api_key:
            print("❌ GEMINI_API_KEY not found in environment variables")
            sys.exit(1)
        
        # Blood emergency scenario for testing
        self.test_emergency = {
            "id": 5001,
            "emergency_type": "Blood",
            "building": "Medical Center Building A",
            "location": {"lat": 11.849010, "lon": 13.056751},
            "timestamp": datetime.now().isoformat(),
            "image_url": "test_images/blood_emergency.jpg",
            "floor_affected": "1st Floor",
            "room_location": "Nursing station"  # ✅ ADDED: Specific room where bleeding person is located
        }
        
        # Load specialized medical and building data
        self.load_medical_trauma_data()
        
        print(f"🩸 {self.name} initialized and ready!")
        print(f"🧠 Using Gemini 3 with specialized bleeding control protocols")
        print(f"🚑 Expert knowledge: Bleeding control, trauma response, shock prevention")
    
    def load_medical_trauma_data(self):
        """Load specialized medical trauma data and building information"""
        self.building_layout = {
            "Medical Center Building A": {
                "floors": ["Ground Floor", "1st Floor", "2nd Floor"],
                "medical_supplies": {
                    "Ground Floor": [
                        {
                            "supply": "Trauma Kit (Advanced)", 
                            "location": "Security office", 
                            "contents": ["Pressure bandages", "Hemostatic gauze", "Tourniquets", "Chest seals", "Emergency blankets"],
                            "quantity": "Full kit for 5 patients",
                            "last_restocked": "2024-01-20"
                        },
                        {
                            "supply": "AED with First Aid", 
                            "location": "Main reception", 
                            "contents": ["Basic bandages", "Antiseptic", "Gloves", "Face masks"],
                            "training_required": "Basic first aid knowledge"
                        },
                        {
                            "supply": "Emergency Blankets", 
                            "location": "Multiple locations", 
                            "quantity": "10 thermal blankets",
                            "use": "Shock prevention and warmth"
                        }
                    ],
                    "1st Floor": [
                        {
                            "supply": "Medical Grade Supplies", 
                            "location": "Nursing station", 
                            "contents": ["IV fluids", "Blood pressure cuffs", "Oxygen", "Advanced bandages", "Suture kits"],
                            "staff_access": "Trained medical personnel only"
                        },
                        {
                            "supply": "Hemorrhage Control Kit", 
                            "location": "Emergency supply room", 
                            "contents": ["Combat gauze", "Pressure dressings", "Tourniquets", "Hemostatic agents"],
                            "use": "Severe bleeding control"
                        },
                        {
                            "supply": "Patient Transport", 
                            "location": "Equipment room", 
                            "items": ["Stretchers", "Spine boards", "Wheelchairs"],
                            "capacity": "Multiple patients"
                        }
                    ],
                    "2nd Floor": [
                        {
                            "supply": "Basic First Aid Kit", 
                            "location": "Break room", 
                            "contents": ["Bandages", "Antiseptic wipes", "Gauze pads", "Medical tape"],
                            "accessibility": "All staff access"
                        },
                        {
                            "supply": "Emergency Communication", 
                            "location": "Administrative office", 
                            "equipment": ["Direct hospital line", "Emergency radio", "PA system"],
                            "use": "Medical emergency coordination"
                        }
                    ]
                },
                # ✅ ADDED: Same building layout as fire agent for consistency
                "building_areas": {
                    "Ground Floor": ["Main lobby", "Kitchen", "Storage areas", "Security office", "Main reception", "Electrical room"],
                    "1st Floor": ["All patient rooms", "Corridors", "Nursing stations", "Medical equipment rooms", "Emergency supply room", "Equipment room"],
                    "2nd Floor": ["Conference rooms", "Administrative offices", "Break areas", "Storage areas"]
                },
                "evacuation_routes": {
                    "Ground Floor": {
                        "primary": "Main entrance (front)",
                        "secondary": "Back exit (parking lot)",
                        "capacity": "350 people total",
                        "estimated_time": "3-5 minutes",
                        "ambulance_access": "Direct stretcher access via main entrance"
                    },
                    "1st Floor": {
                        "primary": "Emergency stairwell A (east)",
                        "secondary": "Emergency stairwell B (west)", 
                        "capacity": "200 people total",
                        "estimated_time": "5-8 minutes",
                        "medical_access": "Medical elevator to ambulance bay"
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
                        "medical_considerations": "Clear ambulance access"
                    },
                    {
                        "name": "Secondary Assembly Point - Front Courtyard", 
                        "capacity": "200 people",
                        "distance": "50m from building",
                        "safety_features": ["Open space", "Near road access"],
                        "medical_considerations": "Close to emergency services"
                    }
                ],
                "medical_personnel": {
                    "on_site_staff": [
                        {"role": "Registered Nurse", "location": "1st Floor nursing station", "availability": "24/7", "trauma_trained": True},
                        {"role": "EMT Certified Security", "location": "Ground Floor", "availability": "24/7", "bleeding_control": True},
                        {"role": "First Aid Certified Staff", "location": "Various floors", "availability": "Business hours", "basic_care": True}
                    ],
                    "emergency_response": {
                        "ems": "911 - Request trauma team for severe bleeding",
                        "hospital_direct": "+234-800-TRAUMA",
                        "poison_control": "1-800-222-1222",
                        "medical_director": "+234-800-MEDICAL"
                    }
                },
                "bleeding_hazards": {
                    "Ground Floor": [
                        {"hazard": "Glass doors and windows", "risk": "Laceration injuries", "mitigation": "Safety film applied"},
                        {"hazard": "Sharp furniture edges", "risk": "Impact injuries", "mitigation": "Padding on corners"}
                    ],
                    "1st Floor": [
                        {"hazard": "Medical equipment", "risk": "Sharp instruments", "mitigation": "Proper storage and handling"},
                        {"hazard": "Patient lifting", "risk": "Back injuries", "mitigation": "Mechanical lifts available"}
                    ],
                    "2nd Floor": [
                        {"hazard": "Office equipment", "risk": "Paper cuts, minor injuries", "mitigation": "Safety training provided"},
                        {"hazard": "Stairwell access", "risk": "Fall injuries", "mitigation": "Non-slip surfaces, handrails"}
                    ]
                }
            }
        }
        
        # Medical bleeding control protocols
        self.bleeding_protocols = {
            "bleeding_assessment": {
                "arterial": "Bright red, spurting blood - CRITICAL",
                "venous": "Dark red, steady flow - SERIOUS", 
                "capillary": "Slow oozing - MINOR",
                "internal": "No visible bleeding but shock signs - CRITICAL"
            },
            "bleeding_control_steps": {
                "1": "Apply direct pressure with clean cloth/gauze",
                "2": "Elevate injured area above heart if possible",
                "3": "Apply pressure bandage to maintain pressure",
                "4": "If bleeding continues, apply tourniquet above wound",
                "5": "Treat for shock - elevate legs, keep warm",
                "6": "Monitor breathing and consciousness continuously"
            },
            "shock_signs": {
                "early": ["Rapid pulse", "Pale skin", "Anxiety", "Thirst"],
                "moderate": ["Weak pulse", "Cold/clammy skin", "Confusion", "Nausea"],
                "severe": ["Very weak pulse", "Blue lips/fingernails", "Unconsciousness", "Shallow breathing"]
            },
            "tourniquet_use": {
                "when": "Severe limb bleeding that direct pressure cannot control",
                "placement": "2-3 inches above wound, never over joint",
                "tightness": "Tight enough to stop bleeding completely",
                "time": "Note exact time applied - critical for medical team"
            },
            "do_not": [
                "Remove embedded objects",
                "Give food or water to conscious patient",
                "Move patient unnecessarily", 
                "Remove blood-soaked bandages (add more on top)",
                "Use tourniquet for minor bleeding"
            ]
        }
    
    def call_gemini(self, user_message):
        """Call Gemini 3 API with specialized bleeding control context - GEMINI ONLY"""
        try:
            # Build medical bleeding-specific context
            context_prompt = self.build_bleeding_context_prompt(user_message)
            
            # Create Python script for Gemini API call
            script_content = f'''
import google.genai as genai

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
                    # Show actual Gemini error
                    error_msg = response.replace("GEMINI_ERROR: ", "") if response.startswith("GEMINI_ERROR:") else "Unknown Gemini error"
                    return f"🚨 GEMINI API ERROR: {error_msg}\n\n❌ Blood Emergency Agent requires Gemini 3 to function. Please resolve API issues."
            else:
                return f"🚨 GEMINI CONNECTION FAILED: {result.stderr}\n\n❌ Blood Emergency Agent is Gemini-powered only. Cannot provide guidance without Gemini."
                
        except Exception as e:
            return f"🚨 GEMINI SYSTEM ERROR: {str(e)}\n\n❌ Blood Emergency Agent requires Gemini 3. Please check API configuration and quota."
    
    def build_bleeding_context_prompt(self, user_message):
        """Build specialized bleeding control context prompt for Gemini"""
        
        # Blood emergency context
        emergency_info = f"""
BLOOD EMERGENCY SITUATION:
- Type: {self.test_emergency['emergency_type']}
- Location: {self.test_emergency['building']}
- Floor Affected: {self.test_emergency.get('floor_affected', 'Unknown')}
- Room Location: {self.test_emergency.get('room_location', 'Unknown room')}
- Time: {self.test_emergency['timestamp']}
- Status: ACTIVE BLEEDING EMERGENCY - Immediate medical response required
"""
        
        # User location and medical assessment
        location_info = ""
        if self.user_location:
            location_info = f"""
USER LOCATION:
- Building: {self.user_location['building']}
- Floor: {self.user_location['floor']}
"""
        else:
            location_info = "USER LOCATION: Unknown - CRITICAL to determine for medical response"
        
        # Medical bleeding assessment
        medical_assessment_info = f"""
BLEEDING ASSESSMENT STATUS:
- Emergency Phase: {self.emergency_phase}
- User At Scene: {self.user_at_scene}
- Bleeding Severity: {self.medical_assessment['bleeding_severity']}
- Bleeding Location: {self.medical_assessment['bleeding_location']}
- Bleeding Type: {self.medical_assessment['bleeding_type']}
- Consciousness: {self.medical_assessment['consciousness']}
- Shock Signs: {self.medical_assessment['shock_signs']}
- Pressure Applied: {self.medical_assessment['pressure_applied']}
- Medical Help Called: {self.medical_assessment['medical_help_called']}
"""
        
        # Building medical data
        building_data = f"""
MEDICAL BUILDING DATA:
{json.dumps(self.building_layout, indent=2)}
"""
        
        # Bleeding control protocols
        protocols_data = f"""
BLEEDING CONTROL PROTOCOLS:
{json.dumps(self.bleeding_protocols, indent=2)}
"""
        
        # Conversation history
        history_context = ""
        if self.conversation_history:
            recent_history = self.conversation_history[-8:]  # Last 8 exchanges for medical context
            history_context = f"""
CONVERSATION HISTORY:
{chr(10).join(recent_history)}
"""
        
        # Message analysis
        message_analysis = self.analyze_bleeding_message(user_message)
        
        # Full specialized bleeding prompt
        full_prompt = f"""You are AlertAI Blood Emergency Specialist, an expert trauma and bleeding control professional providing real-time guidance during bleeding emergencies. You have specialized knowledge of hemorrhage control, shock prevention, and emergency medical care.

{emergency_info}
{location_info}
{medical_assessment_info}
{building_data}
{protocols_data}
{history_context}

MESSAGE ANALYSIS:
{message_analysis}

CURRENT USER MESSAGE: "{user_message}"

STEP-BY-STEP GUIDANCE RULES:
1. **ONE STEP ONLY**: Give only ONE clear, specific action per response
2. **SHORT & FOCUSED**: Maximum 2-3 sentences with essential medical information only
3. **WAIT FOR CONFIRMATION**: Always end with "Confirm when done" or ask for status
4. **REALISTIC EMERGENCY FLOW**: 
   - Step 1: Direct user to go to bleeding person's EXACT location (floor + room)
   - Step 2: Confirm user has arrived and assess bleeding severity
   - Step 3: Begin bleeding control (direct pressure, elevation)
   - Step 4: Advanced control if needed (pressure bandage, tourniquet)
   - Step 5: Shock prevention and ongoing monitoring
5. **USE BUILDING DATA**: Reference specific medical supplies, trained personnel, evacuation routes
6. **LIFE SAFETY FIRST**: Stop bleeding immediately - time is critical

BLEEDING EMERGENCY SEQUENCE:
Step 1: Direct user to bleeding person's EXACT location (building + floor + room) with safety assessment
Step 2: Confirm arrival and immediate bleeding assessment (severity, location, type)
Step 3: Apply direct pressure with available materials
Step 4: Elevate bleeding area above heart if possible
Step 5: Apply pressure bandage or tourniquet if bleeding continues
Step 6: Treat for shock and monitor vital signs
Step 7: Coordinate with medical personnel and emergency services

CRITICAL BLEEDING CONTROL RULES:
- Apply direct pressure immediately - every second counts
- Use cleanest available material for pressure
- Do NOT remove blood-soaked bandages - add more on top
- Elevate bleeding area above heart level if no spinal injury
- Apply tourniquet only for severe limb bleeding
- Treat for shock - elevate legs, keep warm
- Never remove embedded objects
- Call 911 immediately for severe bleeding
- Monitor breathing and consciousness continuously

CPR GUIDANCE PROTOCOL:
- If person is NOT BREATHING and NO PULSE: CPR is needed immediately
- If trained person available: Direct them to start CPR immediately
- If NO trained person available: Say "If no one here is trained in CPR, tap the CPR Monitor button so the AI can guide you through chest compressions and follow the beeping sound in the CPR monitor"
- CPR is 30 chest compressions followed by 2 rescue breaths
- Compression rate: 100-120 per minute (follow the beep)
- Push hard and fast on center of chest
- Allow complete chest recoil between compressions
- Continue CPR while controlling bleeding if possible

RESPONSE STYLE:
- Be calm but urgent about bleeding control
- Use specific building medical data (supplies, trained staff, evacuation routes)
- Provide clear step-by-step bleeding control instructions
- Ask critical assessment questions (bleeding severity, consciousness, shock signs)
- Include specific medical supply locations and trained personnel
- Reference available trauma equipment and emergency contacts

EXAMPLE RESPONSES FOR BLEEDING EMERGENCY:
Initial dispatch: "STEP 1: Someone is bleeding at [building location] on [floor] in the [room_location]. Go to [specific room] on [floor] immediately. Look for any hazards as you approach. Confirm when you can see the person."

Arrival assessment: "STEP 2: Can you see the person and the bleeding? Describe the bleeding - is it spurting bright red, flowing dark red, or slow oozing? How much blood do you see? Do NOT touch them yet."

Bleeding control: "STEP 3: Apply direct pressure to the bleeding area immediately. Use clean cloth, gauze, or your hands if nothing else available. Press firmly and continuously. Confirm when pressure applied."

Advanced control: "STEP 4: Bleeding is severe. Get trauma kit from [location] if available, or apply tourniquet 2-3 inches above wound. Tighten until bleeding stops completely. Note the time. Confirm when done."

RESPOND WITH NEXT MEDICAL STEP ONLY:"""

        return full_prompt
    
    def analyze_bleeding_message(self, message):
        """Analyze user message for bleeding-specific context and urgency"""
        message_lower = message.lower()
        analysis = []
        
        # Scene arrival detection
        if any(word in message_lower for word in ["i can see", "i see", "i'm here", "arrived", "at the person", "found them"]):
            analysis.append("ARRIVAL: User has arrived at scene")
            self.user_at_scene = True
            self.emergency_phase = "assessment"
        elif any(word in message_lower for word in ["going", "on my way", "heading", "walking"]):
            analysis.append("DISPATCH: User is en route to bleeding person")
            self.emergency_phase = "dispatch"
        
        # Bleeding severity assessment
        if any(word in message_lower for word in ["spurting", "gushing", "arterial", "bright red", "pulsing"]):
            analysis.append("BLEEDING: Arterial bleeding - CRITICAL, immediate pressure needed")
            self.medical_assessment['bleeding_severity'] = "critical"
            self.medical_assessment['bleeding_type'] = "arterial"
        elif any(word in message_lower for word in ["flowing", "steady", "dark red", "venous"]):
            analysis.append("BLEEDING: Venous bleeding - SERIOUS, apply pressure")
            self.medical_assessment['bleeding_severity'] = "serious"
            self.medical_assessment['bleeding_type'] = "venous"
        elif any(word in message_lower for word in ["oozing", "slow", "minor", "small amount"]):
            analysis.append("BLEEDING: Minor bleeding - apply basic first aid")
            self.medical_assessment['bleeding_severity'] = "minor"
            self.medical_assessment['bleeding_type'] = "capillary"
        elif any(word in message_lower for word in ["lot of blood", "pool of blood", "severe", "heavy"]):
            analysis.append("BLEEDING: Severe blood loss - immediate intervention needed")
            self.medical_assessment['bleeding_severity'] = "severe"
        
        # Bleeding location
        if any(word in message_lower for word in ["head", "scalp", "face"]):
            analysis.append("LOCATION: Head/face bleeding - be careful of spinal injury")
            self.medical_assessment['bleeding_location'] = "head"
        elif any(word in message_lower for word in ["arm", "hand", "wrist", "finger"]):
            analysis.append("LOCATION: Arm/hand bleeding - elevation possible")
            self.medical_assessment['bleeding_location'] = "arm"
        elif any(word in message_lower for word in ["leg", "foot", "thigh", "ankle"]):
            analysis.append("LOCATION: Leg bleeding - tourniquet may be needed")
            self.medical_assessment['bleeding_location'] = "leg"
        elif any(word in message_lower for word in ["chest", "abdomen", "torso", "stomach"]):
            analysis.append("LOCATION: Torso bleeding - possible internal injury")
            self.medical_assessment['bleeding_location'] = "torso"
        
        # Consciousness assessment
        if any(word in message_lower for word in ["unconscious", "unresponsive", "passed out", "not awake"]):
            analysis.append("CONSCIOUSNESS: Person unconscious - check breathing, possible shock")
            self.medical_assessment['consciousness'] = "unconscious"
        elif any(word in message_lower for word in ["awake", "conscious", "talking", "alert"]):
            analysis.append("CONSCIOUSNESS: Person conscious - good sign")
            self.medical_assessment['consciousness'] = "conscious"
        elif any(word in message_lower for word in ["confused", "dazed", "weak", "dizzy"]):
            analysis.append("CONSCIOUSNESS: Altered consciousness - possible shock")
            self.medical_assessment['consciousness'] = "altered"
        
        # Shock signs
        if any(word in message_lower for word in ["pale", "cold", "clammy", "weak pulse", "rapid pulse"]):
            analysis.append("SHOCK: Signs of shock present - elevate legs, keep warm")
            self.medical_assessment['shock_signs'] = "present"
        elif any(word in message_lower for word in ["blue lips", "blue fingers", "very weak"]):
            analysis.append("SHOCK: Severe shock signs - critical condition")
            self.medical_assessment['shock_signs'] = "severe"
        
        # Pressure application
        if any(word in message_lower for word in ["applied pressure", "pressing", "holding", "bandage on"]):
            analysis.append("PRESSURE: Pressure being applied to bleeding")
            self.medical_assessment['pressure_applied'] = "yes"
        elif any(word in message_lower for word in ["still bleeding", "won't stop", "bleeding through"]):
            analysis.append("PRESSURE: Bleeding continues despite pressure - need advanced control")
            self.medical_assessment['pressure_applied'] = "insufficient"
        
        # Medical help status
        if any(word in message_lower for word in ["called 911", "ambulance coming", "ems called"]):
            analysis.append("MEDICAL HELP: Emergency services contacted")
            self.medical_assessment['medical_help_called'] = "yes"
        elif any(word in message_lower for word in ["need to call", "should I call", "haven't called"]):
            analysis.append("MEDICAL HELP: Need to contact emergency services")
            self.medical_assessment['medical_help_called'] = "no"
        
        # CPR-related keywords detection
        if any(word in message_lower for word in ["not breathing", "no pulse", "cardiac arrest", "heart stopped", "cpr", "chest compressions"]):
            analysis.append("CPR NEEDED: Person requires immediate CPR - recommend CPR monitor if no trained person available")
        
        # Location detection
        if any(word in message_lower for word in ["ground floor", "ground", "lobby", "entrance"]):
            analysis.append("LOCATION: Ground Floor - trauma kit and EMT security available")
        elif any(word in message_lower for word in ["first floor", "1st floor", "floor 1", "nursing"]):
            analysis.append("LOCATION: 1st Floor - medical grade supplies and trained nurse available")
        elif any(word in message_lower for word in ["second floor", "2nd floor", "floor 2", "office"]):
            analysis.append("LOCATION: 2nd Floor - basic first aid and emergency communication available")
        
        # Urgency assessment
        if any(word in message_lower for word in ["emergency", "urgent", "critical", "dying", "losing blood"]):
            analysis.append("URGENCY: CRITICAL - Life-threatening bleeding emergency")
        
        return "; ".join(analysis) if analysis else "General bleeding emergency inquiry"
    
    def speak(self, text):
        """Display blood emergency specialist response and add to conversation history"""
        print(f"🩸 Blood Specialist: {text}")
        self.conversation_history.append(f"Blood Specialist: {text}")
    
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
        """Parse and store user location for medical response context"""
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
        
        # Provide immediate medical supply info for their floor
        self.provide_floor_medical_info(floor)
    
    def provide_floor_medical_info(self, floor):
        """Provide immediate medical supply information for user's floor"""
        if floor in self.building_layout["Medical Center Building A"]["medical_supplies"]:
            supplies = self.building_layout["Medical Center Building A"]["medical_supplies"][floor]
            print(f"🩸 Medical supplies on {floor}:")
            for supply in supplies:
                print(f"   • {supply['supply']}: {supply['location']}")
        
        # Show trained personnel if available
        personnel = self.building_layout["Medical Center Building A"]["medical_personnel"]["on_site_staff"]
        available_staff = [staff for staff in personnel if floor.lower() in staff['location'].lower() or staff['availability'] == '24/7']
        if available_staff:
            print(f"👨‍⚕️ Trained medical staff available:")
            for staff in available_staff:
                print(f"   • {staff['role']}: {staff['location']}")
    
    def check_for_blood_emergencies(self):
        """Monitor AlertAI server for blood emergencies only"""
        try:
            response = requests.get(f"{self.server_url}/api/alerts/active", timeout=5)
            if response.status_code == 200:
                data = response.json()
                alerts = data.get('alerts', [])
                
                # Filter for blood emergencies only
                blood_alerts = [alert for alert in alerts if alert.get('emergency_type', '').lower() == 'blood']
                
                if blood_alerts:
                    # Check for new blood emergencies
                    for blood_alert in blood_alerts:
                        if not self.current_blood_emergency or blood_alert['id'] != self.current_blood_emergency.get('id'):
                            print(f"\n🩸 NEW BLOOD EMERGENCY DETECTED FROM SERVER!")
                            print(f"ID: {blood_alert['id']}")
                            print(f"Type: {blood_alert['emergency_type']}")
                            print(f"Location: {blood_alert['building']}")
                            print(f"Floor: {blood_alert.get('floor_affected', 'Unknown')}")
                            print(f"Time: {blood_alert['timestamp']}")
                            print("=" * 60)
                            
                            # Replace test emergency with real blood emergency
                            self.current_blood_emergency = blood_alert
                            self.test_emergency = blood_alert  # Use real data instead of test
                            return True
                else:
                    # No blood emergencies active
                    if self.current_blood_emergency:
                        print("🩸 Blood emergency resolved. Monitoring for new bleeding emergencies...")
                        self.current_blood_emergency = None
                        
        except Exception as e:
            print(f"❌ Error checking for blood emergencies: {e}")
        
        return False
    
    def start_monitoring_mode(self):
        """Start monitoring AlertAI server for blood emergencies"""
        print("🩸 BLOOD EMERGENCY MONITORING MODE")
        print("=" * 60)
        print("🚑 Monitoring AlertAI server for BLOOD emergencies only")
        print("🔄 Checking server every 10 seconds")
        print("🚨 Will activate blood specialist when bleeding is detected")
        print("💬 Press Ctrl+C to stop monitoring")
        print("=" * 60)
        
        self.is_monitoring = True
        
        while self.is_monitoring:
            try:
                # Check for blood emergencies
                if self.check_for_blood_emergencies():
                    # Blood emergency detected - start medical guidance
                    self.start_blood_emergency_scenario()
                    # After guidance session, continue monitoring
                    continue
                
                # Show monitoring status
                if not self.current_blood_emergency:
                    print("🩸 Monitoring for blood emergencies... (Ctrl+C to stop)")
                    time.sleep(10)
                    
            except KeyboardInterrupt:
                print("\n🛑 Blood emergency monitoring stopped by user")
                self.is_monitoring = False
                break
            except Exception as e:
                print(f"❌ Monitoring error: {e}")
                time.sleep(5)
    
    def start_blood_emergency_scenario(self):
        """Start the blood emergency scenario with specialized medical guidance"""
        emergency = self.test_emergency
        
        print(f"\n🩸 BLOOD EMERGENCY DETECTED!")
        print(f"Building: {emergency['building']}")
        print(f"Floor Affected: {emergency.get('floor_affected', 'Unknown')}")
        print("🚑 BLOOD SPECIALIST ACTIVATED")
        print("=" * 60)
        
        # Get initial step-by-step blood specialist response
        initial_message = f"BLOOD EMERGENCY: Someone is bleeding at {emergency['building']} on {emergency.get('floor_affected', 'unknown floor')} in the {emergency.get('room_location', 'unknown room')}. I need to direct someone to help control the bleeding immediately."
        
        print(f"👤 You: {initial_message}")
        response = self.call_gemini(initial_message)
        self.speak(response)
        
        # Start specialized blood emergency conversation
        self.blood_conversation_loop()
    
    def blood_conversation_loop(self):
        """Specialized blood emergency conversation loop"""
        print("\n🩸 STEP-BY-STEP Blood Emergency Guidance Active")
        print("🚑 Follow each bleeding control step carefully - time is critical")
        print("💬 Type your response to each step. Type 'quit' to exit, 'restart' for new scenario.")
        print("=" * 80)
        
        while True:
            try:
                # Get user input
                user_input = self.get_user_input()
                
                if user_input.lower() in ["quit", "exit", "stop"]:
                    final_message = "Ending blood emergency session. REMEMBER: Keep pressure on bleeding, monitor for shock, ensure 911 is called for severe bleeding."
                    response = self.call_gemini(final_message)
                    self.speak(response)
                    break
                
                if user_input.lower() in ["restart", "again", "new"]:
                    self.restart_blood_scenario()
                    break
                
                if not user_input.strip():
                    continue
                
                # Update location if mentioned
                if not self.user_location and any(word in user_input.lower() for word in ["floor", "building", "room", "area", "ground", "first", "second"]):
                    self.parse_user_location(user_input)
                
                # Get specialized blood emergency response from Gemini
                response = self.call_gemini(user_input)
                self.speak(response)
                
            except KeyboardInterrupt:
                print("\n🛑 Blood emergency session interrupted")
                print("🚨 SAFETY REMINDER: If severe bleeding, apply direct pressure and call 911 immediately")
                break
            except Exception as e:
                print(f"❌ Error in blood emergency session: {e}")
                self.speak("🚨 GEMINI ERROR: Blood Emergency Agent requires Gemini 3 to function. Cannot provide medical guidance without AI.")
                break
    
    def restart_blood_scenario(self):
        """Restart the blood emergency scenario"""
        print("\n🔄 RESTARTING BLOOD EMERGENCY SCENARIO...")
        
        # Reset medical assessment
        self.conversation_history = []
        self.user_location = None
        self.current_step = 1
        self.emergency_phase = "dispatch"
        self.user_at_scene = False
        self.medical_assessment = {
            "bleeding_severity": "unknown",
            "bleeding_location": "unknown", 
            "bleeding_type": "unknown",
            "consciousness": "unknown",
            "shock_signs": "unknown",
            "pressure_applied": "unknown",
            "medical_help_called": "unknown"
        }
        
        # Wait a moment
        time.sleep(2)
        
        # Start new blood emergency scenario
        self.start_blood_emergency_scenario()

def main():
    """Main function to start Blood Emergency Agent"""
    print("🩸 ALERTAI BLOOD EMERGENCY SPECIALIST - GEMINI 3")
    print("=" * 70)
    print("🚑 Expert bleeding control and trauma response protocols")
    print("🩹 Specialized hemorrhage control and shock prevention")
    print("🏢 Building-specific medical supplies and personnel integration")
    print("🚨 Direct pressure, elevation, tourniquets, and emergency care")
    print("=" * 70)
    
    try:
        print("🔄 Initializing Blood Emergency Agent...")
        agent = BloodEmergencyAgent()
        print("✅ Agent initialized successfully!")
        
        # Choose mode
        print("\n🩸 BLOOD EMERGENCY AGENT MODES:")
        print("1. 🧪 Test Mode - Use hardcoded blood emergency scenario")
        print("2. 📡 Monitor Mode - Monitor AlertAI server for real blood emergencies")
        
        while True:
            try:
                choice = input("\nSelect mode (1 or 2): ").strip()
                if choice == "1":
                    print("🧪 Starting test blood emergency scenario...")
                    agent.start_blood_emergency_scenario()
                    break
                elif choice == "2":
                    print("📡 Starting blood emergency monitoring...")
                    agent.start_monitoring_mode()
                    break
                else:
                    print("❌ Invalid choice. Please enter 1 or 2.")
            except KeyboardInterrupt:
                print("\n👋 Blood Emergency Agent stopped by user")
                break
                
    except KeyboardInterrupt:
        print("\n👋 Blood emergency session ended by user")
        print("🚨 SAFETY REMINDER: Always call 911 for severe bleeding and apply direct pressure")
    except Exception as e:
        print(f"❌ Failed to start blood emergency agent: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()