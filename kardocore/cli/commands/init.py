"""
Init Command - Initialize new KardoCore project
"""

from pathlib import Path
from kardocore.cli.commands.base import BaseCommand


class InitCommand(BaseCommand):
    """Initialize a new KardoCore project"""
    
    name = "init"
    description = "Initialize a new KardoCore project"
    
    def _add_arguments(self, parser):
        """Add command arguments"""
        parser.add_argument(
            "project_name",
            nargs="?",
            default="my-kardo-project",
            help="Name of the project to create"
        )
    
    async def execute(self, args: list[str]) -> int:
        """Execute init command"""
        parsed = self.parse_args(args)
        project_name = parsed.project_name
        
        print(f"🚀 Initializing KardoCore project: {project_name}")
        
        # Create project directory
        project_path = Path.cwd() / project_name
        if project_path.exists():
            print(f"❌ Error: Directory '{project_name}' already exists")
            return 1
        
        project_path.mkdir(parents=True)
        
        # Create main.py
        (project_path / "main.py").write_text("""
from kardocore.db import Database
from kardocore.db.adapters import SQLiteAdapter
from kardocore.auth import AuthManager, UserRepository

async def main():
    # Initialize database
    db = Database(SQLiteAdapter("app.db"))
    await db.connect()
    
    # Initialize auth
    user_repo = UserRepository(db)
    auth = AuthManager(user_repo, secret_key="change-this-secret-key")
    
    print("✅ KardoCore initialized!")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
""", encoding='utf-8')
        
        # Create config.py
        (project_path / "config.py").write_text("""
# KardoCore Configuration

DATABASE_URL = "sqlite:///app.db"
SECRET_KEY = "change-this-secret-key"
DEBUG = True
""", encoding='utf-8')
        
        # Create requirements.txt
        (project_path / "requirements.txt").write_text("""kardocore>=0.2.2
aiosqlite>=0.19.0
bcrypt>=4.0.0
""", encoding='utf-8')
        
        # Create README.md
        (project_path / "README.md").write_text(f"""# {project_name}

KardoCore project initialized.

## Setup

```bash
pip install -r requirements.txt
python main.py
```
""", encoding='utf-8')
        
        print(f"✅ Project '{project_name}' created successfully!")
        print(f"📁 Location: {project_path}")
        print(f"\n Next steps:")
        print(f"   cd {project_name}")
        print(f"   pip install -r requirements.txt")
        print(f"   python main.py")
        
        return 0
