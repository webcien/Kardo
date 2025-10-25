"""
Init Command - Initialize new KardoCore project
"""

from pathlib import Path
from kardocore.cli.commands.base import BaseCommand


class InitCommand(BaseCommand):
    """Initialize a new KardoCore project"""
    
    def __init__(self):
        super().__init__("init", "Initialize a new KardoCore project")
    
    def execute(self, args: list[str]) -> int:
        """Execute init command"""
        project_name = args[0] if args else "my-kardo-project"
        
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
from kardocore.auth import KardoAuth

async def main():
    # Initialize database
    db = Database("sqlite", "app.db")
    await db.connect()
    
    # Initialize auth
    auth = KardoAuth(db)
    
    print("✅ KardoCore initialized!")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
""")
        
        # Create config.py
        (project_path / "config.py").write_text("""
# KardoCore Configuration

DATABASE_URL = "sqlite:///app.db"
SECRET_KEY = "change-this-secret-key"
DEBUG = True
""")
        
        # Create requirements.txt
        (project_path / "requirements.txt").write_text("""kardocore>=0.2.0
aiosqlite>=0.19.0
bcrypt>=4.0.0
""")
        
        # Create README.md
        (project_path / "README.md").write_text(f"""# {project_name}

KardoCore project initialized.

## Setup

```bash
pip install -r requirements.txt
python main.py
```
""")
        
        print(f"✅ Project '{project_name}' created successfully!")
        print(f"📁 Location: {project_path}")
        print(f"\n Next steps:")
        print(f"   cd {project_name}")
        print(f"   pip install -r requirements.txt")
        print(f"   python main.py")
        
        return 0
