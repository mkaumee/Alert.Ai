# AlertAI - Intelligent Emergency Response System

![AlertAI Logo](https://img.shields.io/badge/AlertAI-Emergency%20Response-red?style=for-the-badge&logo=shield&logoColor=white)

## 🚨 Overview

AlertAI is a comprehensive AI-powered emergency detection and response system that combines computer vision, natural language processing, and real-time communication to provide intelligent emergency management for buildings and facilities.

### Key Features

- **🔥 AI-Powered Emergency Detection** - YOLO-based fire detection with Gemini AI verification
- **🤖 Specialized Emergency Agents** - Dedicated AI agents for different emergency types
- **📱 Real-time Web Dashboard** - Live emergency monitoring and alert management
- **💬 WhatsApp Integration** - Instant emergency notifications via WhatsApp
- **🏥 CPR Monitoring** - PoseNet-based CPR technique monitoring and coaching
- **🗺️ Building-Specific Guidance** - Detailed evacuation routes and safety protocols
- **🌐 Multi-Platform Support** - Web app, mobile-responsive, and API access

## 🏗️ System Architecture

```
AlertAI System
├── 🖥️ Combined Server (Flask)
│   ├── Emergency Detection API
│   ├── Web App Hosting
│   ├── User Management
│   └── Alert Distribution
├── 🤖 AI Agents (Gemini-powered)
│   ├── Fire Emergency Agent
│   ├── Medical Emergency Agent
│   ├── Security Response Agent
│   ├── Smoke Safety Agent
│   └── Trauma Response Agent
├── 🌐 Web Application
│   ├── Emergency Dashboard
│   ├── User Registration
│   ├── Real-time Alerts
│   └── Guidance Interface
├── 🔍 Detection Systems
│   ├── YOLO Fire Detection
│   ├── CPR PoseNet Monitor
│   └── Gemini AI Verification
└── 📡 Communication
    ├── WhatsApp Notifications
    ├── Database Logging
    └── Real-time Updates
```

## 🚀 Quick Start

### Prerequisites

- Python 3.7+
- Node.js (for development)
- Webcam (for CPR monitoring)
- Internet connection

### 1. Clone Repository

```bash
git clone <repository-url>
cd alertai-system
```

### 2. Environment Setup

Create environment files:

```bash
# Main environment
cp .env.example .env

# Server environment  
cp server/.env.example server/.env

# Agent environment
cp alertai-agent/.env.example alertai-agent/.env
```

### 3. Configure API Keys

Edit the `.env` files with your API keys:

```bash
# Required API Keys
GEMINI_API_KEY=your_gemini_api_key_here
TWILIO_ACCOUNT_SID=your_twilio_sid
TWILIO_AUTH_TOKEN=your_twilio_token
TWILIO_WHATSAPP_FROM=whatsapp:+14155238886
```

### 4. Install Dependencies

```bash
# Server dependencies
pip install -r server/requirements.txt

# Agent dependencies  
pip install -r alertai-agent/requirements.txt

# YOLO dependencies (optional)
pip install -r yolo_requirements.txt
```

### 5. Start the System

```bash
# Start combined server (recommended)
python combined_server.py

# Or start components separately
python server/app.py          # API server only
python alertai-webapp/serve_webapp.py  # Web app only
```

### 6. Access the System

- **Web Dashboard**: http://localhost:8000
- **API Endpoints**: http://localhost:8000/api/
- **CPR Monitor**: http://localhost:8000/cpr-monitor
- **Health Check**: http://localhost:8000/health

## 📋 System Components

### 🖥️ Combined Server (`combined_server.py`)

The main server that combines all functionality:

- **Emergency Processing**: Receives and processes emergency alerts
- **AI Verification**: Uses Gemini AI to verify emergency authenticity
- **User Management**: Handles user registration and location tracking
- **Alert Distribution**: Sends notifications via WhatsApp and web
- **Static File Serving**: Hosts the web application
- **API Endpoints**: RESTful API for all system interactions

**Key Endpoints:**
- `POST /emergency` - Submit emergency alerts
- `GET /api/alerts/active` - Get active emergencies
- `POST /api/users/register` - Register new users
- `PUT /api/users/location` - Update user location
- `POST /api/guidance-agent` - Chat with emergency agents

### 🤖 AI Emergency Agents

Specialized Gemini-powered agents for different emergency types:

#### Fire Emergency Agent (`alertai-agent/fire_emergency_agent.py`)
- Fire safety protocols and evacuation procedures
- Building-specific fire suppression equipment guidance
- Real-time fire spread assessment and response

#### Medical Emergency Agent (`alertai-agent/fallen_person_agent.py`)
- First aid guidance and medical response protocols
- CPR instructions and medical emergency procedures
- Injury assessment and stabilization techniques

#### Security Response Agent (`alertai-agent/gun_emergency_agent.py`)
- Run-Hide-Fight protocols for active threats
- Lockdown procedures and safe room guidance
- Law enforcement coordination and communication

#### Smoke Safety Agent (`alertai-agent/smoke_emergency_agent.py`)
- Smoke inhalation prevention and evacuation
- Ventilation system management during emergencies
- Safe evacuation route identification

#### Trauma Response Agent (`alertai-agent/blood_emergency_agent.py`)
- Bleeding control and trauma response
- Shock prevention and victim stabilization
- Emergency medical service coordination

### 🌐 Web Application (`alertai-webapp/`)

Modern, responsive web interface:

- **Emergency Dashboard**: Real-time emergency monitoring
- **User Registration**: Location-based alert registration
- **Simulation Testing**: Emergency scenario testing tools
- **Guidance Interface**: Interactive emergency guidance chat
- **Alert History**: Past emergency records and responses

**Key Files:**
- `alertai.html` - Main dashboard interface
- `guidance.html` - Emergency guidance chat interface
- `app.js` - Main application logic and API integration
- `guidance.js` - Chat interface and agent communication
- `styles.css` - Responsive design and styling

### 🔍 Detection Systems

#### YOLO Fire Detection (`yolo_fire_detection.py`)
- Real-time fire detection using computer vision
- Confidence-based alert triggering
- Integration with AlertAI server for emergency processing

#### CPR PoseNet Monitor (`cpr-posenet-monitor/`)
- Real-time CPR technique monitoring using PoseNet
- Audio coaching with metronome timing
- Compression depth and rate feedback
- Cross-platform compatibility (Chrome, Safari, Firefox)

#### Gemini AI Verification (`server/utils/gemini_verification_local.py`)
- AI-powered emergency verification
- False positive reduction
- Image analysis and context understanding

### 📡 Communication Systems

#### WhatsApp Integration (`server/utils/twilio_whatsapp.py`)
- Instant emergency notifications
- Multi-user alert distribution
- Delivery confirmation and status tracking

#### Database Management (`server/utils/db_utils.py`)
- SQLite database for emergency logging
- User management and location tracking
- Alert history and analytics

## 🛠️ Configuration

### Environment Variables

```bash
# API Configuration
GEMINI_API_KEY=your_gemini_api_key
ALERTAI_SERVER_URL=http://localhost:8000

# Twilio WhatsApp
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_WHATSAPP_FROM=whatsapp:+14155238886

# Emergency Contacts
EMERGENCY_CONTACTS=+1234567890,+0987654321

# Detection Settings
FIRE_CONFIDENCE_THRESHOLD=0.5
DETECTION_INTERVAL=1.0
```

### Building Configuration

Customize building-specific settings in the server:

```python
# Building layout and emergency resources
building_data = {
    "floors": ["Ground Floor", "1st Floor", "2nd Floor"],
    "fire_extinguishers": {...},
    "emergency_exits": {...},
    "assembly_points": {...}
}
```

## 🧪 Testing

### Emergency Simulation

Use the web dashboard simulation buttons to test different emergency scenarios:

1. **Fire Emergency** - Test fire detection and response
2. **Medical Emergency** - Test medical response protocols  
3. **Security Emergency** - Test lockdown and security procedures
4. **Smoke Emergency** - Test smoke evacuation procedures
5. **Trauma Emergency** - Test bleeding control and trauma response

### Manual Testing Scripts

```bash
# Test individual emergency types
python send_fire_emergency.py
python send_blood_emergency.py
python send_fallen_person_emergency.py
python send_smoke_emergency.py

# Test WhatsApp integration
python demo_whatsapp_message.py

# Test YOLO fire detection
python test_yolo_fire_model.py
```

### CPR Monitor Testing

Access the CPR monitor at `http://localhost:8000/cpr-monitor` to test:
- Camera permissions and video feed
- Pose detection accuracy
- Audio coaching and metronome
- Compression rate and depth feedback

## 📱 Usage Examples

### Web Dashboard Registration

1. Open http://localhost:8000
2. Fill in user details (name, phone, email)
3. Enable location access for proximity alerts
4. Register to receive emergency notifications

### Emergency Agent Interaction

1. Trigger an emergency (simulation or real)
2. Click "Start [Emergency Type] Agent" in the alert modal
3. Chat with the specialized AI agent for guidance
4. Follow step-by-step emergency procedures

### WhatsApp Notifications

Users receive instant WhatsApp messages with:
- Emergency type and location
- Distance from user's location
- Immediate action instructions
- Building-specific guidance links

## 🔧 Development

### Adding New Emergency Types

1. Create new agent in `alertai-agent/`
2. Add emergency type to server routing
3. Update web app simulation buttons
4. Add detection integration if needed

### Extending Building Data

1. Update building configuration in server
2. Add floor plans and resource locations
3. Customize evacuation routes
4. Update emergency contact information

### API Integration

The system provides RESTful APIs for integration:

```javascript
// Submit emergency
POST /emergency
{
  "emergency_type": "Fire",
  "location": {"lat": 11.849010, "lon": 13.056751},
  "building": "Building A",
  "timestamp": "2026-01-29T12:00:00Z",
  "image_url": "detection_image.jpg"
}

// Get active alerts
GET /api/alerts/active

// Chat with agent
POST /api/guidance-agent
{
  "emergency_type": "Fire",
  "message": "I see smoke in the hallway",
  "history": []
}
```

## 🚀 Deployment

### Local Development
```bash
python combined_server.py
```

### Production Deployment
```bash
# Use production WSGI server
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 combined_server:app
```

### ngrok Tunneling (for testing)
```bash
# Install ngrok
ngrok http 8000

# Configure webhook URLs with ngrok URL
python configure_ngrok.py
```

## 📊 Monitoring and Analytics

- **Emergency Response Times**: Track alert-to-response metrics
- **Detection Accuracy**: Monitor false positive/negative rates  
- **User Engagement**: Analyze alert acknowledgment rates
- **System Performance**: Monitor API response times and uptime

## 🔒 Security Considerations

- **API Key Management**: Store sensitive keys in environment files
- **User Data Protection**: Encrypt location and personal data
- **Emergency Verification**: AI-powered false positive prevention
- **Access Control**: Secure admin endpoints and sensitive operations

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/new-emergency-type`)
3. Commit changes (`git commit -am 'Add new emergency detection'`)
4. Push to branch (`git push origin feature/new-emergency-type`)
5. Create Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For emergency system support:
- **Documentation**: Check component-specific README files
- **Issues**: Report bugs via GitHub issues
- **Emergency Testing**: Use simulation buttons for safe testing
- **Real Emergencies**: Always call local emergency services (911) first

## 🙏 Acknowledgments

- **Google Gemini AI** - Emergency verification and agent intelligence
- **Twilio** - WhatsApp communication infrastructure  
- **TensorFlow.js** - PoseNet CPR monitoring
- **YOLO** - Computer vision fire detection
- **Flask** - Web framework and API development

---

**⚠️ Important**: This system is designed to supplement, not replace, traditional emergency response systems. Always contact local emergency services (911) for real emergencies.