# SOC Automation Platform

A comprehensive Security Operations Center (SOC) automation platform built with Django, React, and Celery.

## Overview

The SOC Automation Platform consists of:
- **Backend**: Django REST API with Celery task queue
- **Frontend**: React-based web interface
- **Task Queue**: Celery with Redis broker for async processing
- **Database**: PostgreSQL

## Prerequisites

- Python 3.9+
- Node.js 16+
- PostgreSQL 12+
- Redis 6+

## Quick Start

### 1. Backend Setup

#### Clone and navigate to backend
```bash
cd backend
```

#### Create a Python virtual environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

#### Create `.env` file in the `backend/` directory
```bash
# Database Configuration
DB_ENGINE=django.db.backends.postgresql
DB_NAME=soc_platform
DB_USER=your_postgres_user
DB_PASSWORD=your_postgres_password
DB_HOST=localhost
DB_PORT=5432

# Django Configuration
SECRET_KEY=your-secret-key-here-change-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Celery & Redis Configuration
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
```

#### Install Python dependencies
```bash
pip install -r requirements.txt
```

#### Run database migrations
```bash
python manage.py migrate
```

#### Create superuser (optional)
```bash
python manage.py createsuperuser
```

#### Populate framework data (optional)
```bash
# Populate MITRE ATT&CK framework
python manage.py populate_mitre

# Populate other frameworks
python manage.py populate_killchain
python manage.py populate_diamond
python manage.py populate_stride
python manage.py populate_owasp
```

#### Start the Django development server
```bash
python manage.py runserver
```

The backend API will be available at `http://localhost:8000`

### 2. Redis Setup

#### Start Redis server
```bash
# Windows (if using WSL or installed Redis)
redis-server

# macOS (with Homebrew)
brew services start redis

# Linux
sudo systemctl start redis-server
```

Verify Redis is running:
```bash
redis-cli ping
# Should return: PONG
```

### 3. Celery Setup

#### In a new terminal, activate the virtual environment and start Celery worker
```bash
cd backend
# Activate your venv first
python -m celery -A soc_platform worker -l info
```

#### (Optional) Start Celery Beat for scheduled tasks
```bash
cd backend
# Activate your venv first
python -m celery -A soc_platform beat -l info
```

### 4. Frontend Setup

#### Navigate to frontend directory
```bash
cd frontend
```

#### Install Node dependencies
```bash
npm install
```

#### Start the React development server
```bash
npm start
```

The frontend will be available at `http://localhost:3000`

## Running the Complete Platform

### Terminal 1 - PostgreSQL
```bash
# Start PostgreSQL service (if not already running)
# Windows: Use pgAdmin or Services
# macOS: brew services start postgresql
# Linux: sudo systemctl start postgresql
```

### Terminal 2 - Redis
```bash
redis-server
```

### Terminal 3 - Django Backend
```bash
cd backend
# Activate venv
python manage.py runserver
```

### Terminal 4 - Celery Worker
```bash
cd backend
# Activate venv
python -m celery -A soc_platform worker -l info
```

### Terminal 5 - Celery Beat (optional)
```bash
cd backend
# Activate venv
python -m celery -A soc_platform beat -l info
```

### Terminal 6 - React Frontend
```bash
cd frontend
npm start
```

## Available Endpoints

### Admin Panel
- `http://localhost:8000/admin/` - Django admin interface

### API Documentation
- `http://localhost:8000/api/docs/` - Swagger API documentation

### Frontend
- `http://localhost:3000/` - React frontend

## Database Access

Access the Django shell to query the database:
```bash
cd backend
python manage.py shell
```

## Running Tests

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Tests
```bash
cd frontend
npm test
```

## Configuration

### Environment Variables

Edit the `.env` file in the backend directory to configure:
- Database credentials
- Django secret key
- Debug mode
- Allowed hosts
- Celery broker and result backend URLs

### Django Settings

Edit `backend/soc_platform/settings.py` for advanced Django configuration.

## Troubleshooting

### Port Already in Use
- Django: Change port with `python manage.py runserver 8001`
- React: Change port with `PORT=3001 npm start`
- Redis: Default port is 6379, change with `redis-server --port 6380`

