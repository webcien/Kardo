# KardoCore CLI Documentation

Complete guide to the **kardo** command-line interface.

---

## Installation

Install KardoCore with CLI support:

```bash
# From PyPI (when published)
pip install kardocore

# From GitHub (current)
pip install git+https://github.com/webcien/Kardo.git@v0.0.9

# For development
git clone https://github.com/webcien/Kardo.git
cd Kardo
pip install -e .
```

Verify installation:

```bash
kardo --version
# Output: KardoCore v0.2.0
```

---

## Commands Overview

| Command | Description |
|---------|-------------|
| `kardo init` | Initialize a new KardoCore project |
| `kardo serve` | Start development server |
| `kardo theme` | Manage themes (install, list, search) |
| `kardo user` | Manage users (create, list, delete) |
| `kardo migrate` | Run database migrations |
| `kardo build` | Build project for production |

---

## Command Reference

### `kardo init` - Initialize Project

Create a new KardoCore project with complete structure.

**Usage:**

```bash
kardo init <project-name> [options]
```

**Options:**

- `--template <name>` - Project template (default, blog, cms, api)
- `--no-git` - Don't initialize git repository

**Examples:**

```bash
# Create default project
kardo init my-blog

# Create with specific template
kardo init my-cms --template cms

# Create without git
kardo init my-api --template api --no-git
```

**Generated Structure:**

```
my-blog/
├── app/
│   ├── models/       # Database models
│   ├── views/        # View functions
│   ├── templates/    # HTML templates
│   └── static/       # Static files (CSS, JS)
├── config/
│   └── config.py     # Configuration
├── tests/            # Tests
├── main.py           # Application entry point
├── requirements.txt  # Dependencies
├── .gitignore
└── README.md
```

---

### `kardo serve` - Development Server

Start a development server with auto-reload.

**Usage:**

```bash
kardo serve [options]
```

**Options:**

- `--host <host>` - Host to bind to (default: 0.0.0.0)
- `--port <port>` - Port to bind to (default: 8000)
- `--reload` - Enable auto-reload on code changes

**Examples:**

```bash
# Start server on default port
kardo serve

# Custom host and port
kardo serve --host localhost --port 3000

# With auto-reload
kardo serve --reload
```

**Output:**

```
ℹ️  Starting development server...
ℹ️  Server running at http://0.0.0.0:8000
ℹ️  Press Ctrl+C to stop
```

---

### `kardo theme` - Theme Management

Manage themes: install, list, search, and uninstall.

**Usage:**

```bash
kardo theme <subcommand> [options]
```

**Subcommands:**

#### `theme install` - Install a theme

```bash
kardo theme install <theme-name>
```

**Examples:**

```bash
# Install from registry
kardo theme install wellness-clinic

# Install from GitHub
kardo theme install https://github.com/user/theme.git

# Install from local directory
kardo theme install ./my-theme
```

#### `theme list` - List installed themes

```bash
kardo theme list
```

**Output:**

```
ℹ️  Installed themes:
  - default
  - wellness-clinic
  - yoga-studio
```

#### `theme search` - Search themes

```bash
kardo theme search <query>
```

**Examples:**

```bash
# Search by keyword
kardo theme search health

# Search by category
kardo theme search category:business
```

#### `theme info` - Show theme information

```bash
kardo theme info <theme-name>
```

**Output:**

```
ℹ️  Theme: wellness-clinic
  Name: Wellness Clinic
  Version: 1.0.0
  Author: WebCien
  Category: Health & Wellness
  Description: Professional theme for health clinics
```

#### `theme uninstall` - Uninstall a theme

```bash
kardo theme uninstall <theme-name>
```

---

### `kardo user` - User Management

Manage users: create, list, delete, and change passwords.

**Usage:**

```bash
kardo user <subcommand> [options]
```

**Subcommands:**

#### `user create` - Create a new user

```bash
kardo user create <email> <username> [options]
```

**Options:**

- `--password <password>` - Password (will prompt if not provided)
- `--role <role>` - User role: admin, author, user, guest (default: user)

**Examples:**

```bash
# Create admin user (will prompt for password)
kardo user create admin@example.com admin --role admin

# Create user with password
kardo user create author@example.com john --password secret123 --role author
```

**Output:**

```
✅ User created: admin (admin)
ℹ️    ID: 1
ℹ️    Email: admin@example.com
```

#### `user list` - List all users

```bash
kardo user list [options]
```

**Options:**

- `--role <role>` - Filter by role

**Examples:**

```bash
# List all users
kardo user list

# List only admins
kardo user list --role admin
```

**Output:**

```
ℹ️  
Users (3):
----------------------------------------------------------------------
ID    Email                          Username             Role       Active
----------------------------------------------------------------------
1     admin@example.com              admin                admin      ✓
2     author@example.com             john                 author     ✓
3     user@example.com               jane                 user       ✓
```

#### `user delete` - Delete a user

```bash
kardo user delete <email>
```

**Example:**

```bash
kardo user delete user@example.com
```

**Output:**

```
⚠️  Are you sure you want to delete user 'jane' (user@example.com)? [y/N] y
✅ User deleted: user@example.com
```

#### `user passwd` - Change user password

```bash
kardo user passwd <email> [options]
```

**Options:**

