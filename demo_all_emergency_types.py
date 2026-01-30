#!/usr/bin/env python3
"""
Demo: All Emergency Types WhatsApp Messages
Shows WhatsApp messages for all emergency types
"""
from datetime import datetime

def coordinates_to_google_maps_url(lat, lon):
    """Convert coordinates to Google Maps URL"""
    return f"https://maps.google.com/maps?q={lat},{lon}"

def format_emergency_message(emergency_data):
    """Format emergency data into WhatsApp message"""
    emergency_type = emergency_data.get('emergency_type', 'Unknown Emergency')
    building = emergency_data.get('building', 'Unknown Location')
    floor = emergency_data.get('floor_affected', 'Unknown Floor')
    timestamp = emergency_data.get('timestamp', datetime.now().isoformat())
    
    # Get coordinates and convert to Google Maps URL
    location = emergency_data.get('location', {})
    lat = location.get('lat', 11.849010)
    lon = location.get('lon', 13.056751)
    maps_url = coordinates_to_google_maps_url(lat, lon)
    
    # Format timestamp for readability
    try:
        dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        formatted_time = dt.strftime('%Y-%m-%d %H:%M:%S')
    except:
        formatted_time = timestamp
    
    # Create emergency message
    message = f"""🚨 *EMERGENCY ALERT* 🚨

*Type:* {emergency_type}
*Location:* {building}
*Floor:* {floor}
*Time:* {formatted_time}

*Google Maps Location:*
{maps_url}

*Coordinates:* {lat}, {lon}

⚠️ *IMMEDIATE ACTION REQUIRED*
Emergency services have been notified. Please respond according to your emergency protocols.

_Sent by AlertAI Emergency System_"""
    
    return message

def demo_all_emergency_types():
    """Demo WhatsApp messages for all emergency types"""
    
    emergency_types = [
        {"type": "Fire", "floor": "2nd Floor", "emoji": "🔥"},
        {"type": "Blood", "floor": "1st Floor", "emoji": "🩸"},
        {"type": "Smoke", "floor": "Ground Floor", "emoji": "💨"},
        {"type": "Fallen Person", "floor": "1st Floor", "emoji": "🏥"},
        {"type": "Gun", "floor": "2nd Floor", "emoji": "🔫"}
    ]
    
    print("🚀 AlertAI WhatsApp Emergency Messages - All Types")
    print("=" * 70)
    
    for i, emergency in enumerate(emergency_types, 1):
        emergency_data = {
            "emergency_type": emergency["type"],
            "building": "Medical Center Building A", 
            "floor_affected": emergency["floor"],
            "timestamp": datetime.now().isoformat(),
            "location": {
                "lat": 11.849010,
                "lon": 13.056751
            }
        }
        
        message = format_emergency_message(emergency_data)
        
        print(f"\n{emergency['emoji']} EMERGENCY TYPE {i}: {emergency['type']}")
        print("-" * 50)
        print(message)
        print("-" * 50)
    
    print(f"\n🗺️ Google Maps URL: {coordinates_to_google_maps_url(11.849010, 13.056751)}")
    print("\n✅ All emergency types configured for WhatsApp alerts!")
    print("📱 Emergency contacts will receive these formatted messages")

if __name__ == "__main__":
    demo_all_emergency_types()