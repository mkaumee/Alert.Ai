#!/usr/bin/env python3
"""
AlertAI Smoke Emergency Agent - Specialized Gemini 3
Expert smoke safety and evacuation guidance using Gemini 3 with specialized smoke protocols
"""
print("💨 Starting Smoke Emergency Agent...")
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

class SmokeEmergencyAgent:
    def __init__(self):
        self.name = "AlertAI Smoke Emergency Specialist"
        self.user_location = None
        self.building_layout = {}
        self.conversation_history = []
        self.emergency_context = {}
        self.smoke_assessment = {
            "smoke_density": "unknown",
            "smoke_source": "unknown", 
            "visibility": "unknown",
            "breathing_difficulty": "unknown",
            "escape_route_clear": "unknown",
            "user_safety": "unknown",
            "evacuation_status": "unknown"
        }
        self.current_step = 1
        self.emergency_phase = "detection"  # detection, assessment, evacuation, safety
        
        # Server monitoring for smoke emergencies
        self.server_url = getattr(config, 'ALERTAI_SERVER_URL', 'http://localhost:8000')
        self.is_monitoring = False
        self.current_smoke_emergency = None
        
        # Check for Gemini API key
        self.api_key = getattr(config, 'AI_API_KEY', '') or getattr(config, 'GEMINI_API_KEY', '')
        print(f"🔑 API Key loaded: {self.api_key[:20]}..." if self.api_key else "❌ No API key")
        if not self.api_key:
            print("❌ GEMINI_API_KEY not found in environment variables")
            sys.exit(1)
        
        # Smoke emergency scenario for testing
        self.test_emergency = {
            "id": 4001,
            "emergency_type": "Smoke",
            "building": "Medical Center Building A",
            "location": {"lat": 11.849010, "lon": 13.056751},
            "timestamp": datetime.now().isoformat(),
            "image_url": "test_images/smoke_emergency.jpg",
            "floor_affected": "Ground Floor"
        }
        
        # Load specialized smoke safety and building data
        self.load_smoke_safety_data()
        
        print(f"💨 {self.name} initialized and ready!")
        print(f"🧠 Using Gemini 3 with specialized smoke safety protocols")
        print(f"🚨 Expert knowledge: Smoke evacuation, breathing safety, visibility procedures")
    
    def load_smoke_safety_data(self):
        """Load specialized smoke safety data and building information"""
        self.building_layout = {
            "Medical Center Building A": {
                "floors": ["Ground Floor", "1st Floor", "2nd Floor"],
                "smoke_detection_systems": {
                    "Ground Floor": [
                        {
                            "system": "Smoke Detectors", 
                            "locations": ["Main lobby", "Corridors", "Electrical room", "Kitchen"],
                            "type": "Photoelectric and ionization",
                            "coverage": "Complete floor coverage",
                            "alert_system": "Building-wide alarm and PA"
                        },
                        {
                            "system": "Smoke Extraction", 
                            "location": "Main lobby and corridors", 
                            "capacity": "High-volume extraction fans",
                            "activation": "Automatic or manual override"
                        },
                        {
                            "system": "Emergency Lighting", 
                            "coverage": "All exit routes", 
                            "duration": "90 minutes battery backup",
                            "visibility": "Low-level pathway lighting"
                        }
                    ],
                    "1st Floor": [
                        {
                            "system": "Medical Grade Smoke Detection", 
                            "locations": ["Patient rooms", "Nursing stations", "Medical equipment rooms"],
                            "sensitivity": "High sensitivity for patient safety",
                            "integration": "Connected to medical monitoring systems"
                        },
                        {
                            "system": "Smoke Compartmentalization", 
                            "features": ["Fire doors", "Smoke barriers", "Pressurization systems"], 
                            "function": "Contain smoke to source area",
                            "activation": "Automatic on smoke detection"
                        },
                        {
                            "system": "Clean Air Zones", 
                            "locations": ["Stairwells", "Safe areas"], 
                            "function": "Positive pressure to keep smoke out",
                            "capacity": "Supports evacuation breathing"
                        }
                    ],
                    "2nd Floor": [
                        {
                            "system": "Office Smoke Detection", 
                            "locations": ["All offices", "Conference rooms", "Break areas"],
                            "type": "Standard photoelectric detectors",
                            "response": "Local and building-wide alerts"
                        },
                        {
                            "system": "Roof Smoke Venting", 
                            "location": "Central roof area", 
                            "function": "Natural smoke extraction",
                            "activation": "Automatic heat/smoke activation"
                        }
                    ]
                },
                "evacuation_routes": {
                    "Ground Floor": {
                        "primary": "Main entrance (if smoke-free)",
                        "secondary": "Back service exit",
                        "smoke_considerations": "Check visibility before using",
                        "assembly_point": "Upwind parking area (100m from building)"
                    },
                    "1st Floor": {
                        "primary": "Emergency stairwell A (pressurized)",
                        "secondary": "Emergency stairwell B (pressurized)",
                        "smoke_refuge": "Stairwell landings (clean air zones)",
                        "patient_evacuation": "Medical elevator if smoke-free"
                    },
                    "2nd Floor": {
                        "primary": "Emergency stairwell A (pressurized)",
                        "secondary": "Emergency stairwell B (pressurized)",
                        "smoke_refuge": "Stairwell landings",
                        "last_resort": "Roof access for helicopter evacuation"
                    }
                },
                "smoke_safety_equipment": {
                    "Ground Floor": [
                        {"equipment": "Emergency Escape Masks", "location": "Security desk", "quantity": "20 masks", "use": "Smoke-filled evacuation"},
                        {"equipment": "Flashlights", "location": "Emergency stations", "quantity": "Multiple", "use": "Low visibility navigation"},
                        {"equipment": "Wet Towels Station", "location": "Near exits", "use": "Breathing protection"}
                    ],
                    "1st Floor": [
                        {"equipment": "Medical Oxygen", "location": "Nursing station", "use": "Smoke inhalation treatment"},
                        {"equipment": "Evacuation Chairs", "location": "Stairwell entrances", "quantity": "4 chairs", "use": "Patient evacuation"},
                        {"equipment": "Emergency Communication", "location": "Nursing stations", "use": "Coordinate evacuation"}
                    ],
                    "2nd Floor": [
                        {"equipment": "Escape Hoods", "location": "Administrative office", "quantity": "15 hoods", "use": "Smoke protection"},
                        {"equipment": "Emergency Rope", "location": "Conference room", "use": "Last resort window evacuation"},
                        {"equipment": "Air Purification Unit", "location": "Safe room", "use": "Clean air while waiting rescue"}
                    ]
                },
                "smoke_hazards": {
                    "toxic_smoke_sources": [
                        {"source": "Electrical equipment", "toxins": ["Carbon monoxide", "Hydrogen cyanide"], "danger": "Extremely toxic"},
                        {"source": "Plastic materials", "toxins": ["Toxic gases", "Dense black smoke"], "danger": "Visibility and breathing hazard"},
                        {"source": "Medical supplies", "toxins": ["Chemical fumes"], "danger": "Respiratory irritation"}
                    ],
                    "smoke_behavior": {
                        "heat_rises": "Smoke and heat rise - stay low",
                        "stack_effect": "Smoke travels up stairwells and elevator shafts",
                        "wind_effect": "External wind can push smoke through building",
                        "door_gaps": "Smoke travels under doors and through gaps"
                    },
                    "breathing_dangers": {
                        "carbon_monoxide": "Colorless, odorless, deadly - causes unconsciousness",
                        "oxygen_depletion": "Smoke consumes oxygen - causes suffocation",
                        "toxic_gases": "Chemical burns to lungs and airways",
                        "particulates": "Lung damage from smoke particles"
                    }
                },
                "emergency_contacts": {
                    "fire_department": "911",
                    "building_maintenance": "+234-800-MAINTENANCE",
                    "hvac_emergency": "+234-800-HVAC",
                    "medical_emergency": "+234-800-MEDICAL"
                }
            }
        }
        
        # Smoke safety protocols
        self.smoke_protocols = {
            "smoke_evacuation_rules": {
                "stay_low": "Crawl below smoke level - clean air is near floor",
                "test_doors": "Feel door handles - hot means fire/smoke behind",
                "close_doors": "Close doors behind you to slow smoke spread",
                "use_stairs": "NEVER use elevators during smoke emergency",
                "follow_exit_signs": "Emergency lighting shows safe exit routes"
            },
            "breathing_protection": {
                "wet_cloth": "Cover nose/mouth with wet cloth if available",
                "shallow_breaths": "Take short, shallow breaths to minimize smoke intake",
                "hold_breath": "Hold breath when passing through heavy smoke",
                "escape_mask": "Use emergency escape mask if available",
                "avoid_smoke": "Do not enter smoke-filled areas if avoidable"
            },
            "visibility_guidelines": {
                "good": "Can see more than 10 feet - evacuation possible",
                "limited": "Can see 3-10 feet - proceed with extreme caution",
                "poor": "Less than 3 feet visibility - find refuge, wait for help",
                "zero": "Cannot see - do not move, call for help, wait for rescue"
            },
            "smoke_assessment": {
                "light": "Thin smoke, good visibility - evacuate quickly",
                "moderate": "Thicker smoke, reduced visibility - stay low, evacuate carefully",
                "heavy": "Dense smoke, poor visibility - find safe room, wait for help",
                "toxic": "Chemical smell, burning eyes/throat - immediate evacuation or refuge"
            }
        }
    
    def call_gemini(self, user_message):
        """Call Gemini 3 API with specialized smoke safety context - GEMINI ONLY"""
        try:
            # Build smoke-specific context
            context_prompt = self.build_smoke_context_prompt(user_message)
            
            # Create Python script for Gemini API call
            script_content = '''
import google.generativeai as genai

api_key = "{api_key}"
genai.configure(api_key=api_key)

model = genai.GenerativeModel('gemini-3-flash')

prompt = """{context_prompt}"""

try:
    result = model.generate_content(prompt)
    print(result.text.strip())
except Exception as e:
    print(f"GEMINI_ERROR: {{str(e)}}")
'''.format(api_key=self.api_key, context_prompt=context_prompt)
            
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
                    return f"🚨 GEMINI API ERROR: {error_msg}\n\n❌ Smoke Emergency Agent requires Gemini 3 to function. Please resolve API issues."
            else:
                return f"🚨 GEMINI CONNECTION FAILED: {result.stderr}\n\n❌ Smoke Emergency Agent is Gemini-powered only. Cannot provide guidance without Gemini."
                
        except Exception as e:
            return f"🚨 GEMINI SYSTEM ERROR: {str(e)}\n\n❌ Smoke Emergency Agent requires Gemini 3. Please check API configuration and quota."
    
    def build_smoke_context_prompt(self, user_message):
        """Build specialized smoke safety context prompt for Gemini"""
        
        # Smoke emergency context
        emergency_info = f"""
SMOKE EMERGENCY SITUATION:
- Type: {self.test_emergency['emergency_type']}
- Location: {self.test_emergency['building']}
- Floor Affected: {self.test_emergency.get('floor_affected', 'Unknown')}
- Time: {self.test_emergency['timestamp']}
- Status: ACTIVE SMOKE EMERGENCY - Immediate evacuation assessment required
"""
        
        # User location and smoke assessment
        location_info = ""
        if self.user_location:
            location_info = f"""
USER LOCATION:
- Building: {self.user_location['building']}
- Floor: {self.user_location['floor']}
"""
        else:
            location_info = "USER LOCATION: Unknown - CRITICAL to determine for smoke safety guidance"
        
        # Smoke assessment
        smoke_assessment_info = f"""
SMOKE ASSESSMENT STATUS:
- Emergency Phase: {self.emergency_phase}
- Smoke Density: {self.smoke_assessment['smoke_density']}
- Smoke Source: {self.smoke_assessment['smoke_source']}
- Visibility: {self.smoke_assessment['visibility']}
- Breathing Difficulty: {self.smoke_assessment['breathing_difficulty']}
- Escape Route Clear: {self.smoke_assessment['escape_route_clear']}
- User Safety: {self.smoke_assessment['user_safety']}
- Evacuation Status: {self.smoke_assessment['evacuation_status']}
"""
        
        # Building smoke safety data
        building_data = f"""
SMOKE SAFETY BUILDING DATA:
{json.dumps(self.building_layout, indent=2)}
"""
        
        # Smoke safety protocols
        protocols_data = f"""
SMOKE SAFETY PROTOCOLS:
{json.dumps(self.smoke_protocols, indent=2)}
"""
        
        # Conversation history
        history_context = ""
        if self.conversation_history:
            recent_history = self.conversation_history[-8:]  # Last 8 exchanges for smoke context
            history_context = f"""
CONVERSATION HISTORY:
{chr(10).join(recent_history)}
"""
        
        # Message analysis
        message_analysis = self.analyze_smoke_message(user_message)
        
        # Full specialized smoke prompt
        full_prompt = f"""You are AlertAI Smoke Emergency Specialist, an expert smoke safety professional providing real-time guidance during smoke emergencies. You have specialized knowledge of smoke behavior, breathing safety, evacuation procedures, and visibility management.

{emergency_info}
{location_info}
{smoke_assessment_info}
{building_data}
{protocols_data}
{history_context}

MESSAGE ANALYSIS:
{message_analysis}

CURRENT USER MESSAGE: "{user_message}"

STEP-BY-STEP GUIDANCE RULES:
1. **ONE STEP ONLY**: Give only ONE clear, specific action per response
2. **SHORT & FOCUSED**: Maximum 2-3 sentences with essential smoke safety information only
3. **WAIT FOR CONFIRMATION**: Always end with "Confirm when done" or ask for status
4. **SMOKE SAFETY PRIORITY LOGIC**: 
   - Step 1: Assess user's current smoke exposure and breathing safety
   - Step 2: Determine visibility and escape route viability
   - Step 3: Guide immediate protective actions (stay low, wet cloth, etc.)
   - Step 4: Direct evacuation using safest smoke-free routes
   - Step 5: Ongoing safety monitoring and emergency coordination
5. **USE BUILDING DATA**: Reference specific smoke detection systems, clean air zones, evacuation routes
6. **BREATHING SAFETY FIRST**: Prioritize respiratory protection and oxygen access

SMOKE EMERGENCY SEQUENCE:
Step 1: Immediate smoke exposure assessment (can you breathe? visibility?)
Step 2: Protective breathing measures (stay low, cover nose/mouth)
Step 3: Visibility and escape route assessment
Step 4: Evacuation guidance using smoke-free routes and clean air zones
Step 5: Emergency services coordination and ongoing safety monitoring

CRITICAL SMOKE SAFETY RULES:
- Stay LOW - smoke and toxic gases rise, clean air is near floor
- Test doors before opening - hot door means fire/smoke behind
- Close doors behind you to slow smoke spread
- NEVER use elevators during smoke emergency
- Use wet cloth over nose/mouth for breathing protection
- If trapped by smoke, go to room with window, signal for help
- Follow emergency lighting to exits
- Get to clean air zones (pressurized stairwells)

RESPONSE STYLE:
- Be calm but urgent about breathing safety
- Use specific building smoke data (detection systems, clean air zones, evacuation routes)
- Provide clear step-by-step smoke safety instructions
- Ask critical assessment questions (visibility, breathing, smoke density)
- Include specific breathing protection and evacuation guidance
- Reference available smoke safety equipment and clean air areas

EXAMPLE RESPONSES FOR SMOKE EMERGENCY:
Initial assessment: "STEP 1: Smoke detected on {{emergency floor}}. Are you experiencing any smoke where you are? Can you see clearly and breathe normally? Stay low and tell me your visibility level."

Breathing protection: "STEP 2: Get low to the floor immediately - clean air is near ground level. Cover your nose and mouth with wet cloth if available. Can you breathe without difficulty now?"

Evacuation guidance: "STEP 3: Visibility is good enough to evacuate. Stay low and head to Emergency Stairwell A - it has clean air pressurization. Test doors before opening. Confirm when moving."

Safety monitoring: "STEP 4: You're in the clean air zone. Continue down stairwell staying low. Do NOT use elevator. Exit to upwind parking area. Confirm when you reach outside."

RESPOND WITH NEXT SMOKE SAFETY STEP ONLY:"""

        return full_prompt
    
    def analyze_smoke_message(self, message):
        """Analyze user message for smoke-specific context and urgency"""
        message_lower = message.lower()
        analysis = []
        
        # Smoke density assessment
        if any(word in message_lower for word in ["thick smoke", "heavy smoke", "dense", "can't see"]):
            analysis.append("SMOKE: Heavy/dense smoke - visibility severely compromised")
            self.smoke_assessment['smoke_density'] = "heavy"
            self.smoke_assessment['visibility'] = "poor"
        elif any(word in message_lower for word in ["light smoke", "thin smoke", "little smoke"]):
            analysis.append("SMOKE: Light smoke - evacuation possible with caution")
            self.smoke_assessment['smoke_density'] = "light"
            self.smoke_assessment['visibility'] = "good"
        elif any(word in message_lower for word in ["smoke", "smoky", "hazy"]):
            analysis.append("SMOKE: Moderate smoke detected - assess evacuation options")
            self.smoke_assessment['smoke_density'] = "moderate"
        
        # Breathing assessment
        if any(word in message_lower for word in ["can't breathe", "hard to breathe", "coughing", "choking"]):
            analysis.append("BREATHING: Difficulty breathing - immediate protective action needed")
            self.smoke_assessment['breathing_difficulty'] = "severe"
        elif any(word in message_lower for word in ["breathing ok", "can breathe", "air is clear"]):
            analysis.append("BREATHING: Breathing normal - good for evacuation")
            self.smoke_assessment['breathing_difficulty'] = "none"
        elif any(word in message_lower for word in ["slight cough", "irritated", "burning eyes"]):
            analysis.append("BREATHING: Mild irritation - use protection and evacuate")
            self.smoke_assessment['breathing_difficulty'] = "mild"
        
        # Visibility assessment
        if any(word in message_lower for word in ["can't see", "no visibility", "blind", "dark"]):
            analysis.append("VISIBILITY: Zero visibility - do not move, wait for help")
            self.smoke_assessment['visibility'] = "zero"
        elif any(word in message_lower for word in ["can see", "clear", "good visibility"]):
            analysis.append("VISIBILITY: Good visibility - evacuation possible")
            self.smoke_assessment['visibility'] = "good"
        elif any(word in message_lower for word in ["limited", "reduced", "hazy"]):
            analysis.append("VISIBILITY: Limited visibility - proceed with extreme caution")
            self.smoke_assessment['visibility'] = "limited"
        
        # Escape route assessment
        if any(word in message_lower for word in ["exit blocked", "can't get out", "trapped", "smoke in hallway"]):
            analysis.append("ESCAPE: Route blocked by smoke - find refuge area")
            self.smoke_assessment['escape_route_clear'] = "blocked"
        elif any(word in message_lower for word in ["exit clear", "hallway clear", "can get out"]):
            analysis.append("ESCAPE: Route appears clear - proceed with evacuation")
            self.smoke_assessment['escape_route_clear'] = "clear"
        
        # User safety status
        if any(word in message_lower for word in ["safe", "clean air", "no smoke here"]):
            analysis.append("SAFETY: User in clean air area - good for staging evacuation")
            self.smoke_assessment['user_safety'] = "safe"
        elif any(word in message_lower for word in ["in smoke", "surrounded", "getting worse"]):
            analysis.append("SAFETY: User in smoke - immediate protective action needed")
            self.smoke_assessment['user_safety'] = "danger"
        
        # Location detection
        if any(word in message_lower for word in ["ground floor", "ground", "lobby", "entrance"]):
            analysis.append("LOCATION: Ground Floor - smoke extraction and emergency lighting available")
        elif any(word in message_lower for word in ["first floor", "1st floor", "floor 1", "medical"]):
            analysis.append("LOCATION: 1st Floor - clean air zones and smoke compartmentalization available")
        elif any(word in message_lower for word in ["second floor", "2nd floor", "floor 2", "office"]):
            analysis.append("LOCATION: 2nd Floor - roof venting and escape equipment available")
        
        # Urgency assessment
        if any(word in message_lower for word in ["emergency", "urgent", "help", "can't breathe", "trapped"]):
            analysis.append("URGENCY: CRITICAL - Immediate smoke safety response needed")
        
        return "; ".join(analysis) if analysis else "General smoke emergency inquiry"
    
    def speak(self, text):
        """Display smoke specialist response and add to conversation history"""
        print(f"💨 Smoke Specialist: {text}")
        self.conversation_history.append(f"Smoke Specialist: {text}")
    
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
        """Parse and store user location for smoke safety context"""
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
        
        # Provide immediate smoke safety info for their floor
        self.provide_floor_smoke_info(floor)
    
    def provide_floor_smoke_info(self, floor):
        """Provide immediate smoke safety information for user's floor"""
        if floor in self.building_layout["Medical Center Building A"]["smoke_detection_systems"]:
            systems = self.building_layout["Medical Center Building A"]["smoke_detection_systems"][floor]
            print(f"💨 Smoke safety systems on {floor}:")
            for system in systems:
                if 'system' in system:
                    print(f"   • {system['system']}: {system.get('location', system.get('locations', 'Multiple locations'))}")
        
        # Show evacuation routes
        if floor in self.building_layout["Medical Center Building A"]["evacuation_routes"]:
            routes = self.building_layout["Medical Center Building A"]["evacuation_routes"][floor]
            print(f"🚪 Smoke evacuation routes from {floor}:")
            print(f"   • Primary: {routes['primary']}")
            if 'secondary' in routes:
                print(f"   • Secondary: {routes['secondary']}")
    
    def check_for_smoke_emergencies(self):
        """Monitor AlertAI server for smoke emergencies only"""
        try:
            response = requests.get(f"{self.server_url}/api/alerts/active", timeout=5)
            if response.status_code == 200:
                data = response.json()
                alerts = data.get('alerts', [])
                
                # Filter for smoke emergencies only
                smoke_alerts = [alert for alert in alerts if alert.get('emergency_type', '').lower() == 'smoke']
                
                if smoke_alerts:
                    # Check for new smoke emergencies
                    for smoke_alert in smoke_alerts:
                        if not self.current_smoke_emergency or smoke_alert['id'] != self.current_smoke_emergency.get('id'):
                            print(f"\n💨 NEW SMOKE EMERGENCY DETECTED FROM SERVER!")
                            print(f"ID: {smoke_alert['id']}")
                            print(f"Type: {smoke_alert['emergency_type']}")
                            print(f"Location: {smoke_alert['building']}")
                            print(f"Floor: {smoke_alert.get('floor_affected', 'Unknown')}")
                            print(f"Time: {smoke_alert['timestamp']}")
                            print("=" * 60)
                            
                            # Replace test emergency with real smoke emergency
                            self.current_smoke_emergency = smoke_alert
                            self.test_emergency = smoke_alert  # Use real data instead of test
                            return True
                else:
                    # No smoke emergencies active
                    if self.current_smoke_emergency:
                        print("💨 Smoke emergency resolved. Monitoring for new smoke emergencies...")
                        self.current_smoke_emergency = None
                        
        except Exception as e:
            print(f"❌ Error checking for smoke emergencies: {e}")
        
        return False
    
    def start_monitoring_mode(self):
        """Start monitoring AlertAI server for smoke emergencies"""
        print("💨 SMOKE EMERGENCY MONITORING MODE")
        print("=" * 60)
        print("🚨 Monitoring AlertAI server for SMOKE emergencies only")
        print("🔄 Checking server every 10 seconds")
        print("🚨 Will activate smoke specialist when smoke is detected")
        print("💬 Press Ctrl+C to stop monitoring")
        print("=" * 60)
        
        self.is_monitoring = True
        
        while self.is_monitoring:
            try:
                # Check for smoke emergencies
                if self.check_for_smoke_emergencies():
                    # Smoke emergency detected - start safety guidance
                    self.start_smoke_emergency_scenario()
                    # After guidance session, continue monitoring
                    continue
                
                # Show monitoring status
                if not self.current_smoke_emergency:
                    print("💨 Monitoring for smoke emergencies... (Ctrl+C to stop)")
                    time.sleep(10)
                    
            except KeyboardInterrupt:
                print("\n🛑 Smoke emergency monitoring stopped by user")
                self.is_monitoring = False
                break
            except Exception as e:
                print(f"❌ Monitoring error: {e}")
                time.sleep(5)
    
    def start_smoke_emergency_scenario(self):
        """Start the smoke emergency scenario with specialized safety guidance"""
        emergency = self.test_emergency
        
        print(f"\n💨 SMOKE EMERGENCY DETECTED!")
        print(f"Building: {emergency['building']}")
        print(f"Floor Affected: {emergency.get('floor_affected', 'Unknown')}")
        print("🚨 SMOKE SPECIALIST ACTIVATED")
        print("=" * 60)
        
        # Get initial step-by-step smoke specialist response
        initial_message = f"SMOKE EMERGENCY: Smoke detected at {emergency['building']} on {emergency.get('floor_affected', 'unknown floor')}. I need immediate smoke safety guidance to help people evacuate safely."
        
        print(f"👤 You: {initial_message}")
        response = self.call_gemini(initial_message)
        self.speak(response)
        
        # Start specialized smoke conversation
        self.smoke_conversation_loop()
    
    def smoke_conversation_loop(self):
        """Specialized smoke emergency conversation loop"""
        print("\n💨 STEP-BY-STEP Smoke Emergency Guidance Active")
        print("🚨 Follow each smoke safety step carefully - breathing safety is critical")
        print("💬 Type your response to each step. Type 'quit' to exit, 'restart' for new scenario.")
        print("=" * 80)
        
        while True:
            try:
                # Get user input
                user_input = self.get_user_input()
                
                if user_input.lower() in ["quit", "exit", "stop"]:
                    final_message = "Ending smoke emergency session. REMEMBER: Stay low in smoke, get to fresh air, call 911 if smoke persists."
                    response = self.call_gemini(final_message)
                    self.speak(response)
                    break
                
                if user_input.lower() in ["restart", "again", "new"]:
                    self.restart_smoke_scenario()
                    break
                
                if not user_input.strip():
                    continue
                
                # Update location if mentioned
                if not self.user_location and any(word in user_input.lower() for word in ["floor", "building", "room", "area", "ground", "first", "second"]):
                    self.parse_user_location(user_input)
                
                # Get specialized smoke response from Gemini
                response = self.call_gemini(user_input)
                self.speak(response)
                
            except KeyboardInterrupt:
                print("\n🛑 Smoke emergency session interrupted")
                print("🚨 SAFETY REMINDER: If in smoke, stay low and get to fresh air immediately")
                break
            except Exception as e:
                print(f"❌ Error in smoke emergency session: {e}")
                self.speak("🚨 GEMINI ERROR: Smoke Emergency Agent requires Gemini 3 to function. Cannot provide smoke safety guidance without AI.")
                break
    
    def restart_smoke_scenario(self):
        """Restart the smoke emergency scenario"""
        print("\n🔄 RESTARTING SMOKE EMERGENCY SCENARIO...")
        
        # Reset smoke assessment
        self.conversation_history = []
        self.user_location = None
        self.current_step = 1
        self.emergency_phase = "detection"
        self.smoke_assessment = {
            "smoke_density": "unknown",
            "smoke_source": "unknown", 
            "visibility": "unknown",
            "breathing_difficulty": "unknown",
            "escape_route_clear": "unknown",
            "user_safety": "unknown",
            "evacuation_status": "unknown"
        }
        
        # Wait a moment
        time.sleep(2)
        
        # Start new smoke scenario
        self.start_smoke_emergency_scenario()

