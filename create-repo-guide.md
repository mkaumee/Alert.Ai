# Create Repository for AlertAI System

## GitHub (Recommended)

### Step 1: Create Repository on GitHub
1. Go to [GitHub.com](https://github.com)
2. Click the "+" icon → "New repository"
3. Repository name: `alertai-system` (or your preferred name)
4. Description: `AI-Powered Emergency Response System with Real-time Detection and Guidance`
5. **Important**: 
   - ✅ Make it **Public** or **Private** (your choice)
   - ❌ **DO NOT** initialize with README, .gitignore, or license (we already have these)
   - ✅ **Enable Git LFS** if the option is available
6. Click "Create repository"

### Step 2: Copy Repository URL
After creation, copy the repository URL from the page:
- HTTPS: `https://github.com/yourusername/alertai-system.git`
- SSH: `git@github.com:yourusername/alertai-system.git`

## GitLab

### Step 1: Create Repository on GitLab
1. Go to [GitLab.com](https://gitlab.com)
2. Click "New project" → "Create blank project"
3. Project name: `alertai-system`
4. Description: `AI-Powered Emergency Response System`
5. **Important**:
   - ❌ **DO NOT** initialize with README
   - Set visibility level (Private/Internal/Public)
6. Click "Create project"

### Step 2: Copy Repository URL
- HTTPS: `https://gitlab.com/yourusername/alertai-system.git`
- SSH: `git@gitlab.com:yourusername/alertai-system.git`

## Bitbucket

### Step 1: Create Repository on Bitbucket
1. Go to [Bitbucket.org](https://bitbucket.org)
2. Click "Create" → "Repository"
3. Repository name: `alertai-system`
4. Description: `AI-Powered Emergency Response System`
5. **Important**:
   - ❌ **DO NOT** initialize with README
   - Set access level (Private/Public)
6. Click "Create repository"

## After Creating Repository

Once you have your repository URL, run these commands:

```bash
# Add your remote repository (replace with your actual URL)
git remote add origin <your-repository-url>

# Push everything to your repository
git push -u origin master
```

## Repository Settings for LFS

### GitHub
- LFS is automatically supported
- Free tier: 1GB storage, 1GB bandwidth/month
- Paid plans available for more storage

### GitLab
- LFS is automatically supported  
- Free tier: 10GB storage
- Unlimited bandwidth on all plans

### Bitbucket
- LFS is automatically supported
- Free tier: 1GB storage, 1GB bandwidth/month
- Paid plans available for more storage

## Important Notes

⚠️ **LFS Storage**: Your project includes large files (models, images, virtual environment)
- Total LFS size is approximately 200-500MB
- Monitor your LFS usage on your Git provider
- Consider cleaning up unnecessary large files if needed

✅ **What's Included**: Your repository will contain the complete AlertAI system:
- All source code and configuration
- Pre-trained YOLO fire detection model
- Complete Python virtual environment
- Fire detection training dataset
- Database files with sample data
- Comprehensive documentation

## Verification

After pushing, verify your repository:
1. **Check web interface**: All files should be visible
2. **LFS files**: Large files show "Git LFS" badge
3. **README**: Should display the AlertAI documentation
4. **File count**: Should show all your project files

## Next Steps

1. **Create repository** using the guide above
2. **Copy the repository URL**
3. **Run the push commands** from `push-to-repo.md`
4. **Verify everything uploaded** correctly
5. **Share with team** if needed