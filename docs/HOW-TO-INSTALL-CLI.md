# KardoCore CLI Installation & Usage Guide

Complete guide for installing and using the KardoCore Command Line Interface (CLI).

---

## 📋 Table of Contents

1. [CLI Installation](#cli-installation)
2. [CLI Commands Overview](#cli-commands-overview)
3. [Project Management](#project-management)
4. [Theme Management](#theme-management)
5. [Development Server](#development-server)
6. [Database Management](#database-management)
7. [User Management](#user-management)
8. [Build & Deployment](#build--deployment)
9. [Advanced Usage](#advanced-usage)

---

## CLI Installation

The KardoCore CLI is automatically installed when you install KardoCore.

### Install from PyPI

```bash
# Install KardoCore (includes CLI)
pip install kardocore

# Verify installation
kardo --version
```

### Install from GitHub

```bash
# Stable version (v0.0.9)
pip install git+https://github.com/webcien/Kardo.git@v0.0.9

# Development version (main)
pip install git+https://github.com/webcien/Kardo.git@main

# Verify installation
kardo --version
```

### Global Installation

```bash
# Install globally with pipx (recommended)
pipx install kardocore

# Verify
kardo --version
```

### Development Installation

```bash
# Clone repository
git clone https://github.com/webcien/Kardo.git
cd Kardo

# Install in development mode
pip install -e .

# Verify
kardo --version
```

---

## CLI Commands Overview

### General Commands

```bash
# Show version
kardo --version

# Show help
kardo --help

# Show help for specific command
kardo <command> --help
```

### Available Commands

| Command | Description |
|---------|-------------|
| `kardo init` | Initialize new project |
| `kardo serve` | Start development server |
| `kardo theme` | Manage themes |
| `kardo migrate` | Database migrations |
| `kardo user` | User management |
| `kardo build` | Build for production |
| `kardo deploy` | Deploy application |
| `kardo shell` | Interactive shell |

---

## Project Management

### Initialize New Project

```bash
# Create new project (interactive)
kardo init

# Create with specific mode
kardo init --mode=core          # Core only (API)
kardo init --mode=admin         # Core + Admin
kardo init --mode=full          # Full CMS
kardo init --mode=theme         # Theme only

# Create with project name
kardo init --name="My CMS" --mode=full

# Create in specific directory
kardo init --path=/path/to/project --mode=full
```

### Example: Initialize Full CMS Project

```bash
$ kardo init --mode=full --name="My Blog"

🎨 KardoCore Project Initializer

Project Name: My Blog
Mode: Full CMS (Core + Admin + Theme)
Directory: /current/directory/my-blog

Creating project structure...
✅ Created app.py
✅ Created config.py
✅ Created models/
✅ Created routes/
✅ Created templates/
✅ Created static/
✅ Created admin/

Installing dependencies...
✅ kardocore[full] installed

Initializing database...
✅ Database created

Creating admin user...
Username: admin
Email: admin@example.com
Password: ********
✅ Admin user created

🎉 Project initialized successfully!

Next steps:
  cd my-blog
  kardo serve
  Visit http://localhost:8000
  Admin: http://localhost:8000/admin
```

---

## Theme Management

### List Available Themes

```bash
# List all available themes
kardo theme list --available

# List installed themes
kardo theme list

# List by category
kardo theme list --category=salud-bienestar
```

### Install Theme

```bash
# Install from registry
kardo theme install wellness-clinic

# Install specific version
kardo theme install wellness-clinic@1.0.0

# Install from GitHub
kardo theme install https://github.com/user/theme-repo

# Install from local directory
kardo theme install /path/to/theme
```

### Search Themes

```bash
# Search by name
kardo theme search health

# Search by category
kardo theme search --category=salud-bienestar

# Search by tag
kardo theme search --tag=medical
```

### Theme Information

```bash
# View theme details
kardo theme info wellness-clinic

# View theme README
kardo theme readme wellness-clinic
```

### Activate Theme

```bash
# Activate installed theme
kardo theme activate wellness-clinic

# Activate with preview
kardo theme activate wellness-clinic --preview
```

### Customize Theme

```bash
# Create customizable copy
kardo theme customize wellness-clinic

# This creates:
# themes/wellness-clinic-custom/
#   ├── templates/
#   ├── static/
#   └── theme.yaml
```

### Uninstall Theme

```bash
# Uninstall theme
kardo theme uninstall wellness-clinic

# Force uninstall (skip confirmation)
kardo theme uninstall wellness-clinic --force
```

---

## Development Server

### Start Server

```bash
# Start development server (default: localhost:8000)
kardo serve

# Specify host and port
kardo serve --host=0.0.0.0 --port=8080

# Enable auto-reload
kardo serve --reload

# Enable debug mode
kardo serve --debug

# Specify workers
kardo serve --workers=4
```

### Example Output

```bash
$ kardo serve

🚀 KardoCore Development Server

Application: My CMS
Mode: Full CMS
Host: localhost
Port: 8000
Debug: True
Auto-reload: True

Starting server...
✅ Server started successfully

URLs:
  Frontend: http://localhost:8000
  Admin:    http://localhost:8000/admin
  API:      http://localhost:8000/api

Press Ctrl+C to stop
```

### Production Server

```bash
# Start with production settings
kardo serve --production

# This is equivalent to:
kardo serve --host=0.0.0.0 --port=8000 --workers=4 --no-reload --no-debug
```

---

## Database Management

### Initialize Database

```bash
# Create database
kardo db init

# Create with specific database
kardo db init --database=postgresql://user:pass@localhost/dbname
```

### Migrations

```bash
# Create migration
kardo migrate create "Add user table"

# Apply migrations
kardo migrate up

# Rollback migration
kardo migrate down

# Show migration status
kardo migrate status

# Reset database (WARNING: deletes all data)
kardo migrate reset
```

### Database Shell

```bash
# Open database shell
kardo db shell

# Execute SQL query
kardo db query "SELECT * FROM users"

# Dump database
kardo db dump > backup.sql

# Restore database
kardo db restore < backup.sql
```

---

## User Management

### Create User

```bash
# Create user (interactive)
kardo user create

# Create with parameters
kardo user create --username=john --email=john@example.com --password=secret

# Create admin user
kardo user create --username=admin --admin

# Create with specific role
kardo user create --username=editor --role=editor
```

### List Users

```bash
# List all users
kardo user list

# List with details
kardo user list --verbose

# Filter by role
kardo user list --role=admin
```

### Update User

```bash
# Change password
kardo user password john

# Make user admin
kardo user promote john

# Remove admin privileges
kardo user demote john

# Deactivate user
kardo user deactivate john

# Activate user
kardo user activate john
```

### Delete User

```bash
# Delete user
kardo user delete john

# Force delete (skip confirmation)
kardo user delete john --force
```

---

## Build & Deployment

### Build for Production

```bash
# Build project
kardo build

# Build with specific output directory
kardo build --output=dist/

# Build with optimization
kardo build --optimize

# Build and minify
kardo build --minify
```

### Deploy

```bash
# Deploy to production
kardo deploy

# Deploy to specific platform
kardo deploy --platform=heroku
kardo deploy --platform=vercel
kardo deploy --platform=aws

# Deploy with custom config
kardo deploy --config=deploy.yaml
```

### Export

```bash
# Export as static site
kardo export

# Export specific pages
kardo export --pages=index,about,contact

# Export with custom output
kardo export --output=static/
```

---

## Advanced Usage

### Interactive Shell

```bash
# Start interactive Python shell with app context
kardo shell

# Example session:
$ kardo shell
>>> from models import User
>>> users = User.objects.all()
>>> print(users)
```

### Run Scripts

```bash
# Run Python script with app context
kardo run script.py

# Run with arguments
kardo run script.py --arg1=value1 --arg2=value2
```

### Configuration

```bash
# Show current configuration
kardo config show

# Set configuration value
kardo config set database.url postgresql://localhost/mydb

# Get configuration value
kardo config get database.url

# Edit configuration file
kardo config edit
```

### Logs

```bash
# View logs
kardo logs

# Follow logs (tail -f)
kardo logs --follow

# Filter by level
kardo logs --level=error

# Export logs
kardo logs --export=logs.txt
```

### Testing

```bash
# Run tests
kardo test

# Run specific test file
kardo test tests/test_models.py

# Run with coverage
kardo test --coverage

# Run in watch mode
kardo test --watch
```

### Code Generation

```bash
# Generate model
kardo generate model User

# Generate route
kardo generate route /api/users

# Generate admin
kardo generate admin User

# Generate CRUD
kardo generate crud Post
```

---

## CLI Configuration

### Configuration File

Create `.kardorc` in your project root:

```yaml
# .kardorc
project:
  name: "My CMS"
  mode: "full"

server:
  host: "localhost"
  port: 8000
  reload: true
  debug: true

database:
  url: "sqlite:///kardo.db"
  pool_size: 10

theme:
  active: "wellness-clinic"
  custom_dir: "themes/"

admin:
  base_url: "/admin"
  title: "My CMS Admin"

logging:
  level: "INFO"
  file: "kardo.log"
```

### Environment Variables

```bash
# Set via environment variables
export KARDO_DEBUG=true
export KARDO_DATABASE_URL=postgresql://localhost/mydb
export KARDO_SECRET_KEY=my-secret-key

# Or use .env file
KARDO_DEBUG=true
KARDO_DATABASE_URL=postgresql://localhost/mydb
KARDO_SECRET_KEY=my-secret-key
```

---

## Complete Workflow Example

### 1. Create New Project

```bash
# Initialize full CMS project
kardo init --mode=full --name="My Blog"
cd my-blog
```

### 2. Install Theme

```bash
# Install a blog theme
kardo theme install blog-minimal
kardo theme activate blog-minimal
```

### 3. Create Admin User

```bash
# Create admin user
kardo user create --username=admin --admin
```

### 4. Start Development Server

```bash
# Start server with auto-reload
kardo serve --reload
```

### 5. Develop Your Site

```bash
# Generate models
kardo generate model Post
kardo generate model Category

# Run migrations
kardo migrate create "Add Post and Category models"
kardo migrate up

# Create some content via admin panel
# Visit http://localhost:8000/admin
```

### 6. Build for Production

```bash
# Build optimized version
kardo build --optimize --minify

# Test production build
kardo serve --production
```

### 7. Deploy

```bash
# Deploy to Heroku
kardo deploy --platform=heroku

# Or export as static site
kardo export --output=dist/
```

---

## Troubleshooting

### Command Not Found

```bash
# If 'kardo' command not found
which kardo

# Add to PATH or use full path
python -m kardocore.cli <command>

# Or reinstall
pip install --force-reinstall kardocore
```

### Permission Errors

```bash
# Use virtual environment
python -m venv venv
source venv/bin/activate
pip install kardocore
```

### Database Errors

```bash
# Reset database
kardo migrate reset

# Reinitialize
kardo db init
```

---

## Getting Help

```bash
# General help
kardo --help

# Command-specific help
kardo init --help
kardo theme --help
kardo serve --help

# Online documentation
# https://kardo.dev/docs/cli

# Community support
# Discord: https://discord.gg/kardo
# GitHub: https://github.com/webcien/Kardo/issues
```

---

**Happy coding with KardoCore CLI! 🚀**

