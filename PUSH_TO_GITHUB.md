# Copy-Paste Commands for GitHub Push

## 🎯 Super Quick Setup (3 Steps)

### Prerequisites
- Download the `snapbuddy` folder to your computer
- Have a GitHub account
- Have git installed on your computer

---

## Step 1: Create GitHub Repository

1. **Go to**: https://github.com/new

2. **Fill in**:
   - Repository name: `snapbuddy`
   - Description: `AI-Powered Aesthetic Photography Matching Platform`
   - Choose: Public or Private
   - **IMPORTANT**: Do NOT check any boxes (no README, no .gitignore, no license)

3. **Click**: "Create repository"

4. **Keep this page open** - you'll need the URL

---

## Step 2: Open Terminal in Your snapbuddy Folder

### On Mac/Linux:
```bash
cd /path/to/snapbuddy
```

### On Windows (Command Prompt):
```cmd
cd C:\path\to\snapbuddy
```

### On Windows (PowerShell):
```powershell
cd C:\path\to\snapbuddy
```

---

## Step 3: Copy & Paste These Commands

### Configure Git (First Time Only)
Replace with your actual name and email:

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### Initialize and Push
**Replace `YOUR_GITHUB_USERNAME` with your actual GitHub username!**

```bash
# Initialize git repository
git init

# Add all files
git add .

# Create first commit
git commit -m "Initial commit: SnapBuddy AI platform"

# Add your GitHub repository as remote (CHANGE YOUR_GITHUB_USERNAME!)
git remote add origin https://github.com/YOUR_GITHUB_USERNAME/snapbuddy.git

# Rename branch to main
git branch -M main

# Push to GitHub
git push -u origin main
```

### When Asked for Credentials:

**Username**: Your GitHub username  
**Password**: Your Personal Access Token (NOT your GitHub password)

---

## 🔑 How to Get Personal Access Token

1. **Go to**: https://github.com/settings/tokens

2. **Click**: "Generate new token" → "Generate new token (classic)"

3. **Fill in**:
   - Note: `SnapBuddy deployment`
   - Expiration: `90 days` (or your choice)
   - Select scopes: Check `repo` (this selects all repo permissions)

4. **Click**: "Generate token"

5. **COPY THE TOKEN** - You won't see it again!

6. **Use this token as your password** when pushing to GitHub

---

## ✅ Success!

After running the commands, your repository should be live at:
```
https://github.com/YOUR_GITHUB_USERNAME/snapbuddy
```

Visit this URL to verify all files are there!

---

## 🚀 Next: Deploy to Render

1. **Go to**: https://dashboard.render.com

2. **Sign up/Login** (can use GitHub to sign in)

3. **Click**: "New +" → "Blueprint"

4. **Connect** your GitHub repository (`snapbuddy`)

5. **Render will detect** `render.yaml` automatically

6. **Set environment variables** (see DEPLOYMENT.md for details):
   - `GEMINI_API_KEY`
   - `GOOGLE_CLOUD_PROJECT`
   - `GCS_BUCKET_NAME`
   - `GOOGLE_MAPS_API_KEY`
   - And others...

7. **Click**: "Apply"

8. **Wait** for deployment (5-10 minutes)

9. **Access** your live app at the Render URL!

---

## 🆘 Troubleshooting

### Error: "Authentication failed"
**Cause**: Used GitHub password instead of Personal Access Token  
**Fix**: Use Personal Access Token (see section above)

### Error: "remote origin already exists"
**Fix**: Run this first:
```bash
git remote remove origin
```
Then run the `git remote add origin` command again

### Error: "repository not found"
**Cause**: Repository doesn't exist on GitHub or wrong URL  
**Fix**: 
1. Verify repository exists at: https://github.com/YOUR_GITHUB_USERNAME/snapbuddy
2. Check username is spelled correctly
3. Make sure you created the repo on GitHub first

### Error: "Permission denied (publickey)"
**Cause**: Trying to use SSH without SSH keys set up  
**Fix**: Use HTTPS URL instead:
```bash
git remote set-url origin https://github.com/YOUR_GITHUB_USERNAME/snapbuddy.git
git push -u origin main
```

---

## 📱 Alternative: Use GitHub Desktop

If command line is difficult, use GitHub Desktop:

1. **Download**: https://desktop.github.com
2. **Install** and sign in
3. **File** → "Add Local Repository"
4. **Select** your `snapbuddy` folder
5. **Initialize** repository if prompted
6. **Publish** to GitHub
7. **Choose** repository name and visibility
8. **Publish**

---

## 🎓 Learning Git

Basic commands for future updates:

```bash
# Check what changed
git status

# Add new/changed files
git add .

# Commit changes
git commit -m "Description of changes"

# Push to GitHub
git push

# Pull latest from GitHub
git pull
```

---

## 💡 Pro Tips

1. **Never commit secrets**: `.env` files are already in `.gitignore`
2. **Commit often**: Small, focused commits are better
3. **Write clear commit messages**: Describe what changed and why
4. **Pull before push**: Avoid conflicts by pulling latest changes first

---

## 📋 Summary Checklist

- [ ] Created GitHub repository
- [ ] Installed git on computer
- [ ] Downloaded snapbuddy folder
- [ ] Opened terminal in snapbuddy folder
- [ ] Configured git name and email
- [ ] Ran git commands to push
- [ ] Used Personal Access Token (not password)
- [ ] Verified files on GitHub
- [ ] Ready to deploy to Render!

---

**Need more help? See GITHUB_SETUP.md for detailed instructions!**
