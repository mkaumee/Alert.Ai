"""
AlertAI Agent Configuration
"""
import os
from dotenv import load_dotenv, dotenv_values

# Load environment variables from .env file in agent directory (as fallback)
env_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path=env_path)

# Get values from .env file as fallback only
env_values = dotenv_values(env_path)

class AlertAIAgentConfig:
    """Configuration settings for AlertAI AI Agent"""
    
    # Server URLs - ONLY use Railway environment variables
    ALERTAI_SERVER_URL = os.environ.get("ALERTAI_SERVER_URL", "http://localhost:5000")
    ALERTAI_WEBAPP_URL = os.environ.get("ALERTAI_WEBAPP_URL", "http://localhost:3000")
    
    # Agent Settings
    AGENT_NAME = "AlertAI Assistant"
    AGENT_VERSION = "1.0.0"
    
    # AI Model Configuration - ONLY use Railway environment variables
    AI_MODEL = "models/gemini-3-flash-preview"
    AI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
    GEMINI_API_KEY = AI_API_KEY  # Alias for backward compatibility
    
    # Response Settings
    MAX_RESPONSE_LENGTH = 500
    RESPONSE_TIMEOUT = 30
    
    # Emergency Types
    SUPPORTED_EMERGENCY_TYPES = [
        "Fire",
        "Accident", 
        "Smoke",
        "Fallen Person",
        "Gun",
        "Blood"
    ]
    
    # Agent Capabilities
    CAPABILITIES = [
        "Emergency response guidance",
        "Real-time alert analysis", 
        "User support and assistance",
        "System status monitoring",
        "Emergency protocol advice"
    ]
    
    # Database
    DATABASE_PATH = os.environ.get("DATABASE_PATH", "../server/db/database.db")
    
    # Emergency Settings
    PROXIMITY_THRESHOLD_METERS = int(os.environ.get("PROXIMITY_THRESHOLD_METERS", "100"))
    EMERGENCY_ALERT_TIMEOUT_HOURS = float(os.environ.get("EMERGENCY_ALERT_TIMEOUT_HOURS", "2"))
    
    # Logging
    LOG_LEVEL = "INFO"
    LOG_FILE = "alertai-agent.log"

# Create global config instance
config = AlertAIAgentConfig()

# Validate critical settings with Railway-only debugging
if not config.AI_API_KEY:
    print("⚠️ WARNING: GEMINI_API_KEY not found in Railway environment variables")
    print("Please set GEMINI_API_KEY in Railway dashboard")
    print(f"Railway env check: os.environ.get('GEMINI_API_KEY') = {bool(os.environ.get('GEMINI_API_KEY'))}")
else:
    print(f"✅ Agent configuration loaded - API key from Railway")
    print(f"🔑 API Key loaded: {config.AI_API_KEY[:20]}...")
    print(f"📁 .env file path: {env_path} (IGNORED - using Railway only)")