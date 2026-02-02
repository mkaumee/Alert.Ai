# AlertAI - Intelligent Emergency Response System 

![AlertAI Logo](https://img.shields.io/badge/AlertAI-Emergency%20Response-red?style=for-the-badge\&logo=shield\&logoColor=white)

## Overview

AlertAI is a comprehensive AI-powered emergency detection and response system that combines computer vision, natural language processing, and real-time communication to provide intelligent emergency management for buildings and facilities.

### Key Features

* **AI-Powered Emergency Detection** - YOLO-based fire detection with Gemini AI verification
* **Specialized Emergency Agents** - Dedicated AI agents for different emergency types
* **Real-time Web Dashboard** - Live emergency monitoring and alert management
* **WhatsApp Integration** - Instant emergency notifications via WhatsApp
* **CPR Monitoring** - PoseNet-based CPR technique monitoring and coaching
* **Building-Specific Guidance** - Detailed evacuation routes and safety protocols
* **Multi-Platform Support** - Web app, mobile-responsive, and API access

## System Architecture

```
AlertAI System
├── Combined Server (Flask)
│   ├── Emergency Detection API
│   ├── Web App Hosting
│   ├── User Management
│   └── Alert Distribution
├── AI Agents (Gemini-powered)
│   ├── Fire Emergency Agent
│   ├── Medical Emergency Agent
│   ├── Security Response Agent
│   ├── Smoke Safety Agent
│   └── Trauma Response Agent
├── Web Application
│   ├── Emergency Dashboard
│   ├── User Registration
│   ├── Real-time Alerts
│   └── Guidance Interface
├── Detection Systems
│   ├── YOLO Fire Detection
│   ├── CPR PoseNet Monitor
│   └── Gemini AI Verification
└── Communication
    ├── WhatsApp Notifications
    ├── Database Logging
    └── Real-time Updates
```

## Quick Start

### Prerequisites

* Python 3.7+
* Node.js (for development)
* Webcam (for CPR monitoring)
* Internet connection

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
python server/app.py
python alertai-webapp/serve_webapp.py
```

### 6. Access the System

* **Web Dashboard**: [http://localhost:8000](http://localhost:8000)
* **API Endpoints**: [http://localhost:8000/api/](http://localhost:8000/api/)
* **CPR Monitor**: [http://localhost:8000/cpr-monitor](http://localhost:8000/cpr-monitor)
* **Health Check**: [http://localhost:8000/health](http://localhost:8000/health)

## System Components

### Combined Server (`combined_server.py`)

The main server that combines all functionality:

* **Emergency Processing**: Receives and processes emergency alerts
* **AI Verification**: Uses Gemini AI to verify emergency authenticity
* **User Management**: Handles user registration and location tracking
* **Alert Distribution**: Sends notifications via WhatsApp and web
* **Static File Serving**: Hosts the web application
* **API Endpoints**: RESTful API for all system interactions

**Key Endpoints:**

* `POST /emergency`
* `GET /api/alerts/active`
* `POST /api/users/register`
* `PUT /api/users/location`
* `POST /api/guidance-agent`

### AI Emergency Agents

Specialized Gemini-powered agents for different emergency types:

#### Fire Emergency Agent (`alertai-agent/fire_emergency_agent.py`)

* Fire safety protocols and evacuation procedures
* Building-specific fire suppression equipment guidance
* Real-time fire spread assessment and response

#### Medical Emergency Agent (`alertai-agent/fallen_person_agent.py`)

* First aid guidance and medical response protocols
* CPR instructions and medical emergency procedures
* Injury assessment and stabilization techniques

#### Security Response Agent (`alertai-agent/gun_emergency_agent.py`)

* Run-Hide-Fight protocols for active threats
* Lockdown procedures and safe room guidance
* Law enforcement coordination and communication

#### Smoke Safety Agent (`alertai-agent/smoke_emergency_agent.py`)

* Smoke inhalation prevention and evacuation
* Ventilation system management during emergencies
* Safe evacuation route identification

#### Trauma Response Agent (`alertai-agent/blood_emergency_agent.py`)

* Bleeding control and trauma response
* Shock prevention and victim stabilization
* Emergency medical service coordination

### Web Application (`alertai-webapp/`)

Modern, responsive web interface:

* Emergency Dashboard
* User Registration
* Simulation Testing
* Guidance Interface
* Alert History

## Configuration, Testing, Deployment, Monitoring, Security, Contributing, License, Support, and Acknowledgments


**Important**: This system is designed to supplement, not replace, traditional emergency response systems.


