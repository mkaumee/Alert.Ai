#!/usr/bin/env python3
"""
Configure AlertAI for ngrok deployment
Sets up environment variables and provides usage instructions
"""
import os
import sys

def configure_for_ngrok(ngrok_url):
    """Configure AlertAI to use ngrok URL"""
    
    # Validate URL
    if not ngrok_url.startswith('https://'):
        print("❌ Error: ngrok URL must start with https://")
        return False
    
    if not ngrok_url.endswith('.ngrok.io') and not ngrok_url.endswith('.ngrok-free.dev'):
        print("❌ Error: URL doesn't look like a valid ngrok URL")
        return False
    
    print("🔧 CONFIGURING ALERTAI FOR NGROK")
    print("=" * 50)
    print(f"🌐 ngrok URL: {ngrok_url}")
    
    # Set environment variable for current session
    os.environ['ALERTAI_SERVER_URL'] = ngrok_url
    
    # Create a .env file for persistence
    env_content = f"""# AlertAI Configuration
ALERTAI_SERVER_URL={ngrok_url}

# Gemini API Configuration (if needed)
# GEMINI_API_KEY=your_api_key_here
"""
    
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print("✅ Configuration saved to .env file")
    print("✅ Environment variable set for current session")
    
    print("\n📋 USAGE INSTRUCTIONS:")
    print("=" * 30)
    
    print("\n1. Start the combined server:")
    print("   python combined_server.py")
    
    print("\n2. Start ngrok (in another terminal):")
    print("   ngrok http 8000")
    
    print("\n3. Run YOLO fire detection:")
    print(f"   python yolo_fire_detection.py {ngrok_url}")
    print("   OR")
    print("   python yolo_fire_detection.py  # (uses .env file)")
    
    print("\n4. Test with fire image:")
    print(f"   python test_with_fire_image.py {ngrok_url}")
    print("   OR")
    print("   python test_with_fire_image.py  # (uses .env file)")
    
    print("\n5. Access web app:")
    print(f"   {ngrok_url}")
    
    print("\n🔍 VERIFICATION:")
    print("=" * 20)
    print(f"Health check: {ngrok_url}/health")
    print(f"Emergency API: {ngrok_url}/emergency")
    print(f"Web app: {ngrok_url}/")
    
    return True

def load_from_env():
    """Load configuration from .env file"""
    try:
        with open('.env', 'r') as f:
            for line in f:
                if line.startswith('ALERTAI_SERVER_URL='):
                    url = line.split('=', 1)[1].strip()
                    return url
    except FileNotFoundError:
        pass
    return None

def main():
    """Main configuration function"""
    print("🔧 ALERTAI NGROK CONFIGURATOR")
    print("=" * 40)
    
    if len(sys.argv) > 1:
        ngrok_url = sys.argv[1].rstrip('/')  # Remove trailing slash
        configure_for_ngrok(ngrok_url)
    else:
        # Check if already configured
        existing_url = load_from_env()
        if existing_url:
            print(f"✅ Already configured for: {existing_url}")
            print("\nTo reconfigure, run:")
            print("python configure_ngrok.py https://your-new-ngrok-url.ngrok.io")
        else:
            print("❌ No ngrok URL provided")
            print("\nUsage:")
            print("python configure_ngrok.py https://your-ngrok-url.ngrok.io")
            print("\nExample:")
            print("python configure_ngrok.py https://macrocytic-overconscientiously-josue.ngrok-free.dev")

if __name__ == "__main__":
    main()