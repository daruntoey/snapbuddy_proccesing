# 🚀 Quick GitHub Setup Guide

Follow these steps to push SnapBuddy to your GitHub repository.

## Option 1: Automated Setup (Recommended)

### Step 1: Download the Project
Download the entire `snapbuddy` folder to your computer.

### Step 2: Open Terminal
```bash
cd path/to/snapbuddy
```

### Step 3: Run Setup Script
```bash
chmod +x setup_github.sh
./setup_github.sh
```

The script will guide you through:
1. Creating a GitHub repository
2. Initializing Git
3. Committing files
4. Pushing to GitHub

## Option 2: Manual Setup

### Step 1: Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `snapbuddy`
3. Description: `AI-Powered Aesthetic Photography Matching Platform`
4. Choose Public or Private
5. **Do NOT** initialize with README, .gitignore, or license
6. Click "Create repository"

### Step 2: Initialize Git (in your local snapbuddy folder)

```bash
cd snapbuddy

# Initialize git
git init

# Configure git (first time only)
git config user.name "Your Name"
git config user.email "your.email@example.com"

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: SnapBuddy AI platform"
```

### Step 3: Connect to GitHub

Replace `YOUR_USERNAME` with your GitHub username:

```bash
# Add remote repository
git remote add origin https://github.com/YOUR_USERNAME/snapbuddy.git

# Rename branch to main
git branch -M main

# Push to GitHub
git push -u origin main
```

### Step 4: Authenticate

When prompted for credentials:

**Option A: HTTPS (Recommended)**
- Username: Your GitHub username
- Password: Your Personal Access Token (**NOT** your GitHub password)

**Create a Personal Access Token:**
1. Go to https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Select scopes: `repo` (full control)
4. Copy the token and use it as password

**Option B: SSH**

If you have SSH keys set up:
```bash
git remote set-url origin git@github.com:YOUR_USERNAME/snapbuddy.git
git push -u origin main
```

## Verify Success

After pushing, visit:
```
https://github.com/YOUR_USERNAME/snapbuddy
```

You should see all your files!

## Next Steps

### Deploy to Render

1. Go to https://dashboard.render.com
2. Click "New +" → "Blueprint"
3. Connect your GitHub repository
4. Render will detect `render.yaml`
5. Set environment variables (see DEPLOYMENT.md)
6. Click "Apply"

### Local Development

```bash
# Set up environment variables
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env.local

# Edit .env files with your credentials

# Start with Docker
docker-compose up -d

# Access:
# Frontend: http://localhost:3000
# Backend: http://localhost:8000/docs
```

## Troubleshooting

### Authentication Failed

**Problem**: `Authentication failed` when pushing

**Solution**: 
- For HTTPS: Use Personal Access Token, not your password
- Create token: https://github.com/settings/tokens
- Token needs `repo` permission

### Remote Already Exists

**Problem**: `remote origin already exists`

**Solution**:
```bash
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/snapbuddy.git
```

### Permission Denied

**Problem**: `Permission denied (publickey)`

**Solution**:
- Either use HTTPS with Personal Access Token
- Or set up SSH keys: https://docs.github.com/en/authentication/connecting-to-github-with-ssh

### Repository Not Found

**Problem**: `repository not found`

**Solution**:
- Make sure you created the repository on GitHub first
- Check the repository name is correct
- Verify you're using the right username

## File Structure After Push

Your GitHub repository will contain:

```
snapbuddy/
├── backend/              # FastAPI backend
├── frontend/             # Next.js frontend
├── docker-compose.yml    # Local development
├── render.yaml           # Render deployment
├── README.md             # Project overview
├── DEPLOYMENT.md         # Deployment guide
├── API_DOCUMENTATION.md  # API reference
├── PROJECT_OVERVIEW.md   # Executive summary
├── setup_github.sh       # This setup script
└── .gitignore           # Git exclusions
```

## Need Help?

1. **GitHub Issues**: Create an issue in your repository
2. **GitHub Docs**: https://docs.github.com
3. **Render Docs**: https://render.com/docs

## Quick Commands Reference

```bash
# Check git status
git status

# See commit history
git log --oneline

# Push changes after making edits
git add .
git commit -m "Your commit message"
git push

# Pull latest changes
git pull

# Create a new branch
git checkout -b feature-name

# Switch branches
git checkout main
```

---

**Ready to push to GitHub? Run `./setup_github.sh` to get started!**
