#!/usr/bin/env python3
"""
Demo: WhatsApp Emergency Message Format
Shows what the WhatsApp message would look like when sent
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
    lat = location.get('lat', 11.849010)  # Default coordinates
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

def demo_whatsapp_message():
    """Demo the WhatsApp message format"""
    
    # Sample emergency data
    emergency_data = {
        "emergency_type": "Fire",
        "building": "Medical Center Building A", 
        "floor_affected": "2nd Floor",
        "timestamp": datetime.now().isoformat(),
        "location": {
            "lat": 11.849010,
            "lon": 13.056751
        }
    }
    
    message = format_emergency_message(emergency_data)
    
    print("🚀 AlertAI WhatsApp Emergency Message Demo")
    print("=" * 60)
    print("📱 This is what emergency contacts would receive:")
    print("=" * 60)
    print(message)
    print("=" * 60)
    
    # Show Google Maps URL
    maps_url = coordinates_to_google_maps_url(11.849010, 13.056751)
    print(f"🗺️ Google Maps URL: {maps_url}")
    
    print("\n✅ WhatsApp integration ready!")
    print("📋 To enable:")
    print("1. Get Twilio Account SID and Auth Token")
    print("2. Set up WhatsApp Sandbox or Business API")
    print("3. Configure emergency contacts in .env file")
    print("4. Test with: python test_whatsapp_emergency.py")

if __name__ == "__main__":
    demo_whatsapp_message()