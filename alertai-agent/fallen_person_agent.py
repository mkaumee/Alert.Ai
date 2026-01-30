#!/usr/bin/env python3
"""
AlertAI Fallen Person Emergency Agent - Specialized Gemini 3
Expert medical assessment and first aid guidance using Gemini 3 with specialized protocols
"""
print("🏥 Starting Fallen Person Emergency Agent...")
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

class FallenPersonAgent:
    def __init__(self):
        self.name = "AlertAI Fallen Person Emergency Specialist"
        self.user_location = None
        self.building_layout = {}
        self.conversation_history = []
        self.emergency_context = {}
        self.medical_assessment = {
            "consciousness": "unknown",
            "breathing": "unknown", 
            "pulse": "unknown",
            "bleeding": "unknown",
            "movement": "unknown",
            "pain_level": "unknown",
            "injury_location": "unknown"
        }
        self.current_step = 1
        self.emergency_phase = "dispatch"  # dispatch, arrival, assessment, treatment, monitoring
        self.user_at_scene = False
        
        # Server monitoring for fallen person emergencies
        self.server_url = getattr(config, 'ALERTAI_SERVER_URL', 'http://localhost:8000')
        self.is_monitoring = False
        self.current_fallen_emergency = None
        
        # Check for Gemini API key
        self.api_key = getattr(config, 'AI_API_KEY', '') or getattr(config, 'GEMINI_API_KEY', '')
        print(f"🔑 API Key loaded: {self.api_key[:20]}..." if self.api_key else "❌ No API key")
        if not self.api_key:
            print("❌ GEMINI_API_KEY not found in environment variables")
            sys.exit(1)
        
        # Fallen person emergency scenario for testing
        self.test_emergency = {
            "id": 2001,
            "emergency_type": "Fallen Person",
            "building": "Medical Center Building A",
            "location": {"lat": 11.849010, "lon": 13.056751},
            "timestamp": datetime.now().isoformat(),
            "image_url": "test_images/fallen_person_emergency.jpg",
            "floor_affected": "2nd Floor"
        }
        
        # Load specialized medical and building data
        self.load_medical_safety_data()
        
        print(f"🏥 {self.name} initialized and ready!")
        print(f"🧠 Using Gemini 3 with specialized medical assessment protocols")
        print(f"🚑 Expert knowledge: First aid, injury assessment, emergency positioning")
    
    def load_medical_safety_data(self):
        """Load specialized medical safety data and building information"""
        self.building_layout = {
            "Medical Center Building A": {
                "floors": ["Ground Floor", "1st Floor", "2nd Floor"],
                "medical_equipment": {
                    "Ground Floor": [
                        {
                            "equipment": "AED (Automated External Defibrillator)", 
                            "location": "Main reception desk", 
                            "status": "Active",
                            "last_check": "2024-01-20",
                            "instructions": "For cardiac emergencies only"
                        },
                        {
                            "equipment": "First Aid Kit (Comprehensive)", 
                            "location": "Security office", 
                            "contents": ["Bandages", "Antiseptic", "Splints", "Emergency blanket"],
                            "last_restocked": "2024-01-15"
                        },
                        {
                            "equipment": "Wheelchair", 
                            "location": "Near main entrance", 
                            "condition": "Good",
                            "weight_limit": "300 lbs"
                        }
                    ],
                    "1st Floor": [
                        {
                            "equipment": "Medical Oxygen", 
                            "location": "Nursing station", 
                            "pressure": "Full",
                            "flow_rates": "1-15 L/min",
                            "trained_staff_required": True
                        },
                        {
                            "equipment": "Stretcher/Gurney", 
                            "location": "Medical equipment room", 
                            "condition": "Excellent",
                            "weight_limit": "500 lbs"
                        },
                        {
                            "equipment": "Spine Board", 
                            "location": "Emergency supply closet", 
                            "condition": "Good",
                            "use": "Spinal injury suspected"
                        }
                    ],
                    "2nd Floor": [
                        {
                            "equipment": "First Aid Kit (Basic)", 
                            "location": "Break room", 
                            "contents": ["Basic bandages", "Antiseptic wipes", "Pain relievers"],
                            "last_restocked": "2024-01-10"
                        },
                        {
                            "equipment": "Emergency Blankets", 
                            "location": "Storage closet", 
                            "quantity": "5 thermal blankets",
                            "use": "Shock prevention, warmth"
                        },
                        {
                            "equipment": "Communication Radio", 
                            "location": "Administrative office", 
                            "channel": "Emergency frequency",
                            "range": "Building-wide"
                        }
                    ]
                },
                "evacuation_routes": {
                    "Ground Floor": {
                        "primary": "Main entrance (wheelchair accessible)",
                        "secondary": "Back exit (wheelchair accessible)",
                        "medical_access": "Direct ambulance access at main entrance"
                    },
                    "1st Floor": {
                        "primary": "Medical elevator (for stretcher transport)",
                        "secondary": "Emergency stairwell A (carry assistance required)",
                        "medical_access": "Elevator directly to ambulance bay"
                    },
                    "2nd Floor": {
                        "primary": "Medical elevator (for stretcher transport)",
                        "secondary": "Emergency stairwell A (carry assistance required)",
                        "tertiary": "Emergency stairwell B (carry assistance required)"
                    }
                },
                "medical_personnel": {
                    "on_site_staff": [
                        {"role": "Registered Nurse", "location": "1st Floor nursing station", "availability": "24/7"},
                        {"role": "Security Guard (First Aid Certified)", "location": "Ground Floor", "availability": "24/7"},
                        {"role": "Facility Manager (CPR Certified)", "location": "Ground Floor office", "availability": "Business hours"}
                    ],
                    "emergency_contacts": {
                        "ems": "911",
                        "poison_control": "1-800-222-1222",
                        "hospital_direct": "+234-800-HOSPITAL",
                        "building_medical": "+234-800-MEDIC"
                    }
                },
                "medical_hazards": {
                    "Ground Floor": [
                        {"hazard": "Wet floors near entrance", "risk": "Slip and fall", "mitigation": "Caution signs, non-slip mats"},
                        {"hazard": "Automatic doors", "risk": "Entrapment", "mitigation": "Emergency stop buttons available"}
                    ],
                    "1st Floor": [
                        {"hazard": "Medical oxygen lines", "risk": "Fire acceleration", "mitigation": "No smoking, spark-free zone"},
                        {"hazard": "Patient lifting equipment", "risk": "Mechanical injury", "mitigation": "Trained operators only"}
                    ],
                    "2nd Floor": [
                        {"hazard": "Open stairwells", "risk": "Fall hazard", "mitigation": "Safety railings, emergency lighting"},
                        {"hazard": "Office furniture", "risk": "Sharp edges", "mitigation": "Clear pathways for emergency access"}
                    ]
                }
            }
        }
        
        # Medical assessment protocols
        self.medical_protocols = {
            "primary_assessment": {
                "A": "Airway - Check if airway is clear and open",
                "B": "Breathing - Look, listen, feel for breathing",
                "C": "Circulation - Check pulse and look for severe bleeding",
                "D": "Disability - Check for spinal injury, movement",
                "E": "Exposure - Look for obvious injuries, maintain warmth"
            },
            "consciousness_levels": {
                "alert": "Awake, responsive, oriented",
                "verbal": "Responds to verbal commands",
                "pain": "Responds only to painful stimuli", 
                "unresponsive": "No response to any stimuli"
            },
            "positioning_guidelines": {
                "conscious_breathing": "Recovery position (on side) if no spinal injury suspected",
                "unconscious_breathing": "Recovery position, monitor airway",
                "not_breathing": "Flat on back for CPR if trained",
                "spinal_injury": "Do NOT move - stabilize head and neck",
                "shock": "Elevate legs 12 inches if no spinal injury"
            },
            "do_not_move_if": [
                "Suspected spinal injury",
                "Neck or back pain",
                "Numbness or tingling in extremities",
                "Person fell from height",
                "Unconscious from head trauma",
                "Severe pain when attempting to move"
            ]
        }
    
    def call_gemini(self, user_message):
        """Call Gemini 3 API with specialized medical assessment context - GEMINI ONLY"""
        try:
            # Build medical-specific context
            context_prompt = self.build_medical_context_prompt(user_message)
            
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
                    return f"🚨 GEMINI API ERROR: {error_msg}\n\n❌ Fallen Person Emergency Agent requires Gemini 3 to function. Please resolve API issues."
            else:
                return f"🚨 GEMINI CONNECTION FAILED: {result.stderr}\n\n❌ Fallen Person Emergency Agent is Gemini-powered only. Cannot provide guidance without Gemini."
                
        except Exception as e:
            return f"🚨 GEMINI SYSTEM ERROR: {str(e)}\n\n❌ Fallen Person Emergency Agent requires Gemini 3. Please check API configuration and quota."
    
    def build_medical_context_prompt(self, user_message):
        """Build specialized medical assessment context prompt for Gemini"""
        
        # Medical emergency context
        emergency_info = f"""
FALLEN PERSON EMERGENCY SITUATION:
- Type: {self.test_emergency['emergency_type']}
- Location: {self.test_emergency['building']}
- Floor Affected: {self.test_emergency.get('floor_affected', 'Unknown')}
- Time: {self.test_emergency['timestamp']}
- Status: ACTIVE MEDICAL EMERGENCY - Immediate assessment required
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
        
        # Medical assessment
        medical_assessment_info = f"""