- `--password <password>` - New password (will prompt if not provided)

**Example:**

```bash
kardo user passwd admin@example.com
```

**Output:**

```
Current password: ********
New password: ********
Confirm new password: ********
✅ Password changed for: admin@example.com
```

---

### `kardo migrate` - Database Migrations

Manage database migrations: create, apply, and rollback.

**Usage:**

```bash
kardo migrate <subcommand> [options]
```

**Subcommands:**

#### `migrate up` - Run pending migrations

```bash
kardo migrate up
```

**Output:**

```
ℹ️  Running pending migrations...
✅ All migrations applied
```

#### `migrate down` - Rollback migrations

```bash
kardo migrate down [--steps N]
```

**Options:**

- `--steps <N>` - Number of migrations to rollback (default: 1)

**Examples:**

```bash
# Rollback last migration
kardo migrate down

# Rollback 3 migrations
kardo migrate down --steps 3
```

#### `migrate status` - Show migration status

```bash
kardo migrate status
```

**Output:**

```
ℹ️  Migration status:
  [✓] 001_initial_schema
  [✓] 002_add_users_table
  [ ] 003_add_posts_table
```

#### `migrate create` - Create a new migration

```bash
kardo migrate create <migration-name>
```

**Example:**

```bash
kardo migrate create add_comments_table
```

**Output:**

```
ℹ️  Creating migration: add_comments_table
✅ Migration created: migrations/003_add_comments_table.py
```

---

### `kardo build` - Build for Production

Build project for production deployment.

**Usage:**

```bash
kardo build [options]
```

**Options:**

- `--output <dir>` - Output directory (default: dist)
- `--minify` - Minify CSS and JS
- `--optimize` - Optimize images

**Examples:**

```bash
# Basic build
kardo build

# Build with minification
kardo build --minify

# Build with all optimizations
kardo build --minify --optimize --output production
```

**Output:**

```
ℹ️  Building project for production...
ℹ️  Output directory: dist
ℹ️  1. Compiling templates...
ℹ️  2. Processing static files...
ℹ️  3. Minifying CSS and JS...
ℹ️  4. Optimizing images...
✅ Build complete! Output: dist

To deploy:
  1. Copy dist/ to your server
  2. Set environment variables
  3. Run: python main.py
```

---

## Complete Workflow Example

Here's a complete workflow from project creation to deployment:

```bash
# 1. Create new project
kardo init my-blog
cd my-blog

# 2. Install dependencies
pip install -r requirements.txt

# 3. Initialize database
python main.py

# 4. Create admin user
kardo user create admin@example.com admin --role admin

# 5. Install a theme
kardo theme install wellness-clinic

# 6. Start development server
kardo serve --reload

# 7. Build for production
kardo build --minify --optimize

# 8. Deploy
# Copy dist/ to server and run
```

---

## Configuration

The CLI reads configuration from:

1. **Environment variables**
2. **config/config.py** in project directory
3. **Command-line arguments** (highest priority)

### Environment Variables

```bash
# Database
export DATABASE_URL="postgresql://user:pass@localhost/db"

# Security
export SECRET_KEY="your-secret-key-here"
export JWT_EXPIRES_IN=3600

# Server
export HOST="0.0.0.0"
export PORT=8000
export DEBUG=true

# Environment
export ENVIRONMENT="production"
```

### Config File

```python
# config/config.py

import os

class Config:
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///app.db")
    SECRET_KEY = os.getenv("SECRET_KEY", "change-this")
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", 8000))
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
```

---

## Troubleshooting

### Command not found: kardo

**Solution:**

```bash
# Reinstall with CLI support
pip install --force-reinstall kardocore

# Or install in editable mode
pip install -e .
```

### Database not found

**Error:**

```
❌ Database not found. Make sure you're in a KardoCore project directory.
```

**Solution:**

Make sure you're in a KardoCore project directory (created with `kardo init`) and that `app.db` exists.

```bash
# Initialize database
python main.py
```

### Permission denied

**Error:**

```
❌ Permission denied: /usr/local/bin/kardo
```

**Solution:**

Install in user directory:

```bash
pip install --user kardocore
```

---

## Advanced Usage

### Custom Commands

You can extend the CLI with custom commands:

```python
# my_commands/hello.py

from kardocore.cli.commands.base import BaseCommand

class HelloCommand(BaseCommand):
    name = "hello"
    description = "Say hello"
    
    def _add_arguments(self, parser):
        parser.add_argument("name", help="Name to greet")
    
    async def execute(self, args):
        parsed = self.parse_args(args)
        self.print_success(f"Hello, {parsed.name}!")
        return 0
```

Register in `kardocore/cli/main.py`:

```python
from my_commands.hello import HelloCommand

class KardoCLI:
    def __init__(self):
        self.commands = {
            # ... existing commands
            "hello": HelloCommand(),
        }
```

---

## See Also

- [Database Documentation](DATABASE.md)
- [Authentication Documentation](AUTHENTICATION.md)
- [Theme Development Guide](../KardoTemplates/README.md)
- [API Reference](../README.md)

---

## Support

- **Documentation**: https://github.com/webcien/Kardo
- **Issues**: https://github.com/webcien/Kardo/issues
- **Discussions**: https://github.com/webcien/Kardo/discussions

