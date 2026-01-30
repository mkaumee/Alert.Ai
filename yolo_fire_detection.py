#!/usr/bin/env python3
"""
YOLO Fire Detection Model Integration with AlertAI
Integrates YOLO fire detection model with AlertAI emergency response system
"""
import os
import sys
import cv2
import time
import json
import numpy as np
from datetime import datetime
from pathlib import Path
import threading
import queue

# Import the fire detection integration
from fire_detection_integration import FireDetectionIntegration

class YOLOFireDetection:
    def __init__(self, model_path="fire_dataset", server_url=None):
        self.model_path = model_path
        self.model = None
        self.class_names = ['fire']  # YOLO class names
        self.confidence_threshold = 0.1  # Lower threshold for classification models
        self.fire_class_id = 0  # Fire class ID in YOLO model
        
        # AlertAI integration - FIXED: Initialize properly with configurable server URL
        self.alertai_integration = FireDetectionIntegration(server_url)
        
        # Video capture
        self.cap = None
        self.is_running = False
        
        # Detection state
        self.frame_count = 0
        self.detection_history = []
        self.max_history = 30  # Keep last 30 detections for smoothing
        
        # ADDED: Fire detection tracking
        self.current_fire_confidence = 0.0
        self.fire_detection_active = False
        
        print("🔥 YOLO Fire Detection Model Integration")
        print(f"📁 Model path: {self.model_path}")
        print(f"🎯 AlertAI threshold: {self.alertai_integration.confidence_threshold * 100}%")
        print(f"⏱️  Confirmation time: {self.alertai_integration.confirmation_duration}s")
        
    def load_yolo_model(self):
        """Load YOLO model from the fire_dataset folder"""
        try:
            # Look for common YOLO model files
            model_files = [
                "best.pt",           # YOLOv8/YOLOv5 trained model
                "fire_model.pt",     # Custom named model
                "yolo_fire.pt",      # Alternative name
                "model.pt",          # Generic name
                "fire.weights",      # YOLOv4/v3 weights
                "yolo_fire.weights"  # Alternative weights
            ]
            
            model_file_path = None
            for model_file in model_files:
                potential_path = os.path.join(self.model_path, model_file)
                if os.path.exists(potential_path):
                    model_file_path = potential_path
                    break
            
            if not model_file_path:
                print("❌ No YOLO model file found in fire_dataset folder")
                print(f"   Looking for: {', '.join(model_files)}")
                return False
            
            print(f"📦 Loading YOLO model: {model_file_path}")
            
            # Try different YOLO implementations
            if self.load_ultralytics_yolo(model_file_path):
                return True
            elif self.load_opencv_yolo(model_file_path):
                return True
            else:
                print("❌ Failed to load YOLO model with any method")
                return False
                
        except Exception as e:
            print(f"❌ Error loading YOLO model: {e}")
            return False
    
    def load_ultralytics_yolo(self, model_path):
        """Load YOLO model using Ultralytics (YOLOv8/v5)"""
        try:
            from ultralytics import YOLO
            self.model = YOLO(model_path)
            self.model_type = "ultralytics"
            print("✅ Loaded Ultralytics YOLO model")
            return True
        except ImportError:
            print("⚠️  Ultralytics not available, trying other methods...")
            return False
        except Exception as e:
            print(f"⚠️  Failed to load with Ultralytics: {e}")
            return False
    
    def load_opencv_yolo(self, model_path):
        """Load YOLO model using OpenCV DNN"""
        try:
            # Look for config and weights files
            config_files = [
                os.path.join(self.model_path, "yolo_fire.cfg"),
                os.path.join(self.model_path, "fire.cfg"),
                os.path.join(self.model_path, "yolo.cfg")
            ]
            
            config_path = None
            for config_file in config_files:
                if os.path.exists(config_file):
                    config_path = config_file
                    break
            
            if config_path and model_path.endswith('.weights'):
                self.model = cv2.dnn.readNet(model_path, config_path)
                self.model_type = "opencv"
                print("✅ Loaded OpenCV DNN YOLO model")
                return True
            else:
                print("⚠️  OpenCV DNN requires .cfg and .weights files")
                return False
                
        except Exception as e:
            print(f"⚠️  Failed to load with OpenCV: {e}")
            return False
    
    def detect_fire_ultralytics(self, frame):
        """Detect fire using Ultralytics YOLO"""
        try:
            results = self.model(frame, conf=self.confidence_threshold)
            
            max_confidence = 0.0
            fire_detections = []
            
            for result in results:
                # Check if this is a classification model
                if hasattr(result, 'probs') and result.probs is not None:
                    # Classification model - get fire class probability
                    probs = result.probs
                    if hasattr(probs, 'data'):
                        # Get fire class confidence (assuming class 0 is Fire)
                        if len(probs.data) > 0:
                            fire_confidence = float(probs.data[0])  # Fire class
                            max_confidence = fire_confidence
                            
                            if fire_confidence > self.confidence_threshold:
                                # Create a fake detection covering the whole image for visualization
                                h, w = frame.shape[:2]
                                fire_detections.append({
                                    'confidence': fire_confidence,
                                    'bbox': [w//4, h//4, 3*w//4, 3*h//4],  # Center box
                                    'class_id': 0,
                                    'type': 'classification'
                                })
                
                # Check if this is a detection model
                elif hasattr(result, 'boxes') and result.boxes is not None:
                    # Detection model - get bounding boxes
                    boxes = result.boxes
                    for box in boxes:
                        # Get class ID and confidence
                        class_id = int(box.cls[0])
                        confidence = float(box.conf[0])
                        
                        # Check if it's fire class (assuming fire is class 0)
                        if class_id == self.fire_class_id and confidence > self.confidence_threshold:
                            fire_detections.append({
                                'confidence': confidence,
                                'bbox': box.xyxy[0].tolist(),  # [x1, y1, x2, y2]
                                'class_id': class_id,
                                'type': 'detection'
                            })
                            max_confidence = max(max_confidence, confidence)
            
            return max_confidence, fire_detections
            
        except Exception as e:
            print(f"❌ Error in Ultralytics detection: {e}")
            return 0.0, []
    
    def detect_fire_opencv(self, frame):
        """Detect fire using OpenCV DNN"""
        try:
            height, width = frame.shape[:2]
            
            # Create blob from frame
            blob = cv2.dnn.blobFromImage(frame, 1/255.0, (416, 416), swapRB=True, crop=False)
            self.model.setInput(blob)
            
            # Run inference
            outputs = self.model.forward()
            
            max_confidence = 0.0
            fire_detections = []
            
            for output in outputs:
                for detection in output:
                    scores = detection[5:]
                    class_id = np.argmax(scores)
                    confidence = scores[class_id]
                    
                    if class_id == self.fire_class_id and confidence > self.confidence_threshold:
                        # Get bounding box
                        center_x = int(detection[0] * width)
                        center_y = int(detection[1] * height)
                        w = int(detection[2] * width)
                        h = int(detection[3] * height)
                        
                        x1 = int(center_x - w/2)
                        y1 = int(center_y - h/2)
                        x2 = int(center_x + w/2)
                        y2 = int(center_y + h/2)
                        
                        fire_detections.append({
                            'confidence': float(confidence),
                            'bbox': [x1, y1, x2, y2],
                            'class_id': class_id
                        })
                        max_confidence = max(max_confidence, float(confidence))
            
            return max_confidence, fire_detections
            
        except Exception as e:
            print(f"❌ Error in OpenCV detection: {e}")
            return 0.0, []
    
    def detect_fire_in_frame(self, frame):
        """Detect fire in a single frame"""
        if self.model is None:
            return 0.0, []
        
        if self.model_type == "ultralytics":
            return self.detect_fire_ultralytics(frame)
        elif self.model_type == "opencv":
            return self.detect_fire_opencv(frame)
        else:
            return 0.0, []
    
    def smooth_detections(self, confidence):
        """Smooth detection confidence over multiple frames"""
        self.detection_history.append(confidence)
        
        # Keep only recent history
        if len(self.detection_history) > self.max_history:
            self.detection_history.pop(0)
        
        # Calculate smoothed confidence (average of recent detections)
        if len(self.detection_history) >= 5:  # Need at least 5 frames
            smoothed_confidence = np.mean(self.detection_history[-10:])  # Average last 10 frames
            return smoothed_confidence
        else:
            return confidence
    
    def draw_detections(self, frame, detections, confidence):
        """Draw fire detection boxes on frame"""
        for detection in detections:
            bbox = detection['bbox']
            conf = detection['confidence']
            detection_type = detection.get('type', 'detection')
            
            if detection_type == 'classification':
                # For classification, draw a border around the image
                h, w = frame.shape[:2]
                color = (0, 0, 255) if conf > 0.8 else (0, 165, 255)  # Red if high confidence, orange if medium
                thickness = 5 if conf > 0.8 else 3
                cv2.rectangle(frame, (10, 10), (w-10, h-10), color, thickness)
                
                # Draw classification label
                label = f"FIRE CLASSIFICATION: {conf:.2%}"
                cv2.putText(frame, label, (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
            else:
                # For detection, draw bounding box
                cv2.rectangle(frame, (int(bbox[0]), int(bbox[1])), (int(bbox[2]), int(bbox[3])), (0, 0, 255), 2)
                
                # Draw confidence text
                label = f"Fire: {conf:.2%}"
                cv2.putText(frame, label, (int(bbox[0]), int(bbox[1])-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        
        # Draw overall confidence
        status_text = f"Fire Confidence: {confidence:.2%}"
        color = (0, 255, 0) if confidence < 0.5 else (0, 165, 255) if confidence < 0.8 else (0, 0, 255)
        cv2.putText(frame, status_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
        
        # FIXED: Draw AlertAI status properly
        alertai_threshold = self.alertai_integration.confidence_threshold
        threshold_text = f"AlertAI Threshold: {alertai_threshold:.2%}"
        cv2.putText(frame, threshold_text, (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2)
        
        # Show confirmation countdown and status
        if hasattr(self.alertai_integration, 'fire_detected_start') and self.alertai_integration.fire_detected_start:
            import time
            elapsed = time.time() - self.alertai_integration.fire_detected_start
            remaining = self.alertai_integration.confirmation_duration - elapsed
            if remaining > 0:
                alert_text = f"CONFIRMING FIRE: {remaining:.1f}s ({elapsed:.1f}s elapsed)"
                cv2.putText(frame, alert_text, (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 165, 255), 2)
            else:
                alert_text = "FIRE CONFIRMED - ALERT SENT!"
                cv2.putText(frame, alert_text, (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        # Show emergency sent status
        if hasattr(self.alertai_integration, 'emergency_sent') and self.alertai_integration.emergency_sent:
            sent_text = "EMERGENCY ALERT SENT TO SERVER!"
            cv2.putText(frame, sent_text, (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        
        # Show detection count and frame info
        detection_count = len(detections)
        count_text = f"Frame {self.frame_count}: Detections={detection_count}"
        cv2.putText(frame, count_text, (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        
        return frame
    
    def save_detection_image(self, frame, confidence, detections):
        """Save image when fire is detected"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
            filename = f"fire_detection_{timestamp}_{confidence:.2f}.jpg"
            filepath = os.path.join(self.model_path, "detections", filename)
            
            # Ensure detections folder exists
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            
            # Draw detections on frame before saving
            annotated_frame = self.draw_detections(frame.copy(), detections, confidence)
            
            # Save image
            cv2.imwrite(filepath, annotated_frame)
            
            return filepath
            
        except Exception as e:
            print(f"❌ Error saving detection image: {e}")
            return None
    
    def start_camera_detection(self, camera_id=0):
        """Start fire detection from camera"""
        print(f"📹 Starting camera fire detection (Camera {camera_id})")
        
        # Initialize camera
        self.cap = cv2.VideoCapture(camera_id)
        if not self.cap.isOpened():
            print(f"❌ Cannot open camera {camera_id}")
            return False
        
        # Set camera properties
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.cap.set(cv2.CAP_PROP_FPS, 30)
        
        self.is_running = True
        
        print("🔥 Fire detection started - Controls:")
        print("   Press 'q' to quit")
        print("   Press 't' to test with fake 90% confidence")
        print("   Press 'r' to reset detection state")
        print("   Press 's' to show current status")
        print("   Press 'h' for help")
        print("📊 Detection will be sent to AlertAI when fire is confirmed")
        
        try:
            while self.is_running:
                ret, frame = self.cap.read()
                if not ret:
                    print("❌ Failed to read frame from camera")
                    break
                
                self.frame_count += 1
                
                # Detect fire in frame
                confidence, detections = self.detect_fire_in_frame(frame)
                
                # Smooth confidence over multiple frames
                smoothed_confidence = self.smooth_detections(confidence)
                
                # Update current fire confidence for display
                self.current_fire_confidence = smoothed_confidence
                
                # FIXED: Always send detection data to AlertAI integration
                if self.frame_count % 10 == 0:  # Log every 10 frames to avoid spam
                    print(f"🔥 Frame {self.frame_count}: Raw={confidence:.2%}, Smoothed={smoothed_confidence:.2%}, Detections={len(detections)}")
                
                # Send to AlertAI integration - ALWAYS call this
                image_path = None
                if smoothed_confidence > 0.3:  # Save image for any reasonable detection
                    image_path = self.save_detection_image(frame, smoothed_confidence, detections)
                
                # CRITICAL: Always call the integration callback
                self.alertai_integration.model_detection_callback(smoothed_confidence, image_path)
                
                # Draw detections on frame
                display_frame = self.draw_detections(frame, detections, smoothed_confidence)
                
                # Show frame
                cv2.imshow('YOLO Fire Detection - AlertAI Integration', display_frame)
                
                # Check for quit
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    break
                elif key == ord('t'):  # Press 't' to test with fake high confidence
                    print("🧪 Testing with fake 90% confidence...")
                    self.alertai_integration.model_detection_callback(0.90, image_path)
                elif key == ord('r'):  # Press 'r' to reset detection state
                    print("🔄 Resetting detection state...")
                    self.alertai_integration.reset_emergency_state()
                elif key == ord('s'):  # Press 's' to show current status
                    print(f"📊 Current Status:")
                    print(f"   Fire confidence: {smoothed_confidence:.2%}")
                    print(f"   Detection active: {self.alertai_integration.fire_detected_start is not None}")
                    print(f"   Emergency sent: {self.alertai_integration.emergency_sent}")
                    if self.alertai_integration.fire_detected_start:
                        elapsed = time.time() - self.alertai_integration.fire_detected_start
                        print(f"   Detection duration: {elapsed:.1f}s")
                elif key == ord('h'):  # Press 'h' for help
                    print("🎮 Controls:")
                    print("   q - Quit")
                    print("   t - Test with fake 90% confidence")
                    print("   r - Reset detection state")
                    print("   s - Show current status")
                    print("   h - Show this help")
                
                # Limit FPS
                time.sleep(0.1)  # ~10 FPS for better processing
                
        except KeyboardInterrupt:
            print("\n🛑 Fire detection stopped by user")
        finally:
            self.cleanup()
        
        return True
    
    def start_video_detection(self, video_path):
        """Start fire detection from video file"""
        print(f"🎥 Starting video fire detection: {video_path}")
        
        if not os.path.exists(video_path):
            print(f"❌ Video file not found: {video_path}")
            return False
        
        # Initialize video capture
        self.cap = cv2.VideoCapture(video_path)
        if not self.cap.isOpened():
            print(f"❌ Cannot open video: {video_path}")
            return False
        
        self.is_running = True
        
        print("🔥 Video fire detection started - Press 'q' to quit")
        
        try:
            while self.is_running:
                ret, frame = self.cap.read()
                if not ret:
                    print("📹 End of video reached")
                    break
                
                self.frame_count += 1
                
                # Detect fire in frame
                confidence, detections = self.detect_fire_in_frame(frame)
                
                # Smooth confidence
                smoothed_confidence = self.smooth_detections(confidence)
                
                # Send to AlertAI integration
                if smoothed_confidence > 0.1:
                    image_path = None
                    if smoothed_confidence > 0.6:
                        image_path = self.save_detection_image(frame, smoothed_confidence, detections)
                    
                    self.alertai_integration.model_detection_callback(smoothed_confidence, image_path)
                
                # Draw detections
                display_frame = self.draw_detections(frame, detections, smoothed_confidence)
                
                # Show frame
                cv2.imshow('YOLO Fire Detection - Video', display_frame)
                
                # Check for quit
                key = cv2.waitKey(30) & 0xFF
                if key == ord('q'):
                    break
                
        except KeyboardInterrupt:
            print("\n🛑 Video detection stopped by user")
        finally:
            self.cleanup()
        
        return True
    
    def cleanup(self):
        """Clean up resources"""
        self.is_running = False
        if self.cap:
            self.cap.release()
        cv2.destroyAllWindows()
        print("🧹 Cleanup completed")
    
    def start_test_mode(self):
        """Test mode - simulate fire detection with real fire images"""
        print("🧪 TEST MODE: Simulating fire detection with real fire images")
        print("This will use actual fire images from fire_dataset/test_images folder")
        print("Press Ctrl+C to stop")
        
        # Check AlertAI server connection
        if not self.alertai_integration.check_server_connection():
            print("❌ AlertAI server not available - start server first!")
            return False
        
        # Check for test images
        test_images_folder = os.path.join(self.model_path, "test_images")
        if not os.path.exists(test_images_folder):
            print(f"❌ Test images folder not found: {test_images_folder}")
            print("Creating folder and using fallback image...")
            os.makedirs(test_images_folder, exist_ok=True)
            test_image_path = "test_images/fire_emergency.jpg"  # Fallback
        else:
            # Find available test images
            image_extensions = ['.jpg', '.jpeg', '.png', '.bmp']
            test_images = []
            for ext in image_extensions:
                test_images.extend(Path(test_images_folder).glob(f"*{ext}"))
            
            if test_images:
                # Use the first available test image
                test_image_path = str(test_images[0])
                print(f"✅ Using test fire image: {os.path.basename(test_image_path)}")
            else:
                print(f"⚠️  No test images found in {test_images_folder}")
                test_image_path = "test_images/fire_emergency.jpg"  # Fallback
        
        try:
            confidence_sequence = [
                0.1, 0.2, 0.3, 0.5, 0.7, 0.85, 0.87, 0.89, 0.85, 0.88,  # Ramp up to trigger
                0.85, 0.87, 0.85, 0.86, 0.84, 0.85, 0.87, 0.85, 0.86, 0.85  # Sustained high confidence
            ]
            
            for i, confidence in enumerate(confidence_sequence):
                print(f"\n🔥 Test Step {i+1}: Simulating {confidence:.2%} confidence")
                print(f"   Using image: {os.path.basename(test_image_path)}")
                
                # Send to AlertAI integration with real fire image
                self.alertai_integration.model_detection_callback(confidence, test_image_path)
                
                # Wait between detections
                time.sleep(1.0)
                
                # Check if emergency was sent
                if self.alertai_integration.emergency_sent:
                    print("✅ Emergency alert sent! Check your web app.")
                    print("🎯 This should pass Gemini verification since we used a real fire image")
                    break
            
            print("\n🧪 Test mode completed")
            
        except KeyboardInterrupt:
            print("\n🛑 Test mode stopped by user")
        
        return True

def main():
    """Main function to run YOLO fire detection"""
    import sys
    
    print("🔥 YOLO FIRE DETECTION - ALERTAI INTEGRATION")
    print("=" * 60)
    
    # Check for server URL argument
    server_url = None
    if len(sys.argv) > 1:
        server_url = sys.argv[1]
        print(f"🌐 Using custom server URL: {server_url}")
    else:
        # Check environment variable
        server_url = os.environ.get('ALERTAI_SERVER_URL')
        if server_url:
            print(f"🌐 Using server URL from environment: {server_url}")
        else:
            print(f"🌐 Using default server URL: http://localhost:8000")
    
    # Create YOLO fire detection instance
    detector = YOLOFireDetection(server_url=server_url)
    
    # Load YOLO model
    if not detector.load_yolo_model():
        print("❌ Failed to load YOLO model")
        print("\n📋 Setup Instructions:")
        print("1. Place your YOLO model file in the 'fire_dataset' folder")
        print("2. Supported files: best.pt, fire_model.pt, yolo_fire.weights, etc.")
        print("3. For OpenCV DNN: also include .cfg file")
        print("4. Install required packages:")
        print("   pip install ultralytics opencv-python")
        return
    
    # Check AlertAI server connection
    if not detector.alertai_integration.check_server_connection():
        print("❌ AlertAI server not available")
        print("   Please start the server: python server/app.py")
        return
    
    # Setup monitoring folder
    detector.alertai_integration.setup_monitoring_folder()
    
    # Choose detection mode
    print("\n🎯 Choose detection mode:")
    print("1. Camera detection (live)")
    print("2. Video file detection")
    print("3. Test mode (simulate fire detection)")
    print("4. Exit")
    
    while True:
        try:
            choice = input("\nEnter choice (1-4): ").strip()
            
            if choice == "1":
                # Camera detection
                camera_id = input("Enter camera ID (0 for default): ").strip()
                camera_id = int(camera_id) if camera_id.isdigit() else 0
                detector.start_camera_detection(camera_id)
                break
                
            elif choice == "2":
                # Video file detection
                video_path = input("Enter video file path: ").strip()
                detector.start_video_detection(video_path)
                break
                
            elif choice == "3":
                # Test mode
                detector.start_test_mode()
                break
                
            elif choice == "4":
                print("👋 Exiting...")
                break
                
            else:
                print("❌ Invalid choice. Please enter 1, 2, 3, or 4.")
                
        except KeyboardInterrupt:
            print("\n👋 Exiting...")
            break
        except ValueError:
            print("❌ Invalid input. Please enter a number.")

if __name__ == "__main__":
    main()