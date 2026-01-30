# Database Initialization Fix for Railway Deployment

## Problem
When deploying AlertAI to Railway, users encountered "user table not found" errors when trying to create accounts. This was due to database initialization issues in the Railway environment.

## Root Cause
Railway's file system has different permissions and writable directories compared to local development. The database initialization was failing silently, causing the tables not to be created.

## Solution Implemented

### 1. Enhanced Database Initialization (`server/utils/db_utils.py`)
- Added comprehensive error handling and logging
- Implemented fallback directory strategy:
  1. First try: `./db/database.db` (original location)
  2. Second try: `/tmp/database.db` (Railway writable directory)
  3. Final fallback: In-memory database (temporary solution)
- Added detailed logging to track initialization process
- Added table verification after creation

### 2. Enhanced Health Check Endpoint (`combined_server.py`)
- Added `/health` endpoint with database status
- Shows database path, tables, and record counts
- Helps diagnose database issues in production

### 3. Manual Database Initialization Endpoint
- Added `/init-db` POST endpoint for manual database initialization
- Can be called if automatic initialization fails

## Testing the Fix

### 1. Check Database Status
```bash
curl https://your-railway-app.railway.app/health
```

Expected response:
```json
{
  "status": "healthy",
  "timestamp": "2026-01-30T...",
  "database": {
    "status": "healthy",
    "path": "/tmp/database.db",
    "tables": ["users", "emergencies"],
    "counts": {
      "users": 0,
      "emergencies": 0
    }
  }
}
```

### 2. Manual Database Initialization (if needed)
```bash
curl -X POST https://your-railway-app.railway.app/init-db
```

### 3. Test User Registration
Try creating an account through the web app. The "user table not found" error should be resolved.

## Railway-Specific Considerations

1. **File System Permissions**: Railway containers have limited write access
2. **Temporary Storage**: `/tmp` directory is writable but ephemeral
3. **Database Persistence**: For production, consider using Railway's PostgreSQL addon
4. **Logging**: Enhanced logging helps debug issues in Railway's console

## Next Steps for Production

For a production deployment, consider:
1. Using Railway's PostgreSQL database addon
2. Implementing proper database migrations
3. Adding database backup strategies
4. Using environment variables for database configuration

## Files Modified
- `server/utils/db_utils.py` - Enhanced initialization with fallbacks
- `combined_server.py` - Added health check and manual init endpoints