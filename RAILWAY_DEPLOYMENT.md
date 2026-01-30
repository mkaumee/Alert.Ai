# Railway Deployment Guide for AlertAI

## Prerequisites
- GitHub repository with your AlertAI code
- Railway account (free tier available)

## Deployment Steps

### 1. Connect to Railway
1. Go to [Railway.app](https://railway.app)
2. Sign up/login with GitHub
3. Click "New Project"
4. Select "Deploy from GitHub repo"
5. Choose your `Alert-Ai` repository

### 2. Configure Environment Variables
In Railway dashboard, go to Variables tab and add:

```
GEMINI_API_KEY=your_actual_gemini_api_key_here
TWILIO_ACCOUNT_SID=your_actual_twilio_sid_here
TWILIO_AUTH_TOKEN=your_actual_twilio_token_here
TWILIO_WHATSAPP_FROM=whatsapp:+14155238886
EMERGENCY_CONTACT_1=whatsapp:+1234567890
FLASK_ENV=production
```

### 3. Deploy
- Railway will automatically detect Python and install dependencies
- It will use the `Procfile` to start your app
- Deployment typically takes 2-3 minutes

### 4. Access Your App
- Railway will provide a URL like: `https://your-app-name.railway.app`
- Your AlertAI system will be fully functional at this URL

## What's Included in Railway Deployment

✅ **Complete AlertAI System**
- Web dashboard at root URL
- API endpoints at `/api/`
- CPR monitor at `/cpr-monitor`
- All emergency agents integrated

✅ **Persistent Storage**
- SQLite database persists between deployments
- Fire detection models and datasets included

✅ **Environment Configuration**
- Production-ready Flask configuration
- Dynamic port assignment
- Health check endpoint

✅ **Security**
- Environment variables for sensitive data
- No API keys in code repository

## Testing Your Deployment

1. **Health Check**: Visit `https://your-app.railway.app/health`
2. **Web App**: Visit `https://your-app.railway.app`
3. **API Test**: Use simulation buttons in web app
4. **CPR Monitor**: Visit `https://your-app.railway.app/cpr-monitor`

## Troubleshooting

### Build Fails
- Check Railway logs for Python dependency issues
- Ensure all required files are in GitHub repository

### App Won't Start
- Verify environment variables are set correctly
- Check Railway logs for startup errors

### Database Issues
- Railway provides persistent storage for SQLite
- Database will be created automatically on first run

### Large Files (LFS)
- Railway supports Git LFS
- YOLO models and datasets will be available

## Monitoring
- Railway provides built-in metrics and logs
- Monitor CPU, memory, and request metrics
- View real-time logs for debugging

## Scaling
- Railway free tier: 500 hours/month
- Upgrade to Pro for unlimited usage
- Automatic scaling based on traffic

## Cost
- **Free Tier**: $0/month (500 hours)
- **Pro Tier**: $5/month (unlimited)
- **Team Tier**: $20/month (team features)

Your AlertAI system is now production-ready on Railway! 🚀