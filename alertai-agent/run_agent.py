#!/usr/bin/env python3
"""
Run AlertAI Emergency Response Agent - Live Gemini Version
"""
import sys
import os

def check_dependencies():
    """Check if required packages are installed"""
    required_packages = [
        'google.genai',
        'requests'
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing.append(package)
    
    if missing:
        print("❌ Missing required packages:")
        for pkg in missing:
            print(f"   - {pkg}")
        print("\nInstall with: pip install -r requirements.txt")
        return False
    
    return True

def main():
    print("🤖 ALERTAI EMERGENCY RESPONSE AGENT - LIVE GEMINI")
    print("=" * 60)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Import and run agent
    try:
        from live_gemini_agent import LiveAlertAIAgent
        
        print("✅ Starting AlertAI Live Emergency Assistant...")
        print("🔄 Powered by Live Gemini model")
        print("📡 Real-time server monitoring")
        print("🏢 Dynamic building data integration")
        print("🧠 Context-aware emergency guidance")
        print("=" * 60)
        
        agent = LiveAlertAIAgent()
        agent.start_monitoring()
        
    except KeyboardInterrupt:
        print("\n👋 AlertAI Agent stopped by user")
    except Exception as e:
        print(f"❌ Error running agent: {e}")

if __name__ == "__main__":
    main()