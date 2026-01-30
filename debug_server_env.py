#!/usr/bin/env python3
"""
Debug script to check exactly what environment the server sees when it starts
"""
import os
import sys
from dotenv import load_dotenv, dotenv_values

def debug_server_environment():
    """Debug what environment variables the server sees"""
    print("🔍 DEBUGGING SERVER ENVIRONMENT LOADING")
    print("=" * 70)
    
    # Check current working directory
    print(f"📁 Current working directory: {os.getcwd()}")
    
    # Check system environment BEFORE loading any .env files
    system_gemini_key = os.environ.get('GEMINI_API_KEY', 'NOT_SET')
    print(f"🌐 System GEMINI_API_KEY: {system_gemini_key[:20]}..." if system_gemini_key != 'NOT_SET' else "🌐 System GEMINI_API_KEY: NOT_SET")
    
    # Check all possible .env file locations
    env_files_to_check = [
        '.env',
        'server/.env', 
        'alertai-agent/.env',
        os.path.expanduser('~/.env')
    ]
    
    print("\n📋 Checking .env files:")
    for env_file in env_files_to_check:
        if os.path.exists(env_file):
            env_values = dotenv_values(env_file)
            gemini_key = env_values.get('GEMINI_API_KEY', 'NOT_FOUND')
            print(f"✅ {env_file}: {gemini_key[:20]}..." if gemini_key != 'NOT_FOUND' else f"❌ {env_file}: NO GEMINI_API_KEY")
        else:
            print(f"❌ {env_file}: FILE NOT FOUND")
    
    # Test loading server/.env (like combined_server.py does)
    print(f"\n🔧 Testing server/.env loading (like combined_server.py):")
    load_dotenv(os.path.join('server', '.env'))
    after_server_env = os.getenv('GEMINI_API_KEY', 'NOT_FOUND')
    print(f"After loading server/.env: {after_server_env[:20]}...")
    
    # Simulate what happens when server imports agents
    print(f"\n🤖 Simulating server agent import process:")
    
    # Add alertai-agent to path
    agent_path = os.path.join(os.getcwd(), 'alertai-agent')
    if agent_path not in sys.path:
        sys.path.insert(0, agent_path)
    
    # Change to alertai-agent directory
    original_cwd = os.getcwd()
    try:
        os.chdir('alertai-agent')
        print(f"📁 Changed to: {os.getcwd()}")
        
        # Check what the config sees
        print("🔧 Importing config...")
        
        # Clear any cached config first
        if 'config' in sys.modules:
            del sys.modules['config']
        
        from config import config
        print(f"Config AI_API_KEY: {config.AI_API_KEY[:20]}...")
        
        # Check what environment the config loaded
        env_path = os.path.join(os.path.dirname(__file__), 'alertai-agent', '.env')
        print(f"Config .env path: {env_path}")
        
    finally:
        os.chdir(original_cwd)
    
    # Final diagnosis
    print(f"\n🎯 DIAGNOSIS:")
    print(f"System env: {system_gemini_key[:20]}...")
    print(f"Server env: {after_server_env[:20]}...")
    print(f"Agent config: {config.AI_API_KEY[:20]}...")
    
    if system_gemini_key != 'NOT_SET' and system_gemini_key != config.AI_API_KEY:
        print("⚠️  ISSUE: System environment variable is overriding .env file!")
        print("💡 SOLUTION: Unset the system GEMINI_API_KEY variable")
        print("   Windows: set GEMINI_API_KEY=")
        print("   Linux/Mac: unset GEMINI_API_KEY")

if __name__ == "__main__":
    debug_server_environment()