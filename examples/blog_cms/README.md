# Blog CMS Example

Complete blog CMS example using KardoCore with Database and Authentication.

## Features

- User registration and login
- JWT authentication
- Role-based access (Admin, Author, User)
- Blog post CRUD
- SQLite database
- Session management
- CSRF protection
- Rate limiting

## Installation

```bash
cd examples/blog_cms
pip install -r requirements.txt
python app.py
```

## Usage

1. Run the application:
   ```bash
   python app.py
   ```

2. Register a new user:
   ```bash
   python cli.py register admin@example.com admin AdminPass123!
   ```

3. Login:
   ```bash
   python cli.py login admin@example.com AdminPass123!
   ```

4. Create a post:
   ```bash
   python cli.py create-post "My First Post" "This is the content"
   ```

## API Endpoints

- POST /api/register - Register new user
- POST /api/login - Login user
- POST /api/logout - Logout user
- GET /api/posts - List all posts
- POST /api/posts - Create new post (auth required)
- GET /api/posts/:id - Get post by ID
- PUT /api/posts/:id - Update post (auth required, owner only)
- DELETE /api/posts/:id - Delete post (auth required, owner only)

## Architecture

- **Database**: SQLite with query builder
- **Auth**: JWT + Sessions
- **Security**: CSRF, rate limiting, password hashing
- **Roles**: Admin (all), Author (write), User (read)

