#!/usr/bin/env python3
"""
AlertAI Web App Server
Serves the AlertAI web application on a local HTTP server
"""
import http.server
import socketserver
import webbrowser
import os
import sys
from threading import Timer

class AlertAIHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """Custom HTTP request handler for AlertAI web app"""
    
    def end_headers(self):
        # Add CORS headers to allow communication with Flask server
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        super().end_headers()
    
    def do_OPTIONS(self):
        # Handle preflight requests
        self.send_response(200)
        self.end_headers()
    
    def do_GET(self):
        # Redirect root to alertai.html
        if self.path == '/':
            self.path = '/alertai.html'
        return super().do_GET()
    
    def log_message(self, format, *args):
        # Custom logging format
        print(f"📱 Web App: {format % args}")

def open_browser():
    """Open the web app in browser after a short delay"""
    webbrowser.open('http://localhost:3000')

def start_webapp_server():
    """Start the AlertAI web app server"""
    PORT = 3000
    
    print("🌐 STARTING ALERTAI WEB APP SERVER")
    print("=" * 50)
    
    # Change to webapp directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    try:
        # Create server
        with socketserver.TCPServer(("", PORT), AlertAIHTTPRequestHandler) as httpd:
            print(f"✅ AlertAI Web App Server started!")
            print(f"🌐 URL: http://localhost:{PORT}")
            print(f"📱 Opening in browser...")
            print(f"🔗 Flask Server: http://localhost:5000")
            print("=" * 50)
            print("📝 INSTRUCTIONS:")
            print("1. Register as a user in the web app")
            print("2. Enable location access when prompted")
            print("3. Run: python send_blood_emergency.py (to test alerts)")
            print("4. Press Ctrl+C to stop the server")
            print("=" * 50)
            
            # Open browser after 2 seconds
            Timer(2.0, open_browser).start()
            
            # Start serving
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n🛑 AlertAI Web App Server stopped")
    except OSError as e:
        if "Address already in use" in str(e):
            print(f"❌ Port {PORT} is already in use!")
            print("Try stopping other servers or use a different port")
        else:
            print(f"❌ Server error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    start_webapp_server()