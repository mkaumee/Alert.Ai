# AlertAI Web App

A modern web application for receiving AI-verified emergency alerts based on proximity.

## Features

### 🚨 Emergency Types Supported:
- **Fire Detection** - Real fire emergencies
- **Accident Detection** - Vehicle and other accidents  
- **Smoke Detection** - Smoke without visible fire
- **Fallen Person Detection** - Medical emergencies with fallen individuals
- **Weapon Detection** - Security threats with weapons
- **Blood Detection** - Medical emergencies with visible blood

### 📱 Core Functionality:
- **User Registration** - Name, phone, email, location access
- **Real-time Location Tracking** - GPS-based proximity alerts (100m radius)
- **Emergency Alert Modal** - Full-screen emergency notifications
- **Alert History** - Track past emergency alerts
- **Emergency Actions** - Call emergency services, acknowledge alerts
- **Responsive Design** - Works on desktop, tablet, and mobile

## How It Works

### 1. User Registration:
- User enters personal information
- Grants location access for proximity-based alerts
- System tracks GPS location for emergency filtering

### 2. Emergency Alert Flow:
```
Edge Device → Server → Gemini AI → Verified Emergency → Web App Alert
     ↓           ↓         ↓              ↓               ↓
  Captures    Receives   Verifies      Finds Nearby    Shows Alert
   Image      Emergency   Real/Fake     Users (100m)    to User
```

### 3. Alert Display:
- **Immediate Modal** - Full-screen emergency alert
- **Emergency Details** - Type, location, distance, time
- **Safety Instructions** - Specific guidance for emergency type
- **Action Buttons** - Call emergency services or acknowledge

## File Structure

```
alertai-webapp/
├── index.html          # Main HTML structure
├── styles.css          # Complete CSS styling
├── app.js             # JavaScript functionality
└── README.md          # This documentation
```

## Setup Instructions

### 1. Open the Web App:
```bash
# Navigate to the webapp folder
cd alertai-webapp

# Open in browser (any of these methods):
# Method 1: Double-click index.html
# Method 2: Use a local server
python -m http.server 8080
# Then open: http://localhost:8080

# Method 3: Use Live Server extension in VS Code
```

### 2. User Registration:
1. Enter your name, phone, and email
2. Click "Enable Location Access" and grant permissions
3. Click "Register for Alerts" to complete setup

### 3. Receive Alerts:
- The app will show demo alerts after 10 seconds and 1 minute
- In production, alerts come from your Flask server via push notifications
- Emergency modal appears with full alert details

## Integration with Flask Server

### Current Setup:
- **Demo Mode** - Shows simulated emergency alerts
- **Server URL** - Points to `http://localhost:5000` (your Flask server)

### Production Integration:
1. **User Registration API** - Send user data to Flask server
2. **Location Updates** - Send GPS coordinates to server every 30 seconds  
3. **Push Notifications** - Receive real emergency alerts via WebSocket or FCM
4. **Alert Acknowledgment** - Send confirmation back to server

### API Endpoints Needed:
```javascript
// Register user with server
POST /api/users/register
{
  "name": "John Doe",
  "phone": "+234801234567", 
  "email": "john@example.com",
  "location": {"lat": 6.5244, "lon": 3.3792}
}

// Update user location
PUT /api/users/location
{
  "user_id": "user_123",
  "location": {"lat": 6.5244, "lon": 3.3792}
}

// Acknowledge emergency alert
POST /api/alerts/acknowledge
{
  "user_id": "user_123",
  "alert_id": "alert_456"
}
```

## Emergency Alert Format

The web app expects emergency alerts in this format:

```json
{
  "id": 12345,
  "emergency_type": "Fire",
  "location": {"lat": 6.5244, "lon": 3.3792},
  "building": "Office Building A",
  "timestamp": "2026-01-23T02:00:00Z",
  "distance_meters": 45.2,
  "message": "🚨 FIRE EMERGENCY: Fire detected at Office Building A. You are 45m away. Evacuate immediately.",
  "instructions": "Exit building using nearest fire exit. Do not use elevators. Proceed to assembly point."
}
```

## Customization

### Emergency Types:
Edit the `emergency-grid` in `index.html` and corresponding CSS classes to add/remove emergency types.

### Alert Styling:
Modify CSS classes in `styles.css`:
- `.alert-modal` - Emergency alert popup
- `.emergency-type` - Emergency type cards
- `.alert-item` - Alert list items

### Notification Behavior:
Update JavaScript in `app.js`:
- `receiveEmergencyAlert()` - Handle incoming alerts
- `showEmergencyAlert()` - Display alert modal
- `playAlertSound()` - Alert sound/vibration

## Browser Compatibility

- **Chrome/Edge** - Full support
- **Firefox** - Full support  
- **Safari** - Full support
- **Mobile Browsers** - Responsive design

## Security Features

- **Location Privacy** - GPS data stored locally, only shared when necessary
- **Secure Storage** - User data in localStorage with encryption option
- **Input Validation** - Form validation and sanitization
- **HTTPS Ready** - Secure communication with server

## Next Steps

1. **Connect to Flask Server** - Replace demo alerts with real server integration
2. **Push Notifications** - Implement WebSocket or FCM for real-time alerts
3. **Offline Support** - Add service worker for offline functionality
4. **Advanced Features** - Add emergency contacts, medical info, evacuation routes

---

**AlertAI Web App is ready to receive and display AI-verified emergency alerts!** 🚨📱