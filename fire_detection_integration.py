#!/usr/bin/env python3
"""
Fire Detection Model Integration with AlertAI Server
Monitors fire detection model and sends emergency alerts when fire is confirmed
"""
import os
import sys
import time
import json
import requests
import shutil
from datetime import datetime
from pathlib import Path
import threading
import queue

class FireDetectionIntegration:
    def __init__(self, server_url=None):
        # Allow server URL to be configured
        if server_url:
            self.alertai_server_url = server_url
        else:
            # Check environment variable first, then default to localhost
            self.alertai_server_url = os.environ.get('ALERTAI_SERVER_URL', 'http://localhost:8000')
        
        self.fire_dataset_folder = "fire_dataset"  # Your model's folder
        self.confidence_threshold = 0.80  # 80% confidence
        self.confirmation_duration = 5.0  # 5 seconds
        self.building_name = "Medical Center Building A"
        self.floor_affected = "1st Floor"
        
        # Detection state
        self.fire_detected_start = None
        self.last_fire_confidence = 0.0
        self.last_detection_image = None
        self.emergency_sent = False
        self.last_emergency_time = 0  # Track when last emergency was sent
        self.emergency_cooldown = 300  # 5 minutes cooldown between alerts
        self.monitoring = False
        
        # Image monitoring
        self.image_queue = queue.Queue()
        self.latest_image_path = None
        
        print("🔥 Fire Detection Integration initialized")
        print(f"📡 AlertAI Server: {self.alertai_server_url}")
        print(f"📁 Monitoring folder: {self.fire_dataset_folder}")
        print(f"🎯 Confidence threshold: {self.confidence_threshold * 100}%")
        print(f"⏱️  Confirmation duration: {self.confirmation_duration} seconds")
        print(f"🏢 Building: {self.building_name}")
        print(f"🏠 Floor: {self.floor_affected}")
    
    def check_server_connection(self):
        """Check if AlertAI server is running"""
        try:
            response = requests.get(f"{self.alertai_server_url}/health", timeout=5)
            if response.status_code == 200:
                print("✅ AlertAI server is running and healthy")
                return True
            else:
                print(f"❌ AlertAI server responded with status: {response.status_code}")
                return False
        except requests.exceptions.ConnectionError:
            print("❌ Cannot connect to AlertAI server - is it running?")
            print(f"   Please start the server: python server/app.py")
            return False
        except Exception as e:
            print(f"❌ Error checking server: {e}")
            return False
    
    def setup_monitoring_folder(self):
        """Setup the fire dataset folder for monitoring"""
        if not os.path.exists(self.fire_dataset_folder):
            os.makedirs(self.fire_dataset_folder)
            print(f"📁 Created monitoring folder: {self.fire_dataset_folder}")
        
        # Create subfolders for organization
        subfolders = ["detections", "confirmed_fires", "false_alarms"]
        for subfolder in subfolders:
            folder_path = os.path.join(self.fire_dataset_folder, subfolder)
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
        
        print(f"📂 Monitoring folder structure ready")
    
    def monitor_model_output(self):
        """
        Monitor your fire detection model output
        This function should be adapted to your specific model's output format
        """
        print("🔍 Starting fire detection monitoring...")
        print("📝 Waiting for fire detection model output...")
        
        # This is a template - adapt to your model's actual output
        # Your model should call: self.process_detection(confidence, image_path)
        
        while self.monitoring:
            try:
                # EXAMPLE: Reading from a results file (adapt to your model)
                results_file = os.path.join(self.fire_dataset_folder, "detection_results.json")
                
                if os.path.exists(results_file):
                    with open(results_file, 'r') as f:
                        try:
                            results = json.load(f)
                            confidence = results.get('fire_confidence', 0.0)
                            image_path = results.get('image_path', '')
                            timestamp = results.get('timestamp', '')
                            
                            # Process the detection
                            self.process_detection(confidence, image_path)
                            
                            # Remove processed file
                            os.remove(results_file)
                            
                        except json.JSONDecodeError:
                            pass  # Invalid JSON, skip
                
                # Check for new images in the folder
                self.check_for_new_images()
                
                time.sleep(0.1)  # Check every 100ms
                
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"❌ Error in monitoring: {e}")
                time.sleep(1)
    
    def check_for_new_images(self):
        """Check for new images in the fire dataset folder"""
        try:
            # Look for common image extensions
            image_extensions = ['.jpg', '.jpeg', '.png', '.bmp']
            
            for ext in image_extensions:
                pattern = f"*{ext}"
                images = list(Path(self.fire_dataset_folder).glob(pattern))
                
                if images:
                    # Get the most recent image
                    latest_image = max(images, key=os.path.getctime)
                    
                    if str(latest_image) != self.latest_image_path:
                        self.latest_image_path = str(latest_image)
                        print(f"📸 New image detected: {latest_image.name}")
                        
                        # Move to detections folder for organization
                        detection_path = os.path.join(self.fire_dataset_folder, "detections", latest_image.name)
                        shutil.move(str(latest_image), detection_path)
                        self.latest_image_path = detection_path
                        
        except Exception as e:
            print(f"❌ Error checking for images: {e}")
    
    def process_detection(self, confidence, image_path=""):
        """Process a fire detection result from your model"""
        current_time = time.time()
        
        print(f"🔥 Fire detection: {confidence:.2%} confidence (threshold: {self.confidence_threshold:.2%})")
        
        if confidence >= self.confidence_threshold:
            # High confidence fire detected
            if self.fire_detected_start is None:
                # Start of high confidence detection
                self.fire_detected_start = current_time
                print(f"🚨 Fire detected above threshold! Starting {self.confirmation_duration}s confirmation...")
                print(f"📊 Detection details:")
                print(f"   Confidence: {confidence:.2%}")
                print(f"   Threshold: {self.confidence_threshold:.2%}")
                print(f"   Image: {image_path if image_path else 'None'}")
            
            # Update detection info
            self.last_fire_confidence = confidence
            if image_path and os.path.exists(image_path):
                self.last_detection_image = image_path
            elif self.latest_image_path:
                self.last_detection_image = self.latest_image_path
            
            # Check if we've had high confidence for long enough
            detection_duration = current_time - self.fire_detected_start
            
            if detection_duration >= self.confirmation_duration and not self.emergency_sent:
                # Check cooldown period
                time_since_last_emergency = current_time - self.last_emergency_time
                
                if time_since_last_emergency < self.emergency_cooldown:
                    remaining_cooldown = self.emergency_cooldown - time_since_last_emergency
                    print(f"⏳ Emergency cooldown active: {remaining_cooldown:.0f}s remaining")
                    return
                
                # Fire confirmed! Send emergency alert ONLY ONCE
                print(f"✅ Fire confirmed after {detection_duration:.1f}s! Sending emergency...")
                
                # CRITICAL: Set emergency_sent BEFORE sending to prevent race conditions
                self.emergency_sent = True
                self.last_emergency_time = current_time
                
                # Now send the emergency
                self.send_fire_emergency()
                
            elif self.emergency_sent:
                # Emergency already sent, don't spam
                time_since_emergency = current_time - self.last_emergency_time
                print(f"✅ Emergency already sent {time_since_emergency:.0f}s ago - not sending duplicate")
            else:
                # Still confirming
                remaining_time = self.confirmation_duration - detection_duration
                print(f"⏱️  Confirming fire... {remaining_time:.1f}s remaining (duration: {detection_duration:.1f}s)")
        
        else:
            # Low confidence or no fire
            if self.fire_detected_start is not None:
                detection_duration = current_time - self.fire_detected_start
                print(f"📉 Fire confidence dropped below threshold. Detection lasted {detection_duration:.1f}s")
            
            # Reset detection state but KEEP emergency_sent flag to prevent duplicates
            self.fire_detected_start = None
            # DON'T reset emergency_sent - once sent, don't send again until manual reset or cooldown expires
    
    def send_fire_emergency(self):
        """Send fire emergency alert to AlertAI server"""
        try:
            print("🚨 FIRE CONFIRMED! Sending emergency alert...")
            
            # Prepare emergency data
            emergency_data = {
                "id": int(time.time()),  # Use timestamp as ID
                "emergency_type": "Fire",
                "location": {"lat": 11.849010, "lon": 13.056751},
                "image_url": self.get_image_url(),
                "timestamp": datetime.now().isoformat() + "Z",
                "building": self.building_name,
                "floor_affected": self.floor_affected,
                "created_at": datetime.now().isoformat() + "Z",
                # Additional fire-specific data
                "confidence": self.last_fire_confidence,
                "detection_duration": self.confirmation_duration,
                "room_location": "Kitchen area"  # You can make this dynamic
            }
            
            print(f"📤 Sending emergency data:")
            print(f"   🔥 Type: {emergency_data['emergency_type']}")
            print(f"   🏢 Building: {emergency_data['building']}")
            print(f"   🏠 Floor: {emergency_data['floor_affected']}")
            print(f"   📸 Image: {emergency_data['image_url']}")
            print(f"   🎯 Confidence: {emergency_data['confidence']:.2%}")
            
            # Send to AlertAI server
            response = requests.post(
                f"{self.alertai_server_url}/emergency",
                json=emergency_data,
                timeout=10
            )
            
            if response.status_code == 200:
                print("✅ Fire emergency sent successfully!")
                print("📱 Check the AlertAI web app for the alert")
                print("📱 WhatsApp emergency alert should be sent to configured contacts")
                
                # Move image to confirmed fires folder
                if self.last_detection_image:
                    self.archive_fire_image(confirmed=True)
                
                # Log the emergency
                self.log_emergency(emergency_data, success=True)
                
            else:
                print(f"❌ Failed to send emergency: HTTP {response.status_code}")
                print(f"   Response: {response.text}")
                print("⚠️  Emergency flag kept to prevent duplicate attempts")
                
                # DON'T reset emergency_sent flag - keep it to prevent duplicates
                # The emergency was confirmed, even if server rejected it
                
                # Move image to false alarms folder
                if self.last_detection_image:
                    self.archive_fire_image(confirmed=False)
                
        except requests.exceptions.ConnectionError:
            print(f"❌ Cannot connect to AlertAI server at {self.alertai_server_url}")
            print("⚠️  Server appears to be offline - emergency flag kept to prevent spam")
            print("📝 Emergency was confirmed but server is unreachable")
            
            # DON'T reset emergency_sent flag on connection errors
            # This prevents spam when server is offline
            
            # Move image to confirmed fires folder since fire was actually detected
            if self.last_detection_image:
                self.archive_fire_image(confirmed=True)
                
        except requests.exceptions.Timeout:
            print(f"❌ Timeout sending emergency to AlertAI server")
            print("⚠️  Emergency flag kept to prevent duplicate attempts")
            
            # DON'T reset emergency_sent flag on timeout
            
            # Move image to confirmed fires folder since fire was actually detected
            if self.last_detection_image:
                self.archive_fire_image(confirmed=True)
                
        except Exception as e:
            print(f"❌ Unexpected error sending fire emergency: {e}")
            print("⚠️  Emergency flag kept to prevent duplicate attempts")
            
            # DON'T reset emergency_sent flag on unexpected errors
            # Better to miss one alert than spam multiple alerts
            
            # Move image to confirmed fires folder since fire was actually detected
            if self.last_detection_image:
                self.archive_fire_image(confirmed=True)
    
    def get_image_url(self):
        """Get the URL for the last detection image"""
        if self.last_detection_image and os.path.exists(self.last_detection_image):
            # Return relative path for the server
            if "fire_dataset" in self.last_detection_image:
                # Already has fire_dataset in path
                return self.last_detection_image.replace("\\", "/")
            else:
                # Add fire_dataset prefix
                image_name = os.path.basename(self.last_detection_image)
                return f"fire_dataset/detections/{image_name}"
        else:
            # Check for test images first
            test_images_folder = os.path.join(self.fire_dataset_folder, "test_images")
            if os.path.exists(test_images_folder):
                image_extensions = ['.jpg', '.jpeg', '.png', '.bmp']
                for ext in image_extensions:
                    test_images = list(Path(test_images_folder).glob(f"*{ext}"))
                    if test_images:
                        # Use first available test image
                        return str(test_images[0]).replace("\\", "/")
            
            # Fallback to server test image
            return "test_images/fire_emergency.jpg"
    
    def archive_fire_image(self, confirmed=True):
        """Archive the fire detection image"""
        if not self.last_detection_image or not os.path.exists(self.last_detection_image):
            return
        
        try:
            folder = "confirmed_fires" if confirmed else "false_alarms"
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            image_name = f"fire_{timestamp}_{os.path.basename(self.last_detection_image)}"
            
            archive_path = os.path.join(self.fire_dataset_folder, folder, image_name)
            shutil.move(self.last_detection_image, archive_path)
            
            status = "confirmed" if confirmed else "false alarm"
            print(f"📁 Image archived as {status}: {image_name}")
            
        except Exception as e:
            print(f"❌ Error archiving image: {e}")
    
    def log_emergency(self, emergency_data, success=True):
        """Log emergency data to file"""
        try:
            log_file = os.path.join(self.fire_dataset_folder, "emergency_log.json")
            
            log_entry = {
                "timestamp": datetime.now().isoformat(),
                "success": success,
                "emergency_data": emergency_data,
                "confidence": self.last_fire_confidence,
                "image_path": self.last_detection_image
            }
            
            # Read existing log
            log_data = []
            if os.path.exists(log_file):
                with open(log_file, 'r') as f:
                    try:
                        log_data = json.load(f)
                    except json.JSONDecodeError:
                        log_data = []
            
            # Add new entry
            log_data.append(log_entry)
            
            # Keep only last 100 entries
            log_data = log_data[-100:]
            
            # Write back to file
            with open(log_file, 'w') as f:
                json.dump(log_data, f, indent=2)
                
        except Exception as e:
            print(f"❌ Error logging emergency: {e}")
    
    def start_monitoring(self):
        """Start the fire detection monitoring"""
        print("🚀 Starting Fire Detection Integration...")
        
        # Check server connection
        if not self.check_server_connection():
            print("❌ Cannot start without AlertAI server connection")
            return False
        
        # Setup monitoring folder
        self.setup_monitoring_folder()
        
        # Start monitoring
        self.monitoring = True
        
        try:
            self.monitor_model_output()
        except KeyboardInterrupt:
            print("\n🛑 Fire detection monitoring stopped by user")
        finally:
            self.monitoring = False
        
        return True
    
    def stop_monitoring(self):
        """Stop the fire detection monitoring"""
        self.monitoring = False
        print("🛑 Fire detection monitoring stopped")

    def reset_emergency_state(self):
        """Manually reset the emergency state to allow new alerts"""
        self.fire_detected_start = None
        self.emergency_sent = False
        self.last_fire_confidence = 0.0
        self.last_detection_image = None
        self.last_emergency_time = 0  # Also reset the cooldown timer
        print("🔄 Emergency state reset - ready for new detections")

    def retry_last_emergency(self):
        """Retry sending the last emergency if it failed due to server issues"""
        if self.emergency_sent:
            print("⚠️  Emergency already sent successfully - use reset_emergency_state() first if needed")
            return False
        
        if self.last_fire_confidence < self.confidence_threshold:
            print("⚠️  No confirmed fire detection to retry")
            return False
        
        print("🔄 Retrying last emergency...")
        # Temporarily reset the flag to allow retry
        self.emergency_sent = False
        self.send_fire_emergency()
        return True

    # INTEGRATION METHODS FOR YOUR MODEL
    def model_detection_callback(self, confidence, image_path=None):
        """
        Call this method from your fire detection model
        
        Args:
            confidence (float): Fire detection confidence (0.0 to 1.0)
            image_path (str): Path to the image that was analyzed
        """
        self.process_detection(confidence, image_path)
    
    def create_detection_result_file(self, confidence, image_path=""):
        """
        Create a detection result file for the monitor to pick up
        Use this if your model can't call the callback directly
        
        Args:
            confidence (float): Fire detection confidence (0.0 to 1.0)
            image_path (str): Path to the image that was analyzed
        """
        try:
            results = {
                "fire_confidence": confidence,
                "image_path": image_path,
                "timestamp": datetime.now().isoformat()
            }
            
            results_file = os.path.join(self.fire_dataset_folder, "detection_results.json")
            with open(results_file, 'w') as f:
                json.dump(results, f)
                
        except Exception as e:
            print(f"❌ Error creating detection result file: {e}")

def main():
    """Main function to run the fire detection integration"""
    print("🔥 FIRE DETECTION INTEGRATION FOR ALERTAI")
    print("=" * 60)
    
    # Create integration instance
    integration = FireDetectionIntegration()
    
    # Start monitoring
    integration.start_monitoring()

if __name__ == "__main__":
    main()