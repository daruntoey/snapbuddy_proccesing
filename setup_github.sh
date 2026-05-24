#!/bin/bash

# SnapBuddy - GitHub Push Setup Script
# This script helps you push the SnapBuddy project to your GitHub repository

set -e  # Exit on error

echo "=========================================="
echo "   SnapBuddy - GitHub Setup Script"
echo "=========================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

# Check if git is installed
if ! command -v git &> /dev/null; then
    print_error "Git is not installed. Please install git first."
    exit 1
fi

print_success "Git is installed"

# Get GitHub username
echo ""
echo "Enter your GitHub username:"
read GITHUB_USERNAME

if [ -z "$GITHUB_USERNAME" ]; then
    print_error "GitHub username cannot be empty"
    exit 1
fi

# Get repository name
echo ""
echo "Enter repository name (default: snapbuddy):"
read REPO_NAME
REPO_NAME=${REPO_NAME:-snapbuddy}

echo ""
echo "=========================================="
echo "Setup Summary:"
echo "=========================================="
echo "GitHub Username: $GITHUB_USERNAME"
echo "Repository Name: $REPO_NAME"
echo "Repository URL: https://github.com/$GITHUB_USERNAME/$REPO_NAME"
echo ""

# Confirm
echo "Is this correct? (y/n)"
read CONFIRM

if [ "$CONFIRM" != "y" ] && [ "$CONFIRM" != "Y" ]; then
    print_warning "Setup cancelled"
    exit 0
fi

echo ""
echo "=========================================="
echo "Step 1: Creating GitHub Repository"
echo "=========================================="
echo ""

print_warning "Please create a new repository on GitHub:"
echo ""
echo "1. Go to: https://github.com/new"
echo "2. Repository name: $REPO_NAME"
echo "3. Description: AI-Powered Aesthetic Photography Matching Platform"
echo "4. Choose: Public or Private"
echo "5. Do NOT initialize with README, .gitignore, or license"
echo "6. Click 'Create repository'"
echo ""
echo "Press ENTER when you've created the repository..."
read

print_success "Repository created on GitHub"

echo ""
echo "=========================================="
echo "Step 2: Initializing Local Git Repository"
echo "=========================================="
echo ""

# Initialize git if not already
if [ ! -d ".git" ]; then
    git init
    print_success "Git repository initialized"
else
    print_warning "Git repository already initialized"
fi

# Configure git user if not set
if [ -z "$(git config user.name)" ]; then
    echo "Enter your name for Git commits:"
    read GIT_NAME
    git config user.name "$GIT_NAME"
    print_success "Git user name set"
fi

if [ -z "$(git config user.email)" ]; then
    echo "Enter your email for Git commits:"
    read GIT_EMAIL
    git config user.email "$GIT_EMAIL"
    print_success "Git user email set"
fi

echo ""
echo "=========================================="
echo "Step 3: Adding Files to Git"
echo "=========================================="
echo ""

# Remove build scripts (not needed in repo)
rm -f create_*.sh
print_success "Cleaned up build scripts"

# Add all files
git add .
print_success "Files staged for commit"

# Create initial commit
git commit -m "Initial commit: SnapBuddy AI-powered photography matching platform

Complete production-ready platform including:
- FastAPI backend with 8 AI services
- Next.js 14 frontend with TypeScript
- PostgreSQL + Qdrant + Redis integration
- Google Cloud (GCS, Gemini API, Maps API)
- Docker & Render deployment ready
- Comprehensive documentation

Tech Stack:
- Backend: FastAPI, Python 3.11, SQLAlchemy, Qdrant
- Frontend: Next.js 14, TypeScript, TailwindCSS, ShadCN UI
- AI: Google Gemini, CLIP, Sentence Transformers
- Cloud: Render, Google Cloud Platform
- Database: PostgreSQL with pgvector

Features:
- AI-powered aesthetic matching
- Vector similarity search
- Multi-factor ranking algorithm
- Natural language explanations
- Image & text embedding extraction
- Photographer portfolio management
- Booking system
- JWT authentication

