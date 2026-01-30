#!/usr/bin/env python3
"""
AlertAI Emergency Response Agent - Smart Gemini
Intelligent emergency guidance using Gemini 3 with conversation memory
"""
import os
import sys
import subprocess
import tempfile
import time
import json
from datetime import datetime
from config import config

class SmartAlertAIAgent:
    def __init__(self):
        self.name = "AlertAI Assistant (Smart Gemini)"
        self.user_location = None
        self.building_layout = {}
        self.conversation_history = []
        self.emergency_context = {}
        
        # Check for Gemini API key - use config system like other agents
        self.api_key = getattr(config, 'AI_API_KEY', '') or getattr(config, 'GEMINI_API_KEY', '')
        print(f"🔑 API Key loaded: {self.api_key[:20]}..." if self.api_key else "❌ No API key")
        if not self.api_key:
            print("❌ GEMINI_API_KEY not found in environment variables")
            sys.exit(1)
        
        # Hardcoded fire emergency for testing
        self.test_emergency = {
            "id": 999,
            "emergency_type": "Fire",
            "building": "Medical Center Building A",
            "location": {"lat": 11.849010, "lon": 13.056751},
            "timestamp": datetime.now().isoformat(),
            "image_url": "test_images/fire_emergency.jpg"
        }
        
        # Load building layouts and emergency resources
        self.load_building_data()
        
        print(f"🤖 {self.name} initialized and ready!")
        print(f"🧠 Using Gemini 3 with intelligent conversation memory")
    
    def load_building_data(self):
        """Load building layouts and emergency resource locations"""
        self.building_layout = {
            "Medical Center Building A": {
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
                }
            }
        }
    
    def call_gemini(self, user_message):
        """Call Gemini 3 API with full context and conversation history"""
        try:
            # Build comprehensive context
            context_prompt = self.build_context_prompt(user_message)
            
            # Create Python script for Gemini API call
            script_content = f'''
import google.generativeai as genai

api_key = "{self.api_key}"
genai.configure(api_key=api_key)

model = genai.GenerativeModel('gemini-3-flash')

prompt = """{context_prompt}"""

try:
    result = model.generate_content(prompt)
    print(result.text.strip())
except Exception as e:
    print(f"ERROR: {{str(e)}}")
'''
            
            # Write script to temp file and execute
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
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
                if response and not response.startswith("ERROR:"):
                    return response
                else:
                    return "I'm having trouble processing that. Let me provide standard safety guidance based on your situation."
            else:
                print(f"❌ Gemini API error: {result.stderr}")
                return "I'm experiencing technical difficulties. Please follow standard emergency procedures and contact emergency services."
                
        except Exception as e:
            print(f"❌ Error calling Gemini: {e}")
            return "I'm having technical issues. Please prioritize your safety and follow basic emergency procedures."
    
    def build_context_prompt(self, user_message):
        """Build comprehensive context prompt for Gemini"""
        
        # Emergency context
        emergency_info = f"""
EMERGENCY SITUATION:
- Type: {self.test_emergency['emergency_type']}
- Location: {self.test_emergency['building']}
- Time: {self.test_emergency['timestamp']}
- Status: Active emergency requiring immediate response
"""
        
        # User location context
        location_info = ""
        if self.user_location:
            location_info = f"""
USER LOCATION:
- Building: {self.user_location['building']}
- Floor: {self.user_location['floor']}
"""
        else:
            location_info = "USER LOCATION: Unknown - need to determine this"
        
        # Building data context
        building_data = f"""
BUILDING INFORMATION:
{json.dumps(self.building_layout, indent=2)}
"""
        
        # Conversation history
        history_context = ""
        if self.conversation_history:
            recent_history = self.conversation_history[-10:]  # Last 10 exchanges
            history_context = f"""
CONVERSATION HISTORY:
{chr(10).join(recent_history)}
"""
        
        # Current message analysis
        message_analysis = self.analyze_user_message(user_message)
        
        # Full prompt
        full_prompt = f"""You are AlertAI, an expert emergency response assistant providing real-time guidance during emergencies. You have access to detailed building information and must provide specific, actionable advice.

{emergency_info}
{location_info}
{building_data}
{history_context}

MESSAGE ANALYSIS:
{message_analysis}

CURRENT USER MESSAGE: "{user_message}"

RESPONSE GUIDELINES:
1. SAFETY FIRST: Always prioritize user safety above all else
2. BE SPECIFIC: Use exact building data (room locations, equipment types, exit routes)
3. BE CONCISE: Keep responses to 2-4 sentences unless giving step-by-step instructions
4. ASK CLARIFYING QUESTIONS: If user location or situation is unclear
5. PROVIDE OPTIONS: Offer both evacuation and assistance options when appropriate
6. INCLUDE WARNINGS: Mention specific hazards from building data when relevant
7. BE ENCOURAGING: Maintain calm, confident tone while being urgent about safety

SPECIAL INSTRUCTIONS:
- If user wants to fight fire, assess their location and fire size first
- Always mention specific fire extinguisher types and locations from building data
- Include evacuation routes specific to their floor
- Warn about special hazards (gas lines, electrical equipment, chemicals) in their area
- If user seems panicked, provide calm, step-by-step guidance

RESPOND AS ALERTAI:"""

        return full_prompt
    
    def analyze_user_message(self, message):
        """Analyze user message to understand intent and context"""
        message_lower = message.lower()
        analysis = []
        
        # Intent analysis
        if any(word in message_lower for word in ["fight", "extinguish", "put out", "stop", "tackle"]):
            analysis.append("INTENT: User wants to fight the fire")
        elif any(word in message_lower for word in ["evacuate", "leave", "exit", "escape", "get out"]):
            analysis.append("INTENT: User wants to evacuate")
        elif any(word in message_lower for word in ["where", "location", "floor", "room"]):
            analysis.append("INTENT: User is providing or asking about location")
        elif any(word in message_lower for word in ["scared", "afraid", "panic", "help", "don't know"]):
            analysis.append("INTENT: User is distressed and needs reassurance")
        elif any(word in message_lower for word in ["extinguisher", "equipment", "tools"]):
            analysis.append("INTENT: User asking about fire fighting equipment")
        
        # Location detection
        if any(word in message_lower for word in ["ground floor", "ground", "lobby", "entrance"]):
            analysis.append("LOCATION MENTIONED: Ground Floor")
        elif any(word in message_lower for word in ["first floor", "1st floor", "floor 1"]):
            analysis.append("LOCATION MENTIONED: 1st Floor")
        elif any(word in message_lower for word in ["second floor", "2nd floor", "floor 2"]):
            analysis.append("LOCATION MENTIONED: 2nd Floor")
        
        # Urgency level
        if any(word in message_lower for word in ["emergency", "urgent", "quickly", "fast", "now"]):
            analysis.append("URGENCY: High - immediate response needed")
        
        return "; ".join(analysis) if analysis else "General emergency inquiry"
    
    def speak(self, text):
        """Display AI response and add to conversation history"""
        print(f"🤖 AlertAI: {text}")
        self.conversation_history.append(f"AlertAI: {text}")
    
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
        """Parse and store user location"""
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
        print(f"📍 Location detected: {building}, {floor}")
    
    def start_emergency_scenario(self):
        """Start the emergency scenario with Gemini intelligence"""
        emergency = self.test_emergency
        
        print(f"\n🚨 EMERGENCY SCENARIO STARTING!")
        print(f"Type: {emergency['emergency_type']}")
        print(f"Location: {emergency['building']}")
        print("=" * 50)
        
        # Get initial AI response
        initial_message = f"EMERGENCY ALERT: {emergency['emergency_type']} detected at {emergency['building']}! I need immediate guidance on what to do."
        
        print(f"👤 You: {initial_message}")
        response = self.call_gemini(initial_message)
        self.speak(response)
        
        # Start conversation loop
        self.conversation_loop()
    
    def conversation_loop(self):
        """Main conversation loop with intelligent responses"""
        print("\n💬 Smart conversation started. Type 'quit' to exit, 'restart' to begin again.")
        print("=" * 60)
        
        while True:
            try:
                # Get user input
                user_input = self.get_user_input()
                
                if user_input.lower() in ["quit", "exit", "stop"]:
                    final_message = "I need to end this session now. Please ensure you're safe and emergency services are contacted."
                    response = self.call_gemini(final_message)
                    self.speak(response)
                    break
                
                if user_input.lower() in ["restart", "again"]:
                    self.restart_scenario()
                    break
                
                if not user_input.strip():
                    continue
                
                # Update location if mentioned
                if not self.user_location and any(word in user_input.lower() for word in ["floor", "building", "room", "area"]):
                    self.parse_user_location(user_input)
                
                # Get intelligent response from Gemini
                response = self.call_gemini(user_input)
                self.speak(response)
                
            except KeyboardInterrupt:
                print("\n🛑 Emergency session interrupted")
                break
            except Exception as e:
                print(f"❌ Error in conversation: {e}")
                self.speak("I'm experiencing technical difficulties. Please follow standard emergency procedures and contact emergency services.")
                break
    
    def restart_scenario(self):
        """Restart the emergency scenario"""
        print("\n🔄 RESTARTING SCENARIO...")
        
        # Reset state
        self.conversation_history = []
        self.user_location = None
        
        # Wait a moment
        time.sleep(2)
        
        # Start new scenario
        self.start_emergency_scenario()

def main():
    """Main function to start Smart AlertAI Agent"""
    print("🚨 ALERTAI EMERGENCY RESPONSE AGENT - SMART GEMINI")
    print("=" * 70)
    print("🧠 Intelligent responses with conversation memory")
    print("📊 Detailed building data integration")
    print("🎯 Context-aware emergency guidance")
    print("🔥 Testing with: FIRE EMERGENCY")
    print("🏢 Location: Medical Center Building A")
    print("=" * 70)
    
    try:
        agent = SmartAlertAIAgent()
        agent.start_emergency_scenario()
    except KeyboardInterrupt:
        print("\n👋 Emergency session ended by user")
    except Exception as e:
        print(f"❌ Failed to start agent: {e}")

if __name__ == "__main__":
    main()