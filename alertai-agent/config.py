"""
AlertAI Agent Configuration
"""
import os
from dotenv import load_dotenv, dotenv_values

# Load environment variables from .env file in agent directory
env_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path=env_path)

# Get values from .env file directly (prioritize .env over system env)
env_values = dotenv_values(env_path)

class AlertAIAgentConfig:
    """Configuration settings for AlertAI AI Agent"""
    
    # Server URLs
    ALERTAI_SERVER_URL = env_values.get("ALERTAI_SERVER_URL") or os.getenv("ALERTAI_SERVER_URL", "http://localhost:5000")
    ALERTAI_WEBAPP_URL = env_values.get("ALERTAI_WEBAPP_URL") or os.getenv("ALERTAI_WEBAPP_URL", "http://localhost:3000")
    
    # Agent Settings
    AGENT_NAME = "AlertAI Assistant"
    AGENT_VERSION = "1.0.0"
    
    # AI Model Configuration - prioritize .env file over system environment
    AI_MODEL = "gemini-3-flash-preview"
    AI_API_KEY = env_values.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY", "")
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
    DATABASE_PATH = env_values.get("DATABASE_PATH") or os.getenv("DATABASE_PATH", "../server/db/database.db")
    
    # Emergency Settings
    PROXIMITY_THRESHOLD_METERS = int(env_values.get("PROXIMITY_THRESHOLD_METERS") or os.getenv("PROXIMITY_THRESHOLD_METERS", "100"))
    EMERGENCY_ALERT_TIMEOUT_HOURS = float(env_values.get("EMERGENCY_ALERT_TIMEOUT_HOURS") or os.getenv("EMERGENCY_ALERT_TIMEOUT_HOURS", "2"))
    
    # Logging
    LOG_LEVEL = "INFO"
    LOG_FILE = "alertai-agent.log"

# Create global config instance
config = AlertAIAgentConfig()

# Validate critical settings
if not config.AI_API_KEY:
    print("⚠️ WARNING: GEMINI_API_KEY not found in .env file or environment variables")
    print("Please set GEMINI_API_KEY in your alertai-agent/.env file")
else:
    print(f"✅ Configuration loaded - API key from .env file: {config.AI_API_KEY[:20]}...")
    print(f"📁 Using .env file: {env_path}")