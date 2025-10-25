# KardoAdmin

Modern administrative panel for KardoCore.

## Features

- ✅ Dashboard with statistics
- ✅ User management (CRUD)
- ✅ Content management (posts, pages)
- ✅ File manager with upload
- ✅ Theme manager
- ✅ Settings panel
- ✅ Responsive design (mobile-first)
- ✅ KardoCSS integration
- ✅ KardoTheme templates

## Usage

```python
from kardocore.admin import KardoAdmin
from kardocore.db import Database, SQLiteAdapter
from kardocore.auth import AuthManager

# Initialize
db = Database(SQLiteAdapter("app.db"))
auth = AuthManager(db)
admin = KardoAdmin(db, auth)

# Get dashboard stats
stats = await admin.get_stats()

# Access routes
dashboard_data = await admin.dashboard.index()
users_data = await admin.users.list(page=1)
```

## Routes

- `GET /admin` - Dashboard
- `GET /admin/users` - List users
- `POST /admin/users` - Create user
- `PUT /admin/users/:id` - Update user
- `DELETE /admin/users/:id` - Delete user
- `GET /admin/content` - List content
- `POST /admin/content` - Create content
- `GET /admin/files` - List files
- `POST /admin/files/upload` - Upload files
- `GET /admin/themes` - List themes
- `GET /admin/settings` - Settings page

## Templates

All templates use KardoTheme syntax:

- `#for item in items` - Loops
- `#if condition` - Conditionals
- `{variable}` - Variables
- `#include "file.html"` - Includes

## Styling

Uses KardoCSS classes:

- Layout: `flex`, `grid`, `container`
- Components: `card`, `btn`, `table`, `badge`
- Utilities: `p-4`, `mb-6`, `text-xl`, etc.

## Mobile Support

- Responsive sidebar (hamburger menu on mobile)
- Touch-optimized buttons (44x44px)
- Mobile-first design
- Adaptive layouts

## Security

- CSRF protection required
- Authentication required for all routes
- Role-based access control
- Rate limiting on sensitive operations

## Customization

Override templates by creating files in your project:

```
my_project/
└── templates/
    └── admin/
        └── dashboard/
            └── index.html  # Override default dashboard
```

## Development

Run in development mode:

```bash
kardo serve --admin
```

Access at: `http://localhost:5000/admin`
