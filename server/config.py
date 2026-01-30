"""
AlertAI Server Configuration
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file in server directory (as fallback)
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))

class AlertAIServerConfig:
    """Configuration settings for AlertAI Server"""
    
    # Flask Configuration
    FLASK_ENV = os.getenv("FLASK_ENV", "development")
    FLASK_DEBUG = os.getenv("FLASK_DEBUG", "true").lower() == "true"
    SERVER_HOST = os.getenv("SERVER_HOST", "0.0.0.0")
    SERVER_PORT = int(os.getenv("SERVER_PORT", "5000"))
    
    # Gemini API Configuration - prioritize environment variables over .env file
    GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY", "")
    
    # Database Configuration
    DATABASE_PATH = os.getenv("DATABASE_PATH", "db/database.db")
    
    # Emergency Settings
    PROXIMITY_THRESHOLD_METERS = int(os.getenv("PROXIMITY_THRESHOLD_METERS", "100"))
    EMERGENCY_ALERT_TIMEOUT_HOURS = float(os.getenv("EMERGENCY_ALERT_TIMEOUT_HOURS", "2"))
    
    # Notification Settings
    FCM_SERVER_KEY = os.getenv("FCM_SERVER_KEY", "")
    
    # Twilio WhatsApp Configuration - prioritize environment variables
    TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID") or os.getenv("TWILIO_ACCOUNT_SID", "")
    TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN") or os.getenv("TWILIO_AUTH_TOKEN", "")
    TWILIO_WHATSAPP_FROM = os.environ.get("TWILIO_WHATSAPP_FROM") or os.getenv("TWILIO_WHATSAPP_FROM", "whatsapp:+14155238886")
    
    # Emergency WhatsApp Contacts
    EMERGENCY_CONTACT_1 = os.environ.get("EMERGENCY_CONTACT_1") or os.getenv("EMERGENCY_CONTACT_1", "")
    EMERGENCY_CONTACT_2 = os.environ.get("EMERGENCY_CONTACT_2") or os.getenv("EMERGENCY_CONTACT_2", "")
    EMERGENCY_CONTACT_3 = os.environ.get("EMERGENCY_CONTACT_3") or os.getenv("EMERGENCY_CONTACT_3", "")
    
    # Emergency Contacts
    EMERGENCY_CONTACTS = {
        "fire": os.getenv("EMERGENCY_CONTACTS_FIRE", "911"),
        "medical": os.getenv("EMERGENCY_CONTACTS_MEDICAL", "911"),
        "security": os.getenv("EMERGENCY_CONTACTS_SECURITY", "+234-800-SECURITY")
    }

# Create global config instance
config = AlertAIServerConfig()

# Validate critical settings with better debugging
if not config.GEMINI_API_KEY:
    print("⚠️ WARNING: GEMINI_API_KEY not found in environment variables")
    print("Please set GEMINI_API_KEY in Railway environment variables")
    print(f"Environment check: os.environ.get('GEMINI_API_KEY') = {bool(os.environ.get('GEMINI_API_KEY'))}")
    print(f"Dotenv check: os.getenv('GEMINI_API_KEY') = {bool(os.getenv('GEMINI_API_KEY'))}")
else:
    print(f"✅ Server configuration loaded - API key configured")
    print(f"🔑 Using API key from: {'Railway env vars' if os.environ.get('GEMINI_API_KEY') else '.env file'}")
    print(f"🔑 API key starts with: {config.GEMINI_API_KEY[:10]}...")