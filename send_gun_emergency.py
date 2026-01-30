#!/usr/bin/env python3
"""
Simulate Edge Device - Gun/Weapon Emergency Test
Sends a gun/weapon emergency alert to the AlertAI server
"""
import requests
import json
from datetime import datetime

def send_gun_emergency():
    """
    Simulates an edge device sending a gun/weapon emergency to the server
    """
    print("🔫 SIMULATING EDGE DEVICE - GUN/WEAPON EMERGENCY")
    print("=" * 50)
    
    # Server endpoint
    server_url = "http://localhost:5000/emergency"
    
    # Gun/weapon emergency data (exactly as edge device would send)
    emergency_data = {
        "emergency_type": "Gun",
        "location": {
            "lat": 6.5244,  # Lagos coordinates
            "lon": 3.3792
        },
        "image_url": "test_images/gun_emergency.jpg",  # Local image path
        "timestamp": datetime.now().isoformat() + "Z",
        "building": "Medical Center Building A",
        "floor_affected": "1st Floor"  # Add floor information
    }
    
    print("📤 SENDING GUN/WEAPON EMERGENCY DATA:")
    print(f"   Emergency Type: {emergency_data['emergency_type']}")
    print(f"   Location: {emergency_data['location']['lat']}, {emergency_data['location']['lon']}")
    print(f"   Image: {emergency_data['image_url']}")
    print(f"   Building: {emergency_data['building']}")
    print(f"   Floor: {emergency_data['floor_affected']}")
    print(f"   Timestamp: {emergency_data['timestamp']}")
    
    try:
        # Send POST request to server (simulating edge device)
        print("\n🚀 Sending to AlertAI server...")
        response = requests.post(
            server_url,
            json=emergency_data,
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        
        print(f"\n📡 SERVER RESPONSE:")
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("   ✅ Gun/weapon emergency successfully sent to server!")
            print("   🤖 Server will now verify with Gemini AI")
            print("   🔫 Gun Emergency Agent should detect this!")
        else:
            print(f"   ❌ Server error: {response.status_code}")
            if response.text:
                print(f"   Error details: {response.text}")
                
    except requests.exceptions.ConnectionError:
        print("   ❌ Cannot connect to server!")
        print("   Make sure the server is running: python server/app.py")
    except requests.exceptions.Timeout:
        print("   ❌ Request timed out!")
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
    
    print("\n" + "=" * 50)
    print("🔍 Check server logs for Gemini verification results")
    print("🔫 Check Gun Emergency Agent for specialized security guidance")

if __name__ == "__main__":
    send_gun_emergency()