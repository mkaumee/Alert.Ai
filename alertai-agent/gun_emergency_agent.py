#!/usr/bin/env python3
"""
AlertAI Gun/Weapon Emergency Agent - Specialized Gemini 3
Expert security protocols and lockdown procedures using Gemini 3 with specialized safety protocols
"""
print("🔫 Starting Gun/Weapon Emergency Agent...")
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

class GunEmergencyAgent:
    def __init__(self):
        self.name = "AlertAI Gun/Weapon Emergency Specialist"
        self.user_location = None
        self.building_layout = {}
        self.conversation_history = []
        self.emergency_context = {}
        self.security_assessment = {
            "threat_location": "unknown",
            "threat_type": "unknown", 
            "user_safety": "unknown",
            "lockdown_status": "unknown",
            "escape_route": "unknown",
            "authorities_called": "unknown"
        }
        self.current_step = 1
        self.emergency_phase = "alert"  # alert, assessment, lockdown, evacuation, safe
        
        # Server monitoring for gun/weapon emergencies
        self.server_url = getattr(config, 'ALERTAI_SERVER_URL', 'http://localhost:8000')
        self.is_monitoring = False
        self.current_gun_emergency = None
        
        # Check for Gemini API key
        self.api_key = getattr(config, 'AI_API_KEY', '') or getattr(config, 'GEMINI_API_KEY', '')
        print(f"🔑 API Key loaded: {self.api_key[:20]}..." if self.api_key else "❌ No API key")
        if not self.api_key:
            print("❌ GEMINI_API_KEY not found in environment variables")
            sys.exit(1)
        
        # Gun/weapon emergency scenario for testing
        self.test_emergency = {
            "id": 3001,
            "emergency_type": "Gun",
            "building": "Medical Center Building A",
            "location": {"lat": 11.849010, "lon": 13.056751},
            "timestamp": datetime.now().isoformat(),
            "image_url": "test_images/gun_emergency.jpg",
            "floor_affected": "1st Floor"
        }
        
        # Load specialized security and building data
        self.load_security_data()
        
        print(f"🔫 {self.name} initialized and ready!")
        print(f"🧠 Using Gemini 3 with specialized security protocols")
        print(f"🚨 Expert knowledge: Lockdown procedures, evacuation routes, threat assessment")
    
    def load_security_data(self):
        """Load specialized security data and building information"""
        self.building_layout = {
            "Medical Center Building A": {
                "floors": ["Ground Floor", "1st Floor", "2nd Floor"],
                "security_features": {
                    "Ground Floor": [
                        {
                            "feature": "Security Control Room", 
                            "location": "Main entrance area", 
                            "capabilities": ["CCTV monitoring", "PA system", "Emergency lockdown", "Police direct line"],
                            "staffed": "24/7",
                            "contact": "+234-800-SECURITY"
                        },
                        {
                            "feature": "Metal Detectors", 
                            "location": "Main entrance", 
                            "status": "Active during business hours",
                            "bypass": "Emergency personnel only"
                        },
                        {
                            "feature": "Panic Buttons", 
                            "locations": ["Reception desk", "Security office", "Elevator lobby"],
                            "response": "Immediate police alert and lockdown activation"
                        }
                    ],
                    "1st Floor": [
                        {
                            "feature": "Lockdown Doors", 
                            "locations": ["Main corridor", "Nursing stations", "Patient rooms"], 
                            "type": "Magnetic locks with manual override",
                            "activation": "Security control or panic button"
                        },
                        {
                            "feature": "Safe Rooms", 
                            "locations": ["Medical supply room", "Staff break room"], 
                            "capacity": "15-20 people each",
                            "features": ["Reinforced doors", "Internal communication", "Emergency supplies"]
                        },
                        {
                            "feature": "Emergency Communication", 
                            "type": "Intercom system", 
                            "coverage": "All rooms and corridors",
                            "direct_line": "Security control room"
                        }
                    ],
                    "2nd Floor": [
                        {
                            "feature": "Administrative Safe Room", 
                            "location": "Conference room B", 
                            "capacity": "25 people",
                            "features": ["Reinforced walls", "Independent phone line", "Emergency supplies"]
                        },
                        {
                            "feature": "Roof Access", 
                            "location": "Emergency stairwell", 
                            "use": "Last resort evacuation",
                            "helicopter_landing": "Possible with clearance"
                        },
                        {
                            "feature": "Lockdown Override", 
                            "location": "Administrative office", 
                            "access": "Senior staff only",
                            "function": "Manual building lockdown control"
                        }
                    ]
                },
                "evacuation_routes": {
                    "Ground Floor": {
                        "primary": "Main entrance (if safe)",
                        "secondary": "Back service entrance",
                        "emergency": "Loading dock (staff only)",
                        "assembly_point": "Parking lot (200m from building)"
                    },
                    "1st Floor": {
                        "primary": "Emergency stairwell A (east)",
                        "secondary": "Emergency stairwell B (west)",
                        "safe_rooms": ["Medical supply room", "Staff break room"],
                        "lockdown_zones": "Patient care areas"
                    },
                    "2nd Floor": {
                        "primary": "Emergency stairwell A (east)",
                        "secondary": "Emergency stairwell B (west)",
                        "safe_room": "Conference room B",
                        "roof_access": "Emergency stairwell (last resort)"
                    }
                },
                "lockdown_procedures": {
                    "immediate_actions": [
                        "Activate panic button or call security",
                        "Lock or barricade doors",
                        "Turn off lights",
                        "Move away from windows and doors",
                        "Silence phones and devices",
                        "Wait for all-clear from authorities"
                    ],
                    "communication_protocol": {
                        "code_silver": "Weapon/gun threat - lockdown initiated",
                        "all_clear": "Threat neutralized - normal operations resume",
                        "evacuation": "Immediate evacuation - use designated routes"
                    },
                    "authority_contacts": {
                        "police": "911",
                        "swat": "911 (specify weapon threat)",
                        "building_security": "+234-800-SECURITY",
                        "emergency_coordinator": "+234-800-EMERGENCY"
                    }
                },
                "threat_assessment": {
                    "high_risk_areas": [
                        {"area": "Main entrance", "risk": "Public access point"},
                        {"area": "Parking areas", "risk": "Limited visibility"},
                        {"area": "Loading dock", "risk": "Service access"}
                    ],
                    "safe_zones": [
                        {"zone": "Medical supply rooms", "security": "Reinforced, lockable"},
                        {"zone": "Administrative safe room", "security": "Reinforced walls, independent communication"},
                        {"zone": "Security control room", "security": "Bulletproof glass, direct police line"}
                    ],
                    "escape_routes": {
                        "primary": "Emergency stairwells (if clear)",
                        "secondary": "Service corridors (staff access)",
                        "last_resort": "Roof access (helicopter evacuation)"
                    }
                }
            }
        }
        
        # Security protocols
        self.security_protocols = {
            "run_hide_fight": {
                "RUN": "If safe path available - evacuate immediately",
                "HIDE": "If escape not possible - lockdown and barricade",
                "FIGHT": "Only as absolute last resort for survival"
            },
            "lockdown_steps": {
                "1": "Lock or barricade entry points",
                "2": "Turn off lights and close blinds",
                "3": "Move away from doors and windows",
                "4": "Silence all devices",
                "5": "Remain quiet and hidden",
                "6": "Wait for official all-clear"
            },
            "communication_rules": {
                "do": ["Call 911 if safe", "Use text messages if possible", "Follow official instructions"],
                "dont": ["Use social media", "Leave safe area without clearance", "Ignore lockdown alerts"]
            },
            "threat_indicators": {
                "immediate": ["Gunshots", "Screaming", "Panic", "Visible weapon"],
                "potential": ["Suspicious behavior", "Threats", "Unusual packages", "Unauthorized access"]
            }
        }
    
    def call_gemini(self, user_message):
        """Call Gemini 3 API with specialized security context - GEMINI ONLY"""
        try:
            # Build security-specific context
            context_prompt = self.build_security_context_prompt(user_message)
            
            # Create Python script for Gemini API call
            script_content = '''
import google.genai as genai

api_key = "{api_key}"
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
                    return f"🚨 GEMINI API ERROR: {error_msg}\n\n❌ Gun Emergency Agent requires Gemini 3 to function. Please resolve API issues."
            else:
                return f"🚨 GEMINI CONNECTION FAILED: {result.stderr}\n\n❌ Gun Emergency Agent is Gemini-powered only. Cannot provide guidance without Gemini."
                
        except Exception as e:
            return f"🚨 GEMINI SYSTEM ERROR: {str(e)}\n\n❌ Gun Emergency Agent requires Gemini 3. Please check API configuration and quota."
    
    def build_security_context_prompt(self, user_message):
        """Build specialized security context prompt for Gemini"""
        
        # Security emergency context
        emergency_info = f"""
GUN/WEAPON EMERGENCY SITUATION:
- Type: {self.test_emergency['emergency_type']}
- Location: {self.test_emergency['building']}
- Floor Affected: {self.test_emergency.get('floor_affected', 'Unknown')}
- Time: {self.test_emergency['timestamp']}
- Status: ACTIVE WEAPON THREAT - Immediate security response required
"""
        
        # User location and security assessment
        location_info = ""
        if self.user_location:
            location_info = f"""
USER LOCATION:
- Building: {self.user_location['building']}
- Floor: {self.user_location['floor']}
"""
        else:
            location_info = "USER LOCATION: Unknown - CRITICAL to determine for safety guidance"
        
        # Security assessment
        security_assessment_info = f"""
SECURITY ASSESSMENT STATUS:
- Emergency Phase: {self.emergency_phase}
- Threat Location: {self.security_assessment['threat_location']}
- Threat Type: {self.security_assessment['threat_type']}
- User Safety: {self.security_assessment['user_safety']}
- Lockdown Status: {self.security_assessment['lockdown_status']}
- Escape Route: {self.security_assessment['escape_route']}
- Authorities Called: {self.security_assessment['authorities_called']}
"""
        
        # Building security data
        building_data = f"""
SECURITY BUILDING DATA:
{json.dumps(self.building_layout, indent=2)}
"""
        
        # Security protocols
        protocols_data = f"""
SECURITY PROTOCOLS:
{json.dumps(self.security_protocols, indent=2)}
"""
        
        # Conversation history
        history_context = ""
        if self.conversation_history:
            recent_history = self.conversation_history[-8:]  # Last 8 exchanges for security context
            history_context = f"""
CONVERSATION HISTORY:
{chr(10).join(recent_history)}
"""
        
        # Message analysis
        message_analysis = self.analyze_security_message(user_message)
        
        # Full specialized security prompt
        full_prompt = f"""You are AlertAI Gun/Weapon Emergency Specialist, an expert security professional providing real-time guidance during weapon threats. You have specialized knowledge of lockdown procedures, threat assessment, and emergency security protocols.

{emergency_info}
{location_info}
{security_assessment_info}
{building_data}
{protocols_data}
{history_context}

MESSAGE ANALYSIS:
{message_analysis}

CURRENT USER MESSAGE: "{user_message}"

STEP-BY-STEP GUIDANCE RULES:
1. **ONE STEP ONLY**: Give only ONE clear, specific action per response
2. **SHORT & FOCUSED**: Maximum 2-3 sentences with essential security information only
3. **WAIT FOR CONFIRMATION**: Always end with "Confirm when done" or ask for status
4. **SECURITY PRIORITY LOGIC**: 
   - Step 1: Immediate safety assessment - get user to safe location
   - Step 2: Determine threat proximity and user's current safety
   - Step 3: Implement RUN, HIDE, or FIGHT protocol based on situation
   - Step 4: Lockdown procedures if hiding is necessary
   - Step 5: Communication with authorities and ongoing safety monitoring
5. **USE BUILDING DATA**: Reference specific safe rooms, lockdown features, escape routes
6. **LIFE SAFETY FIRST**: Prioritize immediate survival over all other concerns

SECURITY RESPONSE SEQUENCE:
Step 1: Get user to immediate safety (away from threat)
Step 2: Assess threat location and user's position relative to threat
Step 3: Determine best survival strategy (RUN if safe path, HIDE if trapped)
Step 4: Execute chosen strategy with specific building resources
Step 5: Maintain communication and monitor for changes
Step 6: Coordinate with authorities and await all-clear

CRITICAL SECURITY RULES:
- RUN if safe escape route available
- HIDE if escape not possible - use safe rooms and lockdown
- FIGHT only as absolute last resort for survival
- Call 911 immediately if safe to do so
- Follow RUN-HIDE-FIGHT protocol in that order
- Never investigate or confront threat
- Stay hidden until official all-clear from authorities
- Use building's security features (panic buttons, safe rooms, lockdown)

RESPONSE STYLE:
- Be calm but urgent
- Use specific building security data (safe rooms, lockdown features, escape routes)
- Provide clear step-by-step survival instructions
- Ask critical assessment questions (threat location, user safety, escape options)
- Include specific safety warnings and building security resources
- Reference available security personnel and emergency contacts

EXAMPLE RESPONSES FOR WEAPON THREAT:
Initial alert: "STEP 1: WEAPON THREAT DETECTED. Get to the nearest safe room immediately - {{specific location}} on your floor. Do NOT investigate. Move quickly and quietly. Confirm when you reach safety."

Safety assessment: "STEP 2: Are you in a secure location now? Can you see or hear the threat from where you are? Lock the door and stay away from windows. Tell me your exact location."

Lockdown guidance: "STEP 3: Lock and barricade the door. Turn off lights and move away from the door and windows. Silence your phone. Stay quiet and hidden. Confirm when secured."

Authority contact: "STEP 4: If you can do so safely and quietly, call 911 and report weapon threat at {{building location}}. Use text if calling is not safe. Confirm if authorities contacted."

RESPOND WITH NEXT SECURITY STEP ONLY:"""

        return full_prompt
    
    def analyze_security_message(self, message):
        """Analyze user message for security-specific context and urgency"""
        message_lower = message.lower()
        analysis = []
        
        # Threat assessment
        if any(word in message_lower for word in ["gunshot", "shots", "shooting", "gun", "weapon"]):
            analysis.append("THREAT: Active weapon threat confirmed - IMMEDIATE DANGER")
            self.security_assessment['threat_type'] = "active_weapon"
            self.emergency_phase = "lockdown"
        elif any(word in message_lower for word in ["suspicious", "threat", "danger", "scared"]):
            analysis.append("THREAT: Potential threat - assess and secure")
            self.security_assessment['threat_type'] = "potential"
        
        # User safety status
        if any(word in message_lower for word in ["safe", "secure", "locked", "hidden"]):
            analysis.append("SAFETY: User reports being in safe location")
            self.security_assessment['user_safety'] = "secure"
        elif any(word in message_lower for word in ["exposed", "open", "vulnerable", "can't hide"]):
            analysis.append("SAFETY: User in vulnerable position - need immediate safety")
            self.security_assessment['user_safety'] = "vulnerable"
        
        # Threat location
        if any(word in message_lower for word in ["nearby", "close", "same floor", "can hear"]):
            analysis.append("LOCATION: Threat is close - HIDE protocol")
            self.security_assessment['threat_location'] = "close"
        elif any(word in message_lower for word in ["far", "different floor", "can't hear", "distant"]):
            analysis.append("LOCATION: Threat distant - RUN protocol possible")
            self.security_assessment['threat_location'] = "distant"
        
        # Escape assessment
        if any(word in message_lower for word in ["can escape", "clear path", "exit available"]):
            analysis.append("ESCAPE: Escape route available - RUN protocol")
            self.security_assessment['escape_route'] = "available"
        elif any(word in message_lower for word in ["trapped", "blocked", "no exit", "can't leave"]):
            analysis.append("ESCAPE: No escape route - HIDE protocol")
            self.security_assessment['escape_route'] = "blocked"
        
        # Authority contact
        if any(word in message_lower for word in ["called 911", "police called", "authorities"]):
            analysis.append("AUTHORITIES: Emergency services contacted")
            self.security_assessment['authorities_called'] = "yes"
        elif any(word in message_lower for word in ["can't call", "no phone", "too dangerous"]):
            analysis.append("AUTHORITIES: Cannot contact emergency services safely")
            self.security_assessment['authorities_called'] = "unable"
        
        # Location detection
        if any(word in message_lower for word in ["ground floor", "ground", "lobby", "entrance"]):
            analysis.append("LOCATION: Ground Floor - Security control room available")
        elif any(word in message_lower for word in ["first floor", "1st floor", "floor 1", "medical"]):
            analysis.append("LOCATION: 1st Floor - Safe rooms and lockdown doors available")
        elif any(word in message_lower for word in ["second floor", "2nd floor", "floor 2", "admin"]):
            analysis.append("LOCATION: 2nd Floor - Administrative safe room available")
        
        # Urgency assessment
        if any(word in message_lower for word in ["emergency", "urgent", "now", "immediate", "help"]):
            analysis.append("URGENCY: CRITICAL - Immediate security response needed")
        
        return "; ".join(analysis) if analysis else "General weapon threat inquiry"
    
    def speak(self, text):
        """Display security specialist response and add to conversation history"""
        print(f"🔫 Security Specialist: {text}")
        self.conversation_history.append(f"Security Specialist: {text}")
    
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
        """Parse and store user location for security response context"""
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
        
        # Provide immediate security info for their floor
        self.provide_floor_security_info(floor)
    
    def provide_floor_security_info(self, floor):
        """Provide immediate security information for user's floor"""
        if floor in self.building_layout["Medical Center Building A"]["security_features"]:
            security = self.building_layout["Medical Center Building A"]["security_features"][floor]
            print(f"🔫 Security features on {floor}:")
            for feature in security:
                if 'feature' in feature:
                    print(f"   • {feature['feature']}: {feature['location']}")
        
        # Show safe rooms if available
        if floor in self.building_layout["Medical Center Building A"]["evacuation_routes"]:
            routes = self.building_layout["Medical Center Building A"]["evacuation_routes"][floor]
            if 'safe_rooms' in routes:
                print(f"🏠 Safe rooms on {floor}: {', '.join(routes['safe_rooms'])}")
            elif 'safe_room' in routes:
                print(f"🏠 Safe room on {floor}: {routes['safe_room']}")
    
    def check_for_gun_emergencies(self):
        """Monitor AlertAI server for gun/weapon emergencies only"""
        try:
            response = requests.get(f"{self.server_url}/api/alerts/active", timeout=5)
            if response.status_code == 200:
                data = response.json()
                alerts = data.get('alerts', [])
                
                # Filter for gun/weapon emergencies only
                gun_alerts = [alert for alert in alerts if alert.get('emergency_type', '').lower() in ['gun', 'weapon']]
                
                if gun_alerts:
                    # Check for new gun emergencies
                    for gun_alert in gun_alerts:
                        if not self.current_gun_emergency or gun_alert['id'] != self.current_gun_emergency.get('id'):
                            print(f"\n🔫 NEW GUN/WEAPON EMERGENCY DETECTED FROM SERVER!")
                            print(f"ID: {gun_alert['id']}")
                            print(f"Type: {gun_alert['emergency_type']}")
                            print(f"Location: {gun_alert['building']}")
                            print(f"Floor: {gun_alert.get('floor_affected', 'Unknown')}")
                            print(f"Time: {gun_alert['timestamp']}")
                            print("=" * 60)
                            
                            # Replace test emergency with real gun emergency
                            self.current_gun_emergency = gun_alert
                            self.test_emergency = gun_alert  # Use real data instead of test
                            return True
                else:
                    # No gun emergencies active
                    if self.current_gun_emergency:
                        print("🔫 Gun/weapon emergency resolved. Monitoring for new security threats...")
                        self.current_gun_emergency = None
                        
        except Exception as e:
            print(f"❌ Error checking for gun emergencies: {e}")
        
        return False
    
    def start_monitoring_mode(self):
        """Start monitoring AlertAI server for gun/weapon emergencies"""
        print("🔫 GUN/WEAPON EMERGENCY MONITORING MODE")
        print("=" * 60)
        print("🚨 Monitoring AlertAI server for GUN/WEAPON emergencies only")
        print("🔄 Checking server every 10 seconds")
        print("🚨 Will activate security specialist when weapon threat is detected")
        print("💬 Press Ctrl+C to stop monitoring")
        print("=" * 60)
        
        self.is_monitoring = True
        
        while self.is_monitoring:
            try:
                # Check for gun emergencies
                if self.check_for_gun_emergencies():
                    # Gun emergency detected - start security guidance
                    self.start_gun_emergency_scenario()
                    # After guidance session, continue monitoring
                    continue
                
                # Show monitoring status
                if not self.current_gun_emergency:
                    print("🔫 Monitoring for gun/weapon emergencies... (Ctrl+C to stop)")
                    time.sleep(10)
                    
            except KeyboardInterrupt:
                print("\n🛑 Gun/weapon emergency monitoring stopped by user")
                self.is_monitoring = False
                break
            except Exception as e:
                print(f"❌ Monitoring error: {e}")
                time.sleep(5)
    
    def start_gun_emergency_scenario(self):
        """Start the gun/weapon emergency scenario with specialized security guidance"""
        emergency = self.test_emergency
        
        print(f"\n🔫 GUN/WEAPON EMERGENCY DETECTED!")
        print(f"Building: {emergency['building']}")
        print(f"Floor Affected: {emergency.get('floor_affected', 'Unknown')}")
        print("🚨 SECURITY SPECIALIST ACTIVATED")
        print("=" * 60)
        
        # Get initial step-by-step security specialist response
        initial_message = f"GUN/WEAPON EMERGENCY: Weapon threat detected at {emergency['building']} on {emergency.get('floor_affected', 'unknown floor')}. I need immediate security guidance to keep people safe."
        
        print(f"👤 You: {initial_message}")
        response = self.call_gemini(initial_message)
        self.speak(response)
        
        # Start specialized security conversation
        self.security_conversation_loop()
    
    def security_conversation_loop(self):
        """Specialized gun/weapon emergency conversation loop"""
        print("\n🔫 STEP-BY-STEP Security Emergency Guidance Active")
        print("🚨 Follow each security step carefully - your safety depends on it")
        print("💬 Type your response to each step. Type 'quit' to exit, 'restart' for new scenario.")
        print("=" * 80)
        
        while True:
            try:
                # Get user input
                user_input = self.get_user_input()
                
                if user_input.lower() in ["quit", "exit", "stop"]:
                    final_message = "Ending security emergency session. REMEMBER: Stay hidden until official all-clear from police. Do not leave safe area."
                    response = self.call_gemini(final_message)
                    self.speak(response)
                    break
                
                if user_input.lower() in ["restart", "again", "new"]:
                    self.restart_security_scenario()
                    break
                
                if not user_input.strip():
                    continue
                
                # Update location if mentioned
                if not self.user_location and any(word in user_input.lower() for word in ["floor", "building", "room", "area", "ground", "first", "second"]):
                    self.parse_user_location(user_input)
                
                # Get specialized security response from Gemini
                response = self.call_gemini(user_input)
                self.speak(response)
                
            except KeyboardInterrupt:
                print("\n🛑 Security emergency session interrupted")
                print("🚨 SAFETY REMINDER: If weapon threat active, stay hidden and call 911")
                break
            except Exception as e:
                print(f"❌ Error in security emergency session: {e}")
                self.speak("🚨 GEMINI ERROR: Gun Emergency Agent requires Gemini 3 to function. Cannot provide security guidance without AI.")
                break
    
    def restart_security_scenario(self):
        """Restart the gun/weapon emergency scenario"""
        print("\n🔄 RESTARTING GUN/WEAPON EMERGENCY SCENARIO...")
        
        # Reset security assessment
        self.conversation_history = []
        self.user_location = None
        self.current_step = 1
        self.emergency_phase = "alert"
        self.security_assessment = {
            "threat_location": "unknown",
            "threat_type": "unknown", 
            "user_safety": "unknown",
            "lockdown_status": "unknown",
            "escape_route": "unknown",
            "authorities_called": "unknown"
        }
        
        # Wait a moment
        time.sleep(2)
        
        # Start new security scenario
        self.start_gun_emergency_scenario()

def main():
    """Main function to start Gun/Weapon Emergency Agent"""
    print("🔫 ALERTAI GUN/WEAPON EMERGENCY SPECIALIST - GEMINI 3")
    print("=" * 70)
    print("🚨 Expert security protocols and lockdown procedures")
    print("🏠 Specialized threat assessment and safe room guidance")
    print("🏢 Building-specific security features and evacuation routes")
    print("🚨 RUN-HIDE-FIGHT protocols and authority coordination")
    print("=" * 70)
    
    try:
        print("🔄 Initializing Gun/Weapon Emergency Agent...")
        agent = GunEmergencyAgent()
        print("✅ Agent initialized successfully!")
        
        # Choose mode
        print("\n🔫 GUN/WEAPON EMERGENCY AGENT MODES:")
        print("1. 🧪 Test Mode - Use hardcoded weapon threat scenario")
        print("2. 📡 Monitor Mode - Monitor AlertAI server for real gun/weapon emergencies")
        
        while True:
            try:
                choice = input("\nSelect mode (1 or 2): ").strip()
                if choice == "1":
                    print("🧪 Starting test gun/weapon emergency scenario...")
                    agent.start_gun_emergency_scenario()
                    break
                elif choice == "2":
                    print("📡 Starting gun/weapon emergency monitoring...")
                    agent.start_monitoring_mode()
                    break
                else:
                    print("❌ Invalid choice. Please enter 1 or 2.")
            except KeyboardInterrupt:
                print("\n👋 Gun/Weapon Emergency Agent stopped by user")
                break
                
    except KeyboardInterrupt:
        print("\n👋 Security emergency session ended by user")
        print("🚨 SAFETY REMINDER: Always call 911 for weapon threats and follow RUN-HIDE-FIGHT protocol")
    except Exception as e:
        print(f"❌ Failed to start gun/weapon emergency agent: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()