### PostgreSQL Connection Error
- Verify PostgreSQL is running
- Check credentials in `.env` file
- Ensure database exists: `createdb soc_platform`

### Redis Connection Error
- Verify Redis is running: `redis-cli ping`
- Check CELERY_BROKER_URL in `.env`

### Module Not Found
- Ensure virtual environment is activated
- Run `pip install -r requirements.txt` again

## Development Workflow

1. Create a feature branch: `git checkout -b feature/your-feature`
2. Make your changes
3. Run tests to ensure nothing breaks
4. Commit and push your changes
5. Create a pull request

## Project Structure

```
soc-automation-platform/
├── backend/                 # Django backend
│   ├── alerts/             # Alert management
│   ├── analytics/          # Analytics module
│   ├── frameworks/         # Security frameworks (MITRE, OWASP, etc.)
│   ├── incidents/          # Incident management
│   ├── integrations/       # External integrations
│   ├── playbooks/          # Playbook automation
│   ├── soc_platform/       # Django settings
│   └── manage.py
├── frontend/               # React frontend
│   ├── public/
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── api/           # API client
│   │   └── App.js
│   └── package.json
├── playbook_scripts/       # Playbook scripts
│   ├── containment/
│   ├── detection/
│   ├── eradication/
│   ├── investigation/
│   ├── notification/
│   └── recovery/
├── deployment/             # Deployment configurations
├── docs/                   # Documentation
├── data/                   # Data files
└── README.md
```

## GitHub Deployment

### Push to GitHub Repository

#### 1. Initialize Git (if not already done)
```bash
cd soc-automation-platform
git init
```

#### 2. Create `.gitignore`
Create a `.gitignore` file in the root directory to exclude unnecessary files:
```bash
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environments
venv/
ENV/
env/
.venv

# Django
*.log
local_settings.py
db.sqlite3
/media/
/staticfiles/

# Environment variables
.env
.env.local

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# Node
node_modules/
npm-debug.log
build/
dist/

# Celery
celerybeat-schedule

# OS
.DS_Store
Thumbs.db

# Testing
.pytest_cache/
.coverage
htmlcov/
.tox/
```

#### 3. Add Files and Commit
```bash
git add .
git commit -m "Initial commit: SOC Automation Platform setup"
```

#### 4. Create GitHub Repository

