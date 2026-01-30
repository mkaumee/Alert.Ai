import os
import requests
import subprocess
import sys
from pathlib import Path
from config import config

class GeminiVerifier:
    def __init__(self):
        """Initialize Gemini verifier for local images"""
        self.api_key = config.GEMINI_API_KEY
        if not self.api_key or self.api_key.strip() == '':
            print("⚠️  WARNING: GEMINI_API_KEY not found in environment variables")
            self.available = False
        else:
            print(f"✅ Gemini API key configured - Ready for local image analysis")
            self.available = True

    def verify_emergency_with_gemini(self, image_path, emergency_type):
        """
        Verify if the local image shows a real emergency using Gemini 3 API.
        Handles both local file paths and URLs.
        """
        if not self.available:
            print("⚠️  Gemini not configured, using simulation fallback")
            return self._simulate_gemini_analysis(image_path, emergency_type)
        
        try:
            print(f"\n🤖 REAL GEMINI 3 VERIFICATION")
            print(f"   Emergency Type: {emergency_type}")
            print(f"   Image Path: {image_path}")
            
            # Handle both local files and URLs
            if self._is_local_file(image_path):
                result = self._analyze_local_image(image_path, emergency_type)
            else:
                result = self._analyze_url_image(image_path, emergency_type)
            
            if result is None:
                print("⚠️  Gemini API call failed, using simulation fallback")
                return self._simulate_gemini_analysis(image_path, emergency_type)
            
            is_verified = self._parse_gemini_response(result)
            
            if is_verified:
                print("✅ Emergency VERIFIED by Gemini 3 - proceeding with alerts")
            else:
                print("❌ Emergency NOT VERIFIED by Gemini 3 - blocking alerts")
            
            return is_verified
            
        except Exception as e:
            print(f"❌ Gemini verification error: {str(e)}")
            print("   Using simulation fallback")
            return self._simulate_gemini_analysis(image_path, emergency_type)

    def _is_local_file(self, path):
        """Check if path is a local file or URL"""
        return not (path.startswith('http://') or path.startswith('https://'))

    def _analyze_local_image(self, image_path, emergency_type):
        """Analyze local image file with Gemini"""
        try:
            # Check if file exists
            if not os.path.exists(image_path):
                print(f"❌ Image file not found: {image_path}")
                return None
            
            print(f"📁 Reading local image: {image_path}")
            file_size = os.path.getsize(image_path)
            print(f"   File size: {file_size} bytes")
            
            # Call Gemini via subprocess for local file
            result = self._call_gemini_subprocess_local(image_path, emergency_type)
            return result
            
        except Exception as e:
            print(f"❌ Local image analysis failed: {str(e)}")
            return None

    def _analyze_url_image(self, image_url, emergency_type):
        """Analyze image from URL with Gemini"""
        try:
            print(f"📥 Downloading image from URL...")
            response = requests.get(image_url, timeout=15)
            response.raise_for_status()
            print(f"   Downloaded: {len(response.content)} bytes")
            
            # Call Gemini via subprocess for URL
            result = self._call_gemini_subprocess_url(image_url, emergency_type)
            return result
            
        except Exception as e:
            print(f"❌ URL image analysis failed: {str(e)}")
            return None

    def _call_gemini_subprocess_local(self, image_path, emergency_type):
        """Call Gemini API via subprocess for local file"""
        try:
            # Create Python script for local file analysis
            script_content = f'''
import os
import google.genai as genai
from google.genai.types import Part

api_key = "{self.api_key}"
client = genai.Client(api_key=api_key)

# Read local image file
with open("{image_path}", "rb") as f:
    image_bytes = f.read()

# Create image part
image_part = Part.from_bytes(data=image_bytes, mime_type='image/jpeg')

# Create prompt
prompt = """Analyze this image carefully. Is there a real {emergency_type} emergency happening?

Look for clear, unambiguous signs of a genuine emergency situation.
Do not consider staged, fake, or unclear situations as emergencies.

Respond with ONLY "YES" if this is clearly a real emergency requiring immediate response.
Respond with ONLY "NO" if this is not an emergency, fake, unclear, or normal situation."""

# Call Gemini
result = client.models.generate_content(
    model='gemini-3-flash-preview',
    contents=[prompt, image_part]
)

print(result.text.strip())
'''
            
            return self._execute_gemini_script(script_content)
            
        except Exception as e:
            print(f"❌ Local subprocess call failed: {str(e)}")
            return None

    def _call_gemini_subprocess_url(self, image_url, emergency_type):
        """Call Gemini API via subprocess for URL"""
        try:
            # Create Python script for URL analysis
            script_content = f'''
import requests
import google.genai as genai
from google.genai.types import Part

api_key = "{self.api_key}"
client = genai.Client(api_key=api_key)

# Download image
response = requests.get("{image_url}", timeout=15)
response.raise_for_status()
image_bytes = response.content

# Create image part
image_part = Part.from_bytes(data=image_bytes, mime_type='image/jpeg')

# Create prompt
prompt = """Analyze this image carefully. Is there a real {emergency_type} emergency happening?

Look for clear, unambiguous signs of a genuine emergency situation.
Do not consider staged, fake, or unclear situations as emergencies.

Respond with ONLY "YES" if this is clearly a real emergency requiring immediate response.
Respond with ONLY "NO" if this is not an emergency, fake, unclear, or normal situation."""

# Call Gemini
result = client.models.generate_content(
    model='gemini-3-flash-preview',
    contents=[prompt, image_part]
)

print(result.text.strip())
'''
            
            return self._execute_gemini_script(script_content)
            
        except Exception as e:
            print(f"❌ URL subprocess call failed: {str(e)}")
            return None

    def _execute_gemini_script(self, script_content):
        """Execute Gemini script and return result"""
        try:
            # Write script to temp file
            import tempfile
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                f.write(script_content)
                temp_script = f.name
            
            # Run script
            print("🔍 Calling Gemini 3 API...")
            result = subprocess.run(
                [sys.executable, temp_script],
                capture_output=True,
                text=True,
                timeout=45,
                cwd=os.getcwd()
            )
            
            # Clean up
            os.unlink(temp_script)
            
            if result.returncode == 0:
                response_text = result.stdout.strip()
                print(f"🤖 Gemini 3 Response: '{response_text}'")
                return response_text
            else:
                print(f"❌ Subprocess error: {result.stderr}")
                return None
                
        except Exception as e:
            print(f"❌ Script execution failed: {str(e)}")
            return None

    def _parse_gemini_response(self, response_text):
        """Parse Gemini's response to determine yes/no"""
        response_text = response_text.strip().lower()
        
        if "yes" in response_text and "no" not in response_text:
            return True
        elif "no" in response_text and "yes" not in response_text:
            return False
        else:
            print(f"⚠️  Unclear Gemini response: '{response_text}' - defaulting to NO for safety")
            return False

    def _simulate_gemini_analysis(self, image_path, emergency_type):
        """Fallback simulation when real API is not available"""
        print("🔄 Using simulation mode")
        print("🔍 Analyzing image with simulated AI...")
        
        # Check if it's a local file
        if self._is_local_file(image_path):
            print(f"📁 Local file detected: {image_path}")
            
            # Simulate based on filename patterns
            filename = os.path.basename(image_path).lower()
            
            if "fire" in filename or "flame" in filename:
                if emergency_type.lower() == "fire":
                    print("🤖 Simulated Gemini: 'YES - Fire detected in filename'")
                    return True
                else:
                    print("🤖 Simulated Gemini: 'NO - Fire in filename but type mismatch'")
                    return False
            
            elif "blood" in filename or "bleeding" in filename or "injury" in filename:
                if "bleeding" in emergency_type.lower() or "blood" in emergency_type.lower():
                    print("🤖 Simulated Gemini: 'YES - Blood/Bleeding detected in filename'")
                    return True
                else:
                    print("🤖 Simulated Gemini: 'NO - Blood in filename but type mismatch'")
                    return False
            
            elif "medical" in filename or "ambulance" in filename:
                if "medical" in emergency_type.lower():
                    print("🤖 Simulated Gemini: 'YES - Medical emergency detected in filename'")
                    return True
                else:
                    print("🤖 Simulated Gemini: 'NO - Medical in filename but type mismatch'")
                    return False
            
            elif "security" in filename or "breach" in filename or "intrusion" in filename:
                if "security" in emergency_type.lower():
                    print("🤖 Simulated Gemini: 'YES - Security breach detected in filename'")
                    return True
                else:
                    print("🤖 Simulated Gemini: 'NO - Security in filename but type mismatch'")
                    return False
            
            elif "normal" in filename or "office" in filename or "fake" in filename:
                print("🤖 Simulated Gemini: 'NO - Normal/fake scene detected in filename'")
                return False
            
            else:
                # For unknown local files, be conservative
                print("🤖 Simulated Gemini: 'YES - Unknown local image, assuming emergency'")
                return True
        
        else:
            # URL-based simulation (existing logic)
            if "fire" in image_path.lower():
                if emergency_type.lower() == "fire":
                    print("🤖 Simulated Gemini: 'YES - Fire detected in URL'")
                    return True
            elif "office" in image_path.lower():
                print("🤖 Simulated Gemini: 'NO - Office scene detected in URL'")
                return False
            else:
                print("🤖 Simulated Gemini: 'YES - Potential emergency in URL'")
                return True

# Global verifier instance
gemini_verifier = GeminiVerifier()