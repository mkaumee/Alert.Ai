"""
AlertAI Server Configuration
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file in server directory
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))

class AlertAIServerConfig:
    """Configuration settings for AlertAI Server"""
    
    # Flask Configuration
    FLASK_ENV = os.getenv("FLASK_ENV", "development")
    FLASK_DEBUG = os.getenv("FLASK_DEBUG", "true").lower() == "true"
    SERVER_HOST = os.getenv("SERVER_HOST", "0.0.0.0")
    SERVER_PORT = int(os.getenv("SERVER_PORT", "5000"))
    
    # Gemini API Configuration
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    
    # Database Configuration
    DATABASE_PATH = os.getenv("DATABASE_PATH", "db/database.db")
    
    # Emergency Settings
    PROXIMITY_THRESHOLD_METERS = int(os.getenv("PROXIMITY_THRESHOLD_METERS", "100"))
    EMERGENCY_ALERT_TIMEOUT_HOURS = float(os.getenv("EMERGENCY_ALERT_TIMEOUT_HOURS", "2"))
    
    # Notification Settings
    FCM_SERVER_KEY = os.getenv("FCM_SERVER_KEY", "")
    
    # Twilio WhatsApp Configuration
    TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID", "")
    TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", "")
    TWILIO_WHATSAPP_FROM = os.getenv("TWILIO_WHATSAPP_FROM", "whatsapp:+14155238886")  # Twilio Sandbox
    
    # Emergency WhatsApp Contacts (comma-separated)
    EMERGENCY_CONTACT_1 = os.getenv("EMERGENCY_CONTACT_1", "")
    EMERGENCY_CONTACT_2 = os.getenv("EMERGENCY_CONTACT_2", "")
    EMERGENCY_CONTACT_3 = os.getenv("EMERGENCY_CONTACT_3", "")
    
    # Emergency Contacts
    EMERGENCY_CONTACTS = {
        "fire": os.getenv("EMERGENCY_CONTACTS_FIRE", "911"),
        "medical": os.getenv("EMERGENCY_CONTACTS_MEDICAL", "911"),
        "security": os.getenv("EMERGENCY_CONTACTS_SECURITY", "+234-800-SECURITY")
    }

# Create global config instance
config = AlertAIServerConfig()

# Validate critical settings
if not config.GEMINI_API_KEY:
    print("⚠️ WARNING: GEMINI_API_KEY not found in environment variables")
    print("Please set GEMINI_API_KEY in your .env file")
else:
    print(f"✅ Server configuration loaded - API key configured")