Ready to deploy to Render with one-click setup via render.yaml"

print_success "Initial commit created"

echo ""
echo "=========================================="
echo "Step 4: Adding Remote Repository"
echo "=========================================="
echo ""

# Remove existing remote if exists
git remote remove origin 2>/dev/null || true

# Add remote
git remote add origin "https://github.com/$GITHUB_USERNAME/$REPO_NAME.git"
print_success "Remote repository added"

# Rename branch to main
git branch -M main
print_success "Branch renamed to main"

echo ""
echo "=========================================="
echo "Step 5: Pushing to GitHub"
echo "=========================================="
echo ""

echo "Choose authentication method:"
echo "1. HTTPS (you'll need to enter username and password/token)"
echo "2. SSH (requires SSH key setup)"
echo "Enter choice (1 or 2):"
read AUTH_METHOD

if [ "$AUTH_METHOD" = "2" ]; then
    # Update remote to SSH
    git remote set-url origin "git@github.com:$GITHUB_USERNAME/$REPO_NAME.git"
    print_success "Remote URL updated to SSH"
fi

echo ""
print_warning "Pushing to GitHub..."
echo ""

if [ "$AUTH_METHOD" = "1" ]; then
    echo "Note: If using Personal Access Token:"
    echo "- Username: your GitHub username"
    echo "- Password: your Personal Access Token (not your GitHub password)"
    echo "- Create token at: https://github.com/settings/tokens"
    echo ""
fi

# Push to GitHub
if git push -u origin main; then
    echo ""
    print_success "Successfully pushed to GitHub!"
    echo ""
    echo "=========================================="
    echo "           🎉 SUCCESS! 🎉"
    echo "=========================================="
    echo ""
    echo "Your repository is now live at:"
    echo "https://github.com/$GITHUB_USERNAME/$REPO_NAME"
    echo ""
    echo "Next Steps:"
    echo "1. Visit your repository on GitHub"
    echo "2. Review the README.md"
    echo "3. Follow DEPLOYMENT.md to deploy to Render"
    echo ""
    echo "Quick Deploy to Render:"
    echo "1. Go to https://dashboard.render.com"
    echo "2. New Blueprint"
    echo "3. Connect your GitHub repo"
    echo "4. Set environment variables"
    echo "5. Deploy!"
    echo ""
else
    echo ""
    print_error "Failed to push to GitHub"
    echo ""
    echo "Common issues:"
    echo "1. Authentication failed:"
    echo "   - For HTTPS: Use Personal Access Token, not password"
    echo "   - Create token: https://github.com/settings/tokens"
    echo ""
    echo "2. Repository doesn't exist:"
    echo "   - Make sure you created it on GitHub first"
    echo ""
    echo "3. Permission denied:"
    echo "   - Check repository permissions"
    echo "   - Verify username is correct"
    echo ""
    echo "Try again with: ./setup_github.sh"
    exit 1
fi

echo "=========================================="
echo "Optional: Create GitHub Releases"
echo "=========================================="
echo ""
echo "Create a release? (y/n)"
read CREATE_RELEASE

if [ "$CREATE_RELEASE" = "y" ] || [ "$CREATE_RELEASE" = "Y" ]; then
    # Tag the release
    git tag -a v1.0.0 -m "SnapBuddy v1.0.0 - Initial Release

Production-ready AI photography matching platform.

Features:
- Complete FastAPI backend with 8 AI services
- Next.js 14 frontend with TypeScript
- Vector similarity matching with Qdrant
- Google Gemini API integration
- Multi-factor ranking algorithm
- Comprehensive documentation
- One-click Render deployment

Estimated cost: ~$70/month for MVP scale"

    git push origin v1.0.0
    
    print_success "Release v1.0.0 created"
    echo ""
    echo "View your release at:"
    echo "https://github.com/$GITHUB_USERNAME/$REPO_NAME/releases"
fi

echo ""
print_success "Setup complete!"