def main():
    """Main function to start Smoke Emergency Agent"""
    print("💨 ALERTAI SMOKE EMERGENCY SPECIALIST - GEMINI 3")
    print("=" * 70)
    print("🚨 Expert smoke safety and evacuation protocols")
    print("🫁 Specialized breathing safety and visibility guidance")
    print("🏢 Building-specific smoke detection and clean air systems")
    print("🚨 Stay low, test doors, and evacuation procedures")
    print("=" * 70)
    
    try:
        print("🔄 Initializing Smoke Emergency Agent...")
        agent = SmokeEmergencyAgent()
        print("✅ Agent initialized successfully!")
        
        # Choose mode
        print("\n💨 SMOKE EMERGENCY AGENT MODES:")
        print("1. 🧪 Test Mode - Use hardcoded smoke emergency scenario")
        print("2. 📡 Monitor Mode - Monitor AlertAI server for real smoke emergencies")
        
        while True:
            try:
                choice = input("\nSelect mode (1 or 2): ").strip()
                if choice == "1":
                    print("🧪 Starting test smoke emergency scenario...")
                    agent.start_smoke_emergency_scenario()
                    break
                elif choice == "2":
                    print("📡 Starting smoke emergency monitoring...")
                    agent.start_monitoring_mode()
                    break
                else:
                    print("❌ Invalid choice. Please enter 1 or 2.")
            except KeyboardInterrupt:
                print("\n👋 Smoke Emergency Agent stopped by user")
                break
                
    except KeyboardInterrupt:
        print("\n👋 Smoke emergency session ended by user")
        print("🚨 SAFETY REMINDER: Always prioritize breathing safety and get to fresh air")
    except Exception as e:
        print(f"❌ Failed to start smoke emergency agent: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()