MEDICAL ASSESSMENT STATUS:
- Emergency Phase: {self.emergency_phase}
- User At Scene: {self.user_at_scene}
- Consciousness: {self.medical_assessment['consciousness']}
- Breathing: {self.medical_assessment['breathing']}
- Pulse: {self.medical_assessment['pulse']}
- Bleeding: {self.medical_assessment['bleeding']}
- Movement: {self.medical_assessment['movement']}
- Pain Level: {self.medical_assessment['pain_level']}
- Injury Location: {self.medical_assessment['injury_location']}
"""
        
        # Building medical data
        building_data = f"""
MEDICAL BUILDING DATA:
{json.dumps(self.building_layout, indent=2)}
"""
        
        # Medical protocols
        protocols_data = f"""
MEDICAL PROTOCOLS:
{json.dumps(self.medical_protocols, indent=2)}
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
        message_analysis = self.analyze_medical_message(user_message)
        
        # Full specialized medical prompt
        full_prompt = f"""You are AlertAI Fallen Person Emergency Specialist, an expert medical first aid professional providing real-time guidance for fallen person emergencies. You have specialized knowledge of medical assessment, first aid, injury care, and emergency positioning.

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
   - Step 1: Direct user to go to fallen person's location
   - Step 2: Confirm user has arrived and can see the person
   - Step 3: Begin medical assessment (breathing, consciousness, wounds)
   - Step 4: Guide appropriate response based on assessment
   - Step 5: Ongoing care and emergency services coordination
5. **USE BUILDING DATA**: Reference specific locations, medical equipment, personnel
6. **SAFETY FIRST**: Ensure scene safety before medical assessment

REALISTIC EMERGENCY SEQUENCE:
Step 1: Direct user to fallen person's location with safety instructions
Step 2: Confirm arrival and initial visual assessment
Step 3: Check consciousness (Can they hear you? Are they awake?)
Step 4: Assess breathing (Are they breathing normally?)
Step 5: Look for visible injuries (bleeding, obvious wounds, deformities)
Step 6: Check for spinal injury risk before any movement
Step 7: Appropriate care based on findings (positioning, first aid, monitoring)
Step 8: Emergency services coordination and ongoing monitoring

CRITICAL MEDICAL RULES:
- DO NOT MOVE if spinal injury suspected
- Call 911 immediately for unconscious person
- Recovery position ONLY if no spinal injury
- Monitor breathing continuously
- Keep person warm (prevent shock)
- Never give food or water to unconscious person
- Document time and changes in condition

CPR GUIDANCE PROTOCOL:
- If person is NOT BREATHING and NO PULSE: CPR is needed immediately
- If trained person available: Direct them to start CPR immediately
- If NO trained person available: Say "If no one here is trained in CPR, tap the CPR Monitor button so the AI can guide you through chest compressions and follow the beeping sound in the CPR monitor"
- CPR is 30 chest compressions followed by 2 rescue breaths
- Compression rate: 100-120 per minute (follow the beep)
- Push hard and fast on center of chest
- Allow complete chest recoil between compressions

RESPONSE STYLE:
- Be calm and reassuring
- Use specific building medical data (equipment locations, trained staff)
- Provide clear step-by-step medical instructions
- Ask critical assessment questions (consciousness, breathing, movement)
- Include specific safety warnings
- Reference available medical equipment and personnel

EXAMPLE RESPONSES FOR REALISTIC FLOW:
Initial contact: "STEP 1: A person has fallen on {{emergency floor}}. Go to {{specific location}} immediately and check on them. Look around for any hazards as you approach. Confirm when you can see the person."

After arrival: "STEP 2: Can you see the person clearly? Are they awake and moving, or do they appear unconscious? Tell me what you observe. Do NOT touch them yet."

Medical assessment: "STEP 3: Call out to them loudly - 'Are you okay? Can you hear me?' Watch for any response. Are they breathing normally? Confirm their response level."

Based on findings: "STEP 4: Look for any visible bleeding, wounds, or obvious injuries. Do NOT move them. Tell me what injuries you can see. Are they in pain when they try to move?"

RESPOND WITH NEXT MEDICAL STEP ONLY:"""

        return full_prompt
    
    def analyze_medical_message(self, message):
        """Analyze user message for medical-specific context and urgency"""
        message_lower = message.lower()
        analysis = []
        
        # Scene arrival detection
        if any(word in message_lower for word in ["i can see", "i see", "i'm here", "arrived", "at the person", "found them"]):
            analysis.append("ARRIVAL: User has arrived at scene")
            self.user_at_scene = True
            self.emergency_phase = "assessment"
        elif any(word in message_lower for word in ["going", "on my way", "heading", "walking"]):
            analysis.append("DISPATCH: User is en route to fallen person")
            self.emergency_phase = "dispatch"
        
        # Medical response intent
        if any(word in message_lower for word in ["help", "assist", "aid", "treat", "care"]):
            analysis.append("INTENT: User wants to provide medical assistance")
        elif any(word in message_lower for word in ["call", "911", "ambulance", "ems", "emergency"]):
            analysis.append("INTENT: User wants to call emergency services")
        elif any(word in message_lower for word in ["move", "lift", "carry", "transport"]):
            analysis.append("INTENT: User wants to move the person - ASSESS SPINAL INJURY FIRST")
        elif any(word in message_lower for word in ["check", "assess", "examine", "look"]):
            analysis.append("INTENT: User wants to assess condition")
        
        # Consciousness level detection
        if any(word in message_lower for word in ["awake", "alert", "talking", "responsive"]):
            analysis.append("CONSCIOUSNESS: Person appears conscious/alert")
            self.medical_assessment['consciousness'] = "alert"
        elif any(word in message_lower for word in ["unconscious", "unresponsive", "not responding", "out cold"]):
            analysis.append("CONSCIOUSNESS: Person appears unconscious - CRITICAL")
            self.medical_assessment['consciousness'] = "unresponsive"
        elif any(word in message_lower for word in ["groggy", "confused", "dazed"]):
            analysis.append("CONSCIOUSNESS: Altered consciousness - monitor closely")
            self.medical_assessment['consciousness'] = "verbal"
        
        # Breathing assessment
        if any(word in message_lower for word in ["breathing", "breath", "air"]):
            if any(word in message_lower for word in ["not breathing", "no breath", "stopped breathing"]):
                analysis.append("BREATHING: NOT BREATHING - IMMEDIATE CPR NEEDED")
                self.medical_assessment['breathing'] = "absent"
            elif any(word in message_lower for word in ["difficulty", "trouble", "labored", "gasping"]):
                analysis.append("BREATHING: Difficulty breathing - monitor airway")
                self.medical_assessment['breathing'] = "labored"
            else:
                analysis.append("BREATHING: Breathing mentioned - assess quality")
                self.medical_assessment['breathing'] = "present"
        
        # CPR-related keywords detection
        if any(word in message_lower for word in ["not breathing", "no pulse", "cardiac arrest", "heart stopped", "cpr", "chest compressions"]):
            analysis.append("CPR NEEDED: Person requires immediate CPR - recommend CPR monitor if no trained person available")
        
        # Bleeding assessment
        if any(word in message_lower for word in ["blood", "bleeding", "cut", "wound"]):
            if any(word in message_lower for word in ["lot of blood", "heavy bleeding", "severe", "gushing"]):
                analysis.append("BLEEDING: Severe bleeding - immediate pressure needed")
                self.medical_assessment['bleeding'] = "severe"
            else:
                analysis.append("BLEEDING: Bleeding present - assess severity")
                self.medical_assessment['bleeding'] = "present"
        
        # Movement/spinal assessment
        if any(word in message_lower for word in ["can't move", "paralyzed", "numb", "tingling"]):
            analysis.append("MOVEMENT: Possible spinal injury - DO NOT MOVE")
            self.medical_assessment['movement'] = "impaired"
        elif any(word in message_lower for word in ["moving", "can move", "wiggling"]):
            analysis.append("MOVEMENT: Person can move - good sign")
            self.medical_assessment['movement'] = "normal"
        
        # Pain assessment
        if any(word in message_lower for word in ["pain", "hurt", "ache", "sore"]):
            if any(word in message_lower for word in ["severe", "excruciating", "terrible", "10/10"]):
                analysis.append("PAIN: Severe pain reported")
                self.medical_assessment['pain_level'] = "severe"
            else:
                analysis.append("PAIN: Pain reported - assess location and severity")
                self.medical_assessment['pain_level'] = "moderate"
        
        # Location detection
        if any(word in message_lower for word in ["ground floor", "ground", "lobby", "entrance"]):
            analysis.append("LOCATION: Ground Floor - AED and wheelchair available")
        elif any(word in message_lower for word in ["first floor", "1st floor", "floor 1", "nursing"]):
            analysis.append("LOCATION: 1st Floor - Medical oxygen and stretcher available")
        elif any(word in message_lower for word in ["second floor", "2nd floor", "floor 2", "office"]):
            analysis.append("LOCATION: 2nd Floor - Basic first aid and emergency blankets available")
        
        # Urgency assessment
        if any(word in message_lower for word in ["emergency", "urgent", "critical", "dying", "serious"]):
            analysis.append("URGENCY: HIGH - Life-threatening situation possible")
        
        return "; ".join(analysis) if analysis else "General medical emergency inquiry"
    
    def speak(self, text):
        """Display medical specialist response and add to conversation history"""
        print(f"🏥 Medical Specialist: {text}")
        self.conversation_history.append(f"Medical Specialist: {text}")
    
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
        
        # Provide immediate medical equipment info for their floor
        self.provide_floor_medical_info(floor)
    
    def provide_floor_medical_info(self, floor):
        """Provide immediate medical equipment information for user's floor"""
        if floor in self.building_layout["Medical Center Building A"]["medical_equipment"]:
            equipment = self.building_layout["Medical Center Building A"]["medical_equipment"][floor]
            print(f"🏥 Medical equipment on {floor}:")
            for item in equipment:
                print(f"   • {item['equipment']}: {item['location']}")
        
        # Show trained personnel if available
        personnel = self.building_layout["Medical Center Building A"]["medical_personnel"]["on_site_staff"]
        available_staff = [staff for staff in personnel if floor.lower() in staff['location'].lower() or staff['availability'] == '24/7']
        if available_staff:
            print(f"👨‍⚕️ Trained staff available:")
            for staff in available_staff:
                print(f"   • {staff['role']}: {staff['location']}")
    
    def check_for_fallen_person_emergencies(self):
        """Monitor AlertAI server for fallen person emergencies only"""
        try:
            response = requests.get(f"{self.server_url}/api/alerts/active", timeout=5)
            if response.status_code == 200:
                data = response.json()
                alerts = data.get('alerts', [])
                
                # Filter for fallen person emergencies only
                fallen_alerts = [alert for alert in alerts if alert.get('emergency_type', '').lower() == 'fallen person']
                
                if fallen_alerts:
                    # Check for new fallen person emergencies
                    for fallen_alert in fallen_alerts:
                        if not self.current_fallen_emergency or fallen_alert['id'] != self.current_fallen_emergency.get('id'):
                            print(f"\n🏥 NEW FALLEN PERSON EMERGENCY DETECTED FROM SERVER!")
                            print(f"ID: {fallen_alert['id']}")
                            print(f"Type: {fallen_alert['emergency_type']}")
                            print(f"Location: {fallen_alert['building']}")
                            print(f"Floor: {fallen_alert.get('floor_affected', 'Unknown')}")
                            print(f"Time: {fallen_alert['timestamp']}")
                            print("=" * 60)
                            
                            # Replace test emergency with real fallen person emergency
                            self.current_fallen_emergency = fallen_alert
                            self.test_emergency = fallen_alert  # Use real data instead of test
                            return True
                else:
                    # No fallen person emergencies active
                    if self.current_fallen_emergency:
                        print("🏥 Fallen person emergency resolved. Monitoring for new medical emergencies...")
                        self.current_fallen_emergency = None
                        
        except Exception as e:
            print(f"❌ Error checking for fallen person emergencies: {e}")
        
        return False
    
    def start_monitoring_mode(self):
        """Start monitoring AlertAI server for fallen person emergencies"""
        print("🏥 FALLEN PERSON EMERGENCY MONITORING MODE")
        print("=" * 60)
        print("🚑 Monitoring AlertAI server for FALLEN PERSON emergencies only")
        print("🔄 Checking server every 10 seconds")
        print("🚨 Will activate medical specialist when fallen person is detected")
        print("💬 Press Ctrl+C to stop monitoring")
        print("=" * 60)
        
        self.is_monitoring = True
        
        while self.is_monitoring:
            try:
                # Check for fallen person emergencies
                if self.check_for_fallen_person_emergencies():
                    # Fallen person emergency detected - start medical guidance
                    self.start_fallen_person_scenario()
                    # After guidance session, continue monitoring
                    continue
                
                # Show monitoring status
                if not self.current_fallen_emergency:
                    print("🏥 Monitoring for fallen person emergencies... (Ctrl+C to stop)")
                    time.sleep(10)
                    
            except KeyboardInterrupt:
                print("\n🛑 Fallen person emergency monitoring stopped by user")
                self.is_monitoring = False
                break
            except Exception as e:
                print(f"❌ Monitoring error: {e}")
                time.sleep(5)
    
    def start_fallen_person_scenario(self):
        """Start the fallen person emergency scenario with specialized medical guidance"""
        emergency = self.test_emergency
        
        print(f"\n🏥 FALLEN PERSON EMERGENCY DETECTED!")
        print(f"Building: {emergency['building']}")
        print(f"Floor Affected: {emergency.get('floor_affected', 'Unknown')}")
        print("🚑 MEDICAL SPECIALIST ACTIVATED")
        print("=" * 60)
        
        # Get initial step-by-step medical specialist response
        initial_message = f"FALLEN PERSON EMERGENCY: Someone has fallen at {emergency['building']} on {emergency.get('floor_affected', 'unknown floor')}. I need to direct someone to go check on them and provide medical guidance."
        
        print(f"👤 You: {initial_message}")
        response = self.call_gemini(initial_message)
        self.speak(response)
        
        # Start specialized medical conversation
        self.medical_conversation_loop()
    
    def medical_conversation_loop(self):
        """Specialized fallen person emergency conversation loop"""
        print("\n🏥 STEP-BY-STEP Medical Emergency Guidance Active")
        print("🚑 Follow each medical step carefully and confirm completion before next step")
        print("💬 Type your response to each step. Type 'quit' to exit, 'restart' for new scenario.")
        print("=" * 80)
        
        while True:
            try:
                # Get user input
                user_input = self.get_user_input()
                
                if user_input.lower() in ["quit", "exit", "stop"]:
                    final_message = "Ending medical emergency session. REMEMBER: Call 911 for serious injuries, monitor breathing and pulse continuously."
                    response = self.call_gemini(final_message)
                    self.speak(response)
                    break
                
                if user_input.lower() in ["restart", "again", "new"]:
                    self.restart_medical_scenario()
                    break
                
                if not user_input.strip():
                    continue
                
                # Update location if mentioned
                if not self.user_location and any(word in user_input.lower() for word in ["floor", "building", "room", "area", "ground", "first", "second"]):
                    self.parse_user_location(user_input)
                
                # Get specialized medical response from Gemini
                response = self.call_gemini(user_input)
                self.speak(response)
                
            except KeyboardInterrupt:
                print("\n🛑 Medical emergency session interrupted")
                print("🚨 SAFETY REMINDER: If person is unconscious or not breathing, call 911 immediately")
                break
            except Exception as e:
                print(f"❌ Error in medical emergency session: {e}")
                self.speak("🚨 GEMINI ERROR: Fallen Person Emergency Agent requires Gemini 3 to function. Cannot provide medical guidance without AI.")
                break
    
    def restart_medical_scenario(self):
        """Restart the fallen person emergency scenario"""
        print("\n🔄 RESTARTING FALLEN PERSON EMERGENCY SCENARIO...")
        
        # Reset medical assessment
        self.conversation_history = []
        self.user_location = None
        self.current_step = 1
        self.emergency_phase = "dispatch"
        self.user_at_scene = False
        self.medical_assessment = {
            "consciousness": "unknown",
            "breathing": "unknown", 
            "pulse": "unknown",
            "bleeding": "unknown",
            "movement": "unknown",
            "pain_level": "unknown",
            "injury_location": "unknown"
        }
        
        # Wait a moment
        time.sleep(2)
        
        # Start new medical scenario
        self.start_fallen_person_scenario()