1. Go to [GitHub](https://github.com/new)
2. Create a new repository named `soc-automation-platform`
3. Choose your privacy settings (public/private)
4. Click "Create repository"

#### 5. Add Remote and Push
```bash
# Add remote (replace USERNAME with your GitHub username)
git remote add origin https://github.com/USERNAME/soc-automation-platform.git
git branch -M main
git push -u origin main
```

Or if using SSH:
```bash
git remote add origin git@github.com:USERNAME/soc-automation-platform.git
git branch -M main
git push -u origin main
```

### Deploy Frontend to GitHub Pages

GitHub Pages is ideal for static React frontends. Here's how to deploy the frontend:

#### 1. Configure Package.json
Add the homepage field in `frontend/package.json`:
```json
{
  "name": "soc-frontend",
  "version": "0.1.0",
  "homepage": "https://USERNAME.github.io/soc-automation-platform",
  "private": true,
  ...
}
```

#### 2. Install GitHub Pages Package
```bash
cd frontend
npm install --save-dev gh-pages
```

#### 3. Add Deploy Scripts
Update `frontend/package.json` scripts section:
```json
"scripts": {
  "start": "react-scripts start",
  "build": "react-scripts build",
  "test": "react-scripts test",
  "eject": "react-scripts eject",
  "predeploy": "npm run build",
  "deploy": "gh-pages -d build"
}
```

#### 4. Update React Router (if used)
If your app uses React Router, update the router configuration:
```javascript
// In your main routing file
import { BrowserRouter as Router } from 'react-router-dom';

<Router basename="/soc-automation-platform">
  {/* Your routes */}
</Router>
```

#### 5. Build and Deploy
```bash
cd frontend
npm run deploy
```

#### 6. Enable GitHub Pages
1. Go to your GitHub repository
2. Click **Settings** → **Pages**
3. Under "Source", select `gh-pages` branch
4. Click **Save**

Your frontend will be available at: `https://USERNAME.github.io/soc-automation-platform`

### Deploy Backend to Remote Server

GitHub Pages only hosts static content. For the backend, deploy to a hosting service:

#### Option A: Heroku (Easy)
```bash
# Install Heroku CLI
# Create Procfile in root directory
```

Create `Procfile`:
```
web: cd backend && gunicorn soc_platform.wsgi
worker: cd backend && celery -A soc_platform worker
beat: cd backend && celery -A soc_platform beat
```

Create `runtime.txt` in root:
```
python-3.11.8
```

Deploy:
```bash
heroku login
heroku create your-app-name
git push heroku main
```

#### Option B: AWS, DigitalOcean, or Azure (Recommended for production)

**DigitalOcean (simplest):**
1. Create a Droplet (Linux VM)
2. SSH into the server
3. Clone your repo: `git clone https://github.com/USERNAME/soc-automation-platform.git`
4. Follow the Quick Start setup guide
5. Use systemd to run services

**Example systemd service for Django:**

Create `/etc/systemd/system/soc-django.service`:
```ini
[Unit]
Description=SOC Platform Django Service
After=network.target

[Service]
Type=notify
User=ubuntu
WorkingDirectory=/home/ubuntu/soc-automation-platform/backend
ExecStart=/home/ubuntu/soc-automation-platform/backend/venv/bin/gunicorn \
  --workers 3 \
  --bind unix:/tmp/soc-django.sock \
  soc_platform.wsgi

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable soc-django
sudo systemctl start soc-django
```

### Create Documentation Site with GitHub Pages

Deploy documentation to a separate GitHub Pages site:

#### Option: Using MkDocs
```bash
pip install mkdocs mkdocs-material

# Create docs site
mkdocs new docs-site
cd docs-site

# Configure mkdocs.yml
site_name: SOC Automation Platform Docs

# Deploy to GitHub Pages
mkdocs gh-deploy
```

### GitHub Actions for CI/CD

Create `.github/workflows/tests.yml` to automatically run tests:

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:14
        env:
          POSTGRES_DB: soc_platform
          POSTGRES_PASSWORD: postgres
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
      
      redis:
        image: redis:7
        options: >-
          --health-cmd "redis-cli ping"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        cd backend
        pip install -r requirements.txt
    
    - name: Run tests
      env:
        DB_ENGINE: django.db.backends.postgresql
        DB_NAME: soc_platform
        DB_USER: postgres
        DB_PASSWORD: postgres
        DB_HOST: localhost
        SECRET_KEY: test-secret-key
      run: |
        cd backend
        pytest
```

Create `.github/workflows/deploy.yml` for automatic deployment:

```yaml
name: Deploy Frontend

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Node
      uses: actions/setup-node@v3
      with:
        node-version: '18'
    
    - name: Install and build
      run: |
        cd frontend
        npm install
        npm run build
    
    - name: Deploy to GitHub Pages
      uses: peaceiris/actions-gh-pages@v3
      with:
        github_token: ${{ secrets.GITHUB_TOKEN }}
        publish_dir: ./frontend/build
```

### Multi-Page Setup with GitHub Pages

If you want multiple documentation pages:

#### Structure your repository
```
soc-automation-platform/
├── frontend/           # Main app at /
├── docs/               # Documentation at /docs
├── api-docs/           # API docs at /api-docs
└── wiki/               # Wiki at /wiki
```

#### Deploy each to separate branches
```bash
# Frontend (main branch) → GitHub Pages root
npm run deploy

# Docs (docs branch)
# Push docs to gh-pages branch with docs/ subfolder
git subtree push --prefix docs origin gh-pages
```

#### Configure custom domain (optional)
1. Create `CNAME` file in repository root with your domain
2. Update DNS records at your registrar
3. Enable in GitHub Pages settings

### Useful Commands

```bash
# View git status
git status

# Check remotes
git remote -v

# Update local repo
git pull origin main

# Undo last commit (keep changes)
git reset --soft HEAD~1

# View commit history
git log --oneline

# Create a new branch
git checkout -b feature/new-feature

# Merge branches
git checkout main
git merge feature/new-feature
```

## Support & Documentation

For more information, check the `/docs` directory or contact the development team.

