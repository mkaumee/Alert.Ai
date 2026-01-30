#!/usr/bin/env python3
"""
Setup script for YOLO Fire Detection Integration with AlertAI
"""
import os
import sys
import subprocess
import shutil
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 7):
        print("❌ Python 3.7 or higher is required")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    return True

def install_requirements():
    """Install required packages"""
    print("📦 Installing required packages...")
    
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "yolo_requirements.txt"])
        print("✅ Requirements installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install requirements: {e}")
        return False

def setup_fire_dataset_folder():
    """Setup the fire_dataset folder structure"""
    print("📁 Setting up fire_dataset folder structure...")
    
    folders = [
        "fire_dataset",
        "fire_dataset/detections",
        "fire_dataset/confirmed_fires", 
        "fire_dataset/false_alarms",
        "fire_dataset/models"
    ]
    
    for folder in folders:
        os.makedirs(folder, exist_ok=True)
        print(f"   ✅ Created: {folder}")
    
    return True

def check_yolo_model():
    """Check if YOLO model exists in fire_dataset folder"""
    print("🔍 Checking for YOLO model files...")
    
    model_files = [
        "fire_dataset/best.pt",
        "fire_dataset/fire_model.pt", 
        "fire_dataset/yolo_fire.pt",
        "fire_dataset/model.pt",
        "fire_dataset/fire.weights",
        "fire_dataset/yolo_fire.weights"
    ]
    
    found_models = []
    for model_file in model_files:
        if os.path.exists(model_file):
            found_models.append(model_file)
            print(f"   ✅ Found: {model_file}")
    
    if not found_models:
        print("⚠️  No YOLO model files found in fire_dataset folder")
        print("\n📋 To add your YOLO model:")
        print("1. Copy your trained YOLO model to the fire_dataset folder")
        print("2. Supported formats:")
        print("   - YOLOv8/v5: best.pt, fire_model.pt, model.pt")
        print("   - YOLOv4/v3: fire.weights + fire.cfg")
        print("3. Rename your model file to one of the supported names")
        return False
    
    print(f"✅ Found {len(found_models)} YOLO model file(s)")
    return True

def test_opencv():
    """Test OpenCV installation"""
    print("📹 Testing OpenCV...")
    
    try:
        import cv2
        print(f"   ✅ OpenCV {cv2.__version__} installed")
        
        # Test camera access
        cap = cv2.VideoCapture(0)
        if cap.isOpened():
            print("   ✅ Camera access available")
            cap.release()
        else:
            print("   ⚠️  Camera not available (this is OK for video file detection)")
        
        return True
    except ImportError:
        print("   ❌ OpenCV not installed")
        return False

def test_ultralytics():
    """Test Ultralytics YOLO installation"""
    print("🤖 Testing Ultralytics YOLO...")
    
    try:
        from ultralytics import YOLO
        print("   ✅ Ultralytics YOLO installed")
        return True
    except ImportError:
        print("   ⚠️  Ultralytics not installed (OK if using OpenCV DNN)")
        return False

def check_alertai_server():
    """Check if AlertAI server is available"""
    print("🌐 Checking AlertAI server...")
    
    try:
        import requests
        response = requests.get("http://localhost:5000/health", timeout=5)
        if response.status_code == 200:
            print("   ✅ AlertAI server is running")
            return True
        else:
            print(f"   ❌ AlertAI server responded with status: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("   ❌ AlertAI server not running")
        print("   💡 Start with: python server/app.py")
        return False
    except Exception as e:
        print(f"   ❌ Error checking server: {e}")
        return False

def create_sample_config():
    """Create a sample configuration file"""
    print("⚙️  Creating sample configuration...")
    
    config = {
        "model_path": "fire_dataset",
        "confidence_threshold": 0.5,
        "alertai_server": "http://localhost:5000",
        "building_name": "Medical Center Building A",
        "floor_affected": "1st Floor",
        "camera_id": 0,
        "detection_smoothing": True,
        "save_detections": True
    }
    
    try:
        import json
        with open("yolo_config.json", "w") as f:
            json.dump(config, f, indent=2)
        print("   ✅ Created yolo_config.json")
        return True
    except Exception as e:
        print(f"   ❌ Failed to create config: {e}")
        return False

def main():
    """Main setup function"""
    print("🔥 YOLO FIRE DETECTION SETUP FOR ALERTAI")
    print("=" * 60)
    
    success = True
    
    # Check Python version
    if not check_python_version():
        success = False
    
    # Setup folder structure
    if not setup_fire_dataset_folder():
        success = False
    
    # Install requirements
    if not install_requirements():
        success = False
    
    # Test installations
    if not test_opencv():
        success = False
    
    test_ultralytics()  # Optional
    
    # Check for YOLO model
    if not check_yolo_model():
        print("⚠️  Setup incomplete - YOLO model needed")
    
    # Check AlertAI server
    check_alertai_server()  # Optional for setup
    
    # Create sample config
    create_sample_config()
    
    print("\n" + "=" * 60)
    if success:
        print("✅ YOLO Fire Detection setup completed successfully!")
        print("\n🚀 Next steps:")
        print("1. Add your YOLO model to the fire_dataset folder")
        print("2. Start AlertAI server: python server/app.py")
        print("3. Run fire detection: python yolo_fire_detection.py")
    else:
        print("❌ Setup completed with some issues")
        print("   Please resolve the issues above before running")
    
    print("\n📚 Files created:")
    print("   - fire_dataset/ (folder structure)")
    print("   - yolo_config.json (configuration)")
    print("   - yolo_fire_detection.py (main script)")
    print("   - fire_detection_integration.py (AlertAI integration)")

if __name__ == "__main__":
    main()