def main():
    """Main function to start Fallen Person Emergency Agent"""
    print("🏥 ALERTAI FALLEN PERSON EMERGENCY SPECIALIST - GEMINI 3")
    print("=" * 70)
    print("🚑 Expert medical assessment and first aid protocols")
    print("🩺 Specialized injury care and emergency positioning knowledge")
    print("🏢 Building-specific medical equipment and personnel integration")
    print("🚨 Primary assessment, positioning, and monitoring procedures")
    print("=" * 70)
    
    try:
        print("🔄 Initializing Fallen Person Emergency Agent...")
        agent = FallenPersonAgent()
        print("✅ Agent initialized successfully!")
        
        # Choose mode
        print("\n🏥 FALLEN PERSON EMERGENCY AGENT MODES:")
        print("1. 🧪 Test Mode - Use hardcoded fallen person scenario")
        print("2. 📡 Monitor Mode - Monitor AlertAI server for real fallen person emergencies")
        
        while True:
            try:
                choice = input("\nSelect mode (1 or 2): ").strip()
                if choice == "1":
                    print("🧪 Starting test fallen person emergency scenario...")
                    agent.start_fallen_person_scenario()
                    break
                elif choice == "2":
                    print("📡 Starting fallen person emergency monitoring...")
                    agent.start_monitoring_mode()
                    break
                else:
                    print("❌ Invalid choice. Please enter 1 or 2.")
            except KeyboardInterrupt:
                print("\n👋 Fallen Person Emergency Agent stopped by user")
                break
                
    except KeyboardInterrupt:
        print("\n👋 Medical emergency session ended by user")
        print("🚨 SAFETY REMINDER: Always call 911 for serious medical emergencies")
    except Exception as e:
        print(f"❌ Failed to start fallen person emergency agent: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()