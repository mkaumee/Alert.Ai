import json
import math
import uuid
from datetime import datetime
from .db_utils import register_user_to_db, update_user_location_in_db, get_all_users_from_db

# Remove in-memory storage - now using database
# web_users = {}

def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    Returns distance in meters
    """
    # Convert decimal degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    
    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    
    # Radius of earth in meters
    r = 6371000
    return c * r

def register_user(user_data):
    """Register a new web app user in database"""
    from .db_utils import register_user_to_db
    return register_user_to_db(user_data)

def update_user_location(user_id, location):
    """Update user's location in database"""
    from .db_utils import update_user_location_in_db
    return update_user_location_in_db(user_id, location)

def get_nearby_users(emergency_location, users=None, threshold=100):
    """
    Returns users within threshold distance (meters) of emergency_location
    Combines mock users and registered web users from database
    """
    if users is None:
        users = load_users()
    
    # Add registered web users from database
    from .db_utils import get_all_users_from_db
    db_users = get_all_users_from_db()
    all_users = users + db_users
    
    nearby_users = []
    emergency_lat = emergency_location['lat']
    emergency_lon = emergency_location['lon']
    
    for user in all_users:
        if 'location' not in user or not user['location']:
            continue
            
        user_lat = user['location']['lat']
        user_lon = user['location']['lon']
        
        distance = haversine_distance(emergency_lat, emergency_lon, user_lat, user_lon)
        
        if distance <= threshold:
            user_with_distance = user.copy()
            user_with_distance['distance_meters'] = round(distance, 2)
            nearby_users.append(user_with_distance)
    
    print(f"Found {len(nearby_users)} users within {threshold}m of emergency")
    return nearby_users

def load_users():
    """
    Load user data from file or return mock data for testing
    In production, this would query a user database
    """
    # Mock user data for testing
    mock_users = [
        {
            "user_id": "user_001",
            "name": "John Doe",
            "phone": "+234801234567",
            "location": {"lat": 11.849010, "lon": 13.056751},  # Same location as emergency
            "fcm_token": "mock_fcm_token_1"
        },
        {
            "user_id": "user_002", 
            "name": "Jane Smith",
            "phone": "+234807654321",
            "location": {"lat": 6.5245, "lon": 3.3793},  # Very close (about 15m away)
            "fcm_token": "mock_fcm_token_2"
        },
        {
            "user_id": "user_003",
            "name": "Bob Johnson", 
            "phone": "+234809876543",
            "location": {"lat": 6.5250, "lon": 3.3800},  # About 90m away
            "fcm_token": "mock_fcm_token_3"
        },
        {
            "user_id": "user_004",
            "name": "Alice Brown",
            "phone": "+234803456789", 
            "location": {"lat": 6.5300, "lon": 3.3900},  # Far away (about 1.2km)
            "fcm_token": "mock_fcm_token_4"
        }
    ]
    
    return mock_users