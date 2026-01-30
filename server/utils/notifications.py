import json
from datetime import datetime
from .twilio_whatsapp import send_whatsapp_emergency_alert

def send_alert_to_users(users, emergency_data, emergency_id=None):
    """
    Sends emergency alert to the filtered users
    Includes both user notifications and WhatsApp emergency alerts
    """
    print(f"\n🚨 SENDING EMERGENCY ALERTS 🚨")
    print(f"Emergency ID: {emergency_id}")
    print(f"Emergency Type: {emergency_data['emergency_type']}")
    print(f"Location: {emergency_data['building']}")
    print(f"Time: {emergency_data['timestamp']}")
    print(f"Users to notify: {len(users)}")
    print("-" * 50)
    
    # Send WhatsApp emergency alerts to emergency contacts
    print("📱 Sending WhatsApp emergency alerts...")
    whatsapp_success = send_whatsapp_emergency_alert(emergency_data, emergency_id)
    if whatsapp_success:
        print("✅ WhatsApp emergency alerts sent successfully")
    else:
        print("❌ WhatsApp emergency alerts failed or blocked (duplicate)")
    
    print("\n📱 Sending user notifications...")
    
    for user in users:
        alert_message = create_alert_message(user, emergency_data)
        
        # Mock notification - in production, use FCM
        print(f"📱 ALERT SENT TO: {user['name']} ({user['phone']})")
        print(f"   Distance: {user.get('distance_meters', 'N/A')}m away")
        print(f"   Message: {alert_message}")
        print(f"   FCM Token: {user['fcm_token']}")
        print()
        
        # TODO: Replace with actual FCM implementation
        # send_fcm_notification(user['fcm_token'], alert_message, emergency_data)

def create_alert_message(user, emergency_data):
    """Create personalized alert message for user"""
    distance = user.get('distance_meters', 0)
    
    message = f"🚨 EMERGENCY ALERT: {emergency_data['emergency_type']} reported at {emergency_data['building']}. You are {distance}m away. Please stay alert and follow safety protocols."
    
    return message

def send_fcm_notification(fcm_token, message, emergency_data):
    """
    Send Firebase Cloud Messaging notification
    TODO: Implement when FCM is set up
    """
    # Placeholder for FCM implementation
    notification_payload = {
        "to": fcm_token,
        "notification": {
            "title": f"Emergency Alert: {emergency_data['emergency_type']}",
            "body": message,
            "sound": "emergency_alert.wav",
            "priority": "high"
        },
        "data": {
            "emergency_type": emergency_data['emergency_type'],
            "location": json.dumps(emergency_data['location']),
            "building": emergency_data['building'],
            "timestamp": emergency_data['timestamp'],
            "image_url": emergency_data['image_url']
        }
    }
    
    # TODO: Send to FCM API
    # response = requests.post(FCM_URL, headers=headers, json=notification_payload)
    pass