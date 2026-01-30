#!/usr/bin/env python3
"""
Launch Terminal Guidance Agent
Quick script to launch terminal guidance agents for debugging
"""
import sys
import subprocess
import os

def launch_agent(emergency_type):
    """Launch the appropriate terminal agent"""
    
    # Map emergency types to agent scripts
    agent_scripts = {
        'fire': 'alertai-agent/fire_emergency_agent.py',
        'smoke': 'alertai-agent/smoke_emergency_agent.py',
        'fallen': 'alertai-agent/fallen_person_agent.py',
        'gun': 'alertai-agent/gun_emergency_agent.py',
        'blood': 'alertai-agent/blood_emergency_agent.py'
    }
    
    emergency_lower = emergency_type.lower()
    script_path = agent_scripts.get(emergency_lower)
    
    if not script_path:
        print(f"❌ Unknown emergency type: {emergency_type}")
        print(f"Available types: {', '.join(agent_scripts.keys())}")
        return False
    
    if not os.path.exists(script_path):
        print(f"❌ Agent script not found: {script_path}")
        return False
    
    print(f"🤖 Launching {emergency_type.title()} Emergency Agent...")
    print(f"📂 Script: {script_path}")
    
    try:
        # For Windows - open new command prompt
        if sys.platform == "win32":
            cmd = f'start "AlertAI {emergency_type.title()} Agent - Terminal Debug" cmd /k "python {script_path}"'
            subprocess.Popen(cmd, shell=True)
            print("✅ Terminal agent launched in new window")
        else:
            # For Linux/Mac
            try:
                subprocess.Popen(['gnome-terminal', '--', 'python3', script_path])
                print("✅ Terminal agent launched in gnome-terminal")
            except FileNotFoundError:
                try:
                    subprocess.Popen(['xterm', '-e', f'python3 {script_path}'])
                    print("✅ Terminal agent launched in xterm")
                except FileNotFoundError:
                    # Fallback - run in current terminal
                    print("⚠️ No terminal emulator found, running in current terminal...")
                    subprocess.run([sys.executable, script_path])
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to launch agent: {e}")
        return False

def main():
    """Main function"""
    print("🖥️ ALERTAI TERMINAL AGENT LAUNCHER")
    print("=" * 50)
    
    if len(sys.argv) > 1:
        emergency_type = sys.argv[1]
        launch_agent(emergency_type)
    else:
        print("📋 Available emergency agents:")
        print("  • fire - Fire Emergency Agent")
        print("  • smoke - Smoke Emergency Agent") 
        print("  • fallen - Fallen Person Agent")
        print("  • gun - Gun Emergency Agent")
        print("  • blood - Blood Emergency Agent")
        
        print("\n💡 Usage:")
        print("  python launch_terminal_agent.py fire")
        print("  python launch_terminal_agent.py blood")
        
        print("\n🎯 This script opens the agent in a new terminal window")
        print("   so you can see the conversation and debug issues.")
        
        # Interactive mode
        while True:
            try:
                choice = input("\nEnter emergency type (or 'quit'): ").strip().lower()
                if choice in ['quit', 'exit', 'q']:
                    break
                elif choice:
                    if launch_agent(choice):
                        print("🎉 Agent launched! Check the new terminal window.")
                    else:
                        print("❌ Failed to launch agent.")
                else:
                    print("❌ Please enter an emergency type.")
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break

if __name__ == "__main__":
    main()