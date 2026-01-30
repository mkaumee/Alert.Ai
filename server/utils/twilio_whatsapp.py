#!/usr/bin/env python3
"""
Twilio WhatsApp Emergency Notification System
Sends emergency alerts via WhatsApp using Twilio API
"""
import os
import sys
import requests
from datetime import datetime, timedelta
from twilio.rest import Client

# Try to import config, fallback to environment variables
try:
    # Try importing from server directory
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    from config import config
except ImportError:
    # Fallback: create a simple config object that reads from environment
    class SimpleConfig:
        def __getattr__(self, name):
            return os.getenv(name, '')
    config = SimpleConfig()

class TwilioWhatsAppNotifier:
    def __init__(self):
        # Get Twilio credentials from environment or config
        self.account_sid = getattr(config, 'TWILIO_ACCOUNT_SID', '') or os.getenv('TWILIO_ACCOUNT_SID', '')
        self.auth_token = getattr(config, 'TWILIO_AUTH_TOKEN', '') or os.getenv('TWILIO_AUTH_TOKEN', '')
        self.whatsapp_from = getattr(config, 'TWILIO_WHATSAPP_FROM', '') or os.getenv('TWILIO_WHATSAPP_FROM', 'whatsapp:+14155238886')
        
        # Emergency contact numbers (WhatsApp format: whatsapp:+1234567890)
        emergency_contact_1 = getattr(config, 'EMERGENCY_CONTACT_1', '') or os.getenv('EMERGENCY_CONTACT_1', '')
        emergency_contact_2 = getattr(config, 'EMERGENCY_CONTACT_2', '') or os.getenv('EMERGENCY_CONTACT_2', '')
        emergency_contact_3 = getattr(config, 'EMERGENCY_CONTACT_3', '') or os.getenv('EMERGENCY_CONTACT_3', '')
        
        self.emergency_contacts = [contact for contact in [emergency_contact_1, emergency_contact_2, emergency_contact_3] if contact and contact.startswith('whatsapp:')]
        
        # Track processed emergency IDs to prevent duplicates
        self.processed_emergency_ids = set()
        
        # Debug output
        print(f"🔍 Twilio Debug Info:")
        print(f"   Account SID: {self.account_sid[:10]}..." if self.account_sid else "   Account SID: Not found")
        print(f"   Auth Token: {self.auth_token[:10]}..." if self.auth_token else "   Auth Token: Not found")
        print(f"   WhatsApp From: {self.whatsapp_from}")
        print(f"   Emergency Contacts: {len(self.emergency_contacts)} configured")
        print(f"   Duplicate Prevention: Emergency ID tracking enabled")
        
        # Initialize Twilio client
        if self.account_sid and self.auth_token:
            try:
                self.client = Client(self.account_sid, self.auth_token)
                print(f"✅ Twilio WhatsApp initialized - From: {self.whatsapp_from}")
                print(f"📱 Emergency contacts: {len(self.emergency_contacts)} configured")
            except Exception as e:
                self.client = None
                print(f"❌ Twilio client initialization failed: {e}")
        else:
            self.client = None
            print("⚠️ Twilio credentials not found - WhatsApp notifications disabled")
            print("   Make sure TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN are set in server/.env")
    
    def is_emergency_already_processed(self, emergency_id):
        """Check if this emergency ID has already been processed"""
        if emergency_id in self.processed_emergency_ids:
            print(f"🚫 DUPLICATE EMERGENCY BLOCKED: ID {emergency_id} already processed")
            print(f"   Total processed emergencies: {len(self.processed_emergency_ids)}")
            return True
        
        # Mark this emergency as processed
        self.processed_emergency_ids.add(emergency_id)
        print(f"✅ NEW EMERGENCY: ID {emergency_id} - WhatsApp alerts will be sent")
        return False
    
    def coordinates_to_google_maps_url(self, lat, lon):
        """Convert coordinates to Google Maps URL"""
        return f"https://maps.google.com/maps?q={lat},{lon}"
    
    def format_emergency_message(self, emergency_data):
        """Format emergency data into WhatsApp message"""
        emergency_type = emergency_data.get('emergency_type', 'Unknown Emergency')
        building = emergency_data.get('building', 'Unknown Location')
        floor = emergency_data.get('floor_affected', 'Unknown Floor')
        timestamp = emergency_data.get('timestamp', datetime.now().isoformat())
        
        # Get coordinates and convert to Google Maps URL
        location = emergency_data.get('location', {})
        lat = location.get('lat', 11.849010)  # Default coordinates
        lon = location.get('lon', 13.056751)
        maps_url = self.coordinates_to_google_maps_url(lat, lon)
        
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
    
    def send_whatsapp_alert(self, emergency_data, emergency_id=None):
        """Send WhatsApp emergency alert to all configured contacts"""
        if not self.client:
            print("❌ Twilio client not initialized - cannot send WhatsApp alerts")
            return False
        
        if not self.emergency_contacts:
            print("⚠️ No emergency contacts configured - WhatsApp alerts not sent")
            return False
        
        # Check if this emergency has already been processed
        if emergency_id and self.is_emergency_already_processed(emergency_id):
            return False  # Skip sending duplicate alert
        
        emergency_type = emergency_data.get('emergency_type', 'Unknown')
        building = emergency_data.get('building', 'Unknown Location')
        
        message_body = self.format_emergency_message(emergency_data)
        
        print(f"\n📱 SENDING WHATSAPP EMERGENCY ALERTS")
        print(f"Emergency ID: {emergency_id}")
        print(f"Emergency Type: {emergency_type}")
        print(f"Building: {building}")
        print(f"Recipients: {len(self.emergency_contacts)}")
        print("-" * 50)
        
        success_count = 0
        
        for contact in self.emergency_contacts:
            try:
                message = self.client.messages.create(
                    body=message_body,
                    from_=self.whatsapp_from,
                    to=contact
                )
                
                print(f"✅ WhatsApp sent to {contact}")
                print(f"   Message SID: {message.sid}")
                print(f"   Status: {message.status}")
                success_count += 1
                
            except Exception as e:
                print(f"❌ Failed to send WhatsApp to {contact}: {str(e)}")
        
        print(f"\n📊 WhatsApp Alert Summary: {success_count}/{len(self.emergency_contacts)} sent successfully")
        return success_count > 0
    
    def test_whatsapp_connection(self):
        """Test WhatsApp connection with a test message"""
        if not self.client:
            return False, "Twilio client not initialized"
        
        if not self.emergency_contacts:
            return False, "No emergency contacts configured"
        
        test_message = """🧪 *AlertAI Test Message* 🧪

This is a test message from the AlertAI Emergency System.

If you received this message, WhatsApp notifications are working correctly.

_Test sent at: {}_""".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        
        try:
            # Send to first contact only for testing
            contact = self.emergency_contacts[0]
            message = self.client.messages.create(
                body=test_message,
                from_=self.whatsapp_from,
                to=contact
            )
            
            return True, f"Test message sent successfully. SID: {message.sid}"
            
        except Exception as e:
            return False, f"Test failed: {str(e)}"

# Global instance
twilio_notifier = TwilioWhatsAppNotifier()

def send_whatsapp_emergency_alert(emergency_data, emergency_id=None):
    """Send WhatsApp emergency alert - called by notifications.py"""
    return twilio_notifier.send_whatsapp_alert(emergency_data, emergency_id)

def test_whatsapp_integration():
    """Test WhatsApp integration - for debugging"""
    return twilio_notifier.test_whatsapp_connection()