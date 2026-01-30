# Emergency Alert Server

A Flask-based server that receives emergency events from edge devices, processes them with **Gemini 3 AI verification**, and sends alerts to nearby users.

## Features

- ✅ Receive emergency events via HTTP POST
- ✅ **Gemini 3 AI verification** - Analyzes images to verify real emergencies
- ✅ Store emergencies in SQLite database with verification status
- ✅ Filter users by proximity (Haversine distance)
- ✅ Send mock notifications to nearby users
- ✅ Health check endpoint
- ✅ Emergency history endpoint
- ✅ Reject false alarms automatically

## 🤖 Gemini 3 Integration

The system uses **Gemini 3 Flash Preview** to analyze emergency images and determine if they show real emergencies. This prevents false alarms and ensures only verified emergencies trigger alerts.

### How It Works:
1. Edge device sends emergency with image URL
2. **Gemini analyzes the image** for emergency indicators
3. If verified → Send alerts to nearby users
4. If rejected → Log but don't send alerts

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Up Gemini API Key
```bash
# Run the setup guide
python setup_gemini.py

# Or set manually:
export GEMINI_API_KEY="your_api_key_here"
```

### 3. Start the Server
```bash
python app.py
```
Server runs on `http://localhost:5000`

### 4. Test Gemini Verification
```bash
# Test with real emergency images
python test_gemini_verification.py

# Test basic functionality
python test_emergency.py
```

## API Endpoints

### POST /emergency
Receive emergency data from edge device.

**Request body:**
```json
{
  "emergency_type": "Bleeding",
  "location": {"lat": 6.5244, "lon": 3.3792},
  "image_url": "https://example.com/test1.jpg",
  "timestamp": "2026-01-21T22:00:00Z",
  "building": "Building A"
}
```

**Response:**
```json
{
  "status": "success",
  "emergency_id": 1,
  "users_notified": 3,
  "message": "Emergency logged and 3 users notified"
}
```

### GET /health
Health check endpoint.

### GET /emergencies
Get all emergency records for debugging.

## Database Schema

**emergencies table:**
- `id` - INTEGER PRIMARY KEY
- `emergency_type` - TEXT (Bleeding, Fire, etc.)
- `lat` - REAL (Latitude)
- `lon` - REAL (Longitude) 
- `image_url` - TEXT (Link to image)
- `timestamp` - DATETIME (Event time)
- `building` - TEXT (Building name)
- `created_at` - DATETIME (Record creation time)

## Configuration

- **Proximity threshold:** 100 meters (configurable in `utils/users.py`)
- **Database:** SQLite (`db/database.db`)
- **Mock users:** Defined in `utils/users.py`

## Next Steps

1. **Integrate Gemini 3:** Replace placeholder in `verify_emergency_with_gemini()`
2. **Add FCM:** Implement real push notifications in `utils/notifications.py`
3. **User management:** Add user registration/location update endpoints
4. **Production database:** Switch to PostgreSQL
5. **Authentication:** Add API key validation
6. **Logging:** Add proper logging with levels