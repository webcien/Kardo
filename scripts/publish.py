#!/usr/bin/env python3
"""
KardoCore PyPI Publication Automation Script

This script automates the process of publishing KardoCore to PyPI.

Usage:
    python scripts/publish.py --test     # Publish to TestPyPI
    python scripts/publish.py --prod     # Publish to PyPI
    python scripts/publish.py --check    # Only check, don't publish
"""

import argparse
import os
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional


class Colors:
    """ANSI color codes for terminal output"""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'


class PyPIPublisher:
    """Automates PyPI publication process"""
    
    def __init__(self, test_mode: bool = False, check_only: bool = False):
        self.test_mode = test_mode
        self.check_only = check_only
        self.root_dir = Path(__file__).parent.parent
        self.dist_dir = self.root_dir / "dist"
        self.setup_py = self.root_dir / "setup.py"
        self.pyproject_toml = self.root_dir / "pyproject.toml"
        self.changelog = self.root_dir / "CHANGELOG.md"
        
    def print_header(self, message: str):
        """Print colored header"""
        print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*70}{Colors.ENDC}")
        print(f"{Colors.HEADER}{Colors.BOLD}{message:^70}{Colors.ENDC}")
        print(f"{Colors.HEADER}{Colors.BOLD}{'='*70}{Colors.ENDC}\n")
        
    def print_success(self, message: str):
        """Print success message"""
        print(f"{Colors.OKGREEN}✅ {message}{Colors.ENDC}")
        
    def print_info(self, message: str):
        """Print info message"""
        print(f"{Colors.OKCYAN}ℹ️  {message}{Colors.ENDC}")
        
    def print_warning(self, message: str):
        """Print warning message"""
        print(f"{Colors.WARNING}⚠️  {message}{Colors.ENDC}")
        
    def print_error(self, message: str):
        """Print error message"""
        print(f"{Colors.FAIL}❌ {message}{Colors.ENDC}")
        
    def run_command(self, cmd: list, capture_output: bool = False) -> Optional[str]:
        """Run shell command"""
        try:
            if capture_output:
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    check=True,
                    cwd=self.root_dir
                )
                return result.stdout.strip()
            else:
                subprocess.run(cmd, check=True, cwd=self.root_dir)
                return None
        except subprocess.CalledProcessError as e:
            self.print_error(f"Command failed: {' '.join(cmd)}")
            if capture_output and e.stderr:
                print(e.stderr)
            sys.exit(1)
            
    def check_prerequisites(self):
        """Check if all prerequisites are met"""
        self.print_header("Checking Prerequisites")
        
        # Check Python version
        py_version = sys.version_info
        if py_version < (3, 11):
            self.print_error(f"Python 3.11+ required, found {py_version.major}.{py_version.minor}")
            sys.exit(1)
        self.print_success(f"Python {py_version.major}.{py_version.minor}.{py_version.micro}")
        
        # Check if in git repository
        if not (self.root_dir / ".git").exists():
            self.print_error("Not in a git repository")
            sys.exit(1)
        self.print_success("Git repository")
        
        # Check required files
        required_files = [
            self.setup_py,
            self.pyproject_toml,
            self.root_dir / "README.md",
            self.root_dir / "LICENSE",
        ]
        
        for file in required_files:
            if not file.exists():
                self.print_error(f"Required file missing: {file.name}")
                sys.exit(1)
        self.print_success("All required files present")
        
        # Check if build and twine are installed
        try:
            import build
            self.print_success("build package installed")
        except ImportError:
            self.print_error("build package not installed. Run: pip install build")
            sys.exit(1)
            
        try:
            import twine
            self.print_success("twine package installed")
        except ImportError:
            self.print_error("twine package not installed. Run: pip install twine")
            sys.exit(1)
            
        # Check for uncommitted changes
        status = self.run_command(["git", "status", "--porcelain"], capture_output=True)
        if status:
            self.print_warning("Uncommitted changes detected:")
            print(status)
            response = input("\nContinue anyway? (y/N): ")
            if response.lower() != 'y':
                sys.exit(0)
        else:
            self.print_success("No uncommitted changes")
            
    def get_version(self) -> str:
        """Extract version from setup.py"""
        self.print_header("Version Information")
        
        content = self.setup_py.read_text()
        match = re.search(r'version\s*=\s*["\']([^"\']+)["\']', content)
        
        if not match:
            self.print_error("Could not find version in setup.py")
            sys.exit(1)
            
        version = match.group(1)
        self.print_info(f"Current version: {version}")
        
        # Check if version tag exists
        tags = self.run_command(["git", "tag"], capture_output=True)
        if f"v{version}" in tags.split('\n'):
            self.print_warning(f"Git tag v{version} already exists")
        
        return version
        
    def check_changelog(self, version: str):
        """Check if CHANGELOG is updated"""
        self.print_header("Checking CHANGELOG")
        
        if not self.changelog.exists():
            self.print_warning("CHANGELOG.md not found")
            return
            
        content = self.changelog.read_text()
        
        # Check if version is mentioned
        if f"[{version}]" not in content and f"## {version}" not in content:
            self.print_warning(f"Version {version} not found in CHANGELOG.md")
            response = input("Continue anyway? (y/N): ")
            if response.lower() != 'y':
                sys.exit(0)
        else:
            self.print_success(f"Version {version} found in CHANGELOG.md")
            
    def clean_build(self):
        """Clean previous build artifacts"""
        self.print_header("Cleaning Build Artifacts")
        
        patterns = [
            "build",
            "dist",
            "*.egg-info",
            "**/__pycache__",
            "**/*.pyc",
        ]
        
        for pattern in patterns:
            for path in self.root_dir.glob(pattern):
                if path.is_dir():
                    import shutil
                    shutil.rmtree(path)
                    self.print_info(f"Removed directory: {path.name}")
                else:
                    path.unlink()
                    self.print_info(f"Removed file: {path.name}")
                    
        self.print_success("Build artifacts cleaned")
        
    def build_package(self):
        """Build package distributions"""
        self.print_header("Building Package")
        
        self.print_info("Building wheel and source distribution...")
        self.run_command([sys.executable, "setup.py", "sdist", "bdist_wheel"])
        
        # List generated files
        if self.dist_dir.exists():
            files = list(self.dist_dir.iterdir())
            self.print_success(f"Generated {len(files)} distribution file(s):")
            for file in files:
                size = file.stat().st_size / 1024  # KB
                print(f"  - {file.name} ({size:.1f} KB)")
        else:
            self.print_error("dist/ directory not found")
            sys.exit(1)
            
    def check_package(self):
        """Check package with twine"""
        self.print_header("Checking Package")
        
        self.print_info("Running twine check...")
        self.run_command([sys.executable, "-m", "twine", "check", "dist/*"])
        self.print_success("Package passed twine checks")
        
    def upload_package(self):
        """Upload package to PyPI or TestPyPI"""
        if self.check_only:
            self.print_header("Check Only Mode")
            self.print_success("Package is ready for publication!")
            self.print_info("Run without --check to publish")
            return
            
        self.print_header("Uploading Package")
        
        if self.test_mode:
            self.print_info("Uploading to TestPyPI...")
            repository = "testpypi"
            url = "https://test.pypi.org"
        else:
            self.print_warning("Uploading to PRODUCTION PyPI...")
            response = input("Are you sure? This cannot be undone. (yes/N): ")
            if response.lower() != 'yes':
                self.print_info("Upload cancelled")
                sys.exit(0)
            repository = "pypi"
            url = "https://pypi.org"
            
        # Check if .pypirc exists
        pypirc = Path.home() / ".pypirc"
        if not pypirc.exists():
            self.print_error("~/.pypirc not found")
            self.print_info("Create it with your PyPI credentials")
            self.print_info("See .pypirc.template for example")
            sys.exit(1)
            
        # Upload
        cmd = [sys.executable, "-m", "twine", "upload"]
        if self.test_mode:
            cmd.extend(["--repository", repository])
        cmd.append("dist/*")
        
        self.run_command(cmd)
        
        version = self.get_version()
        package_url = f"{url}/project/kardocore/{version}/"
        
        self.print_success("Package uploaded successfully!")
        self.print_info(f"View at: {package_url}")
        
    def create_git_tag(self, version: str):
        """Create and push git tag"""
        if self.check_only or self.test_mode:
            return
            
        self.print_header("Creating Git Tag")
        
        tag = f"v{version}"
        
        # Check if tag exists
        tags = self.run_command(["git", "tag"], capture_output=True)
        if tag in tags.split('\n'):
            self.print_warning(f"Tag {tag} already exists")
            return
            
        response = input(f"Create and push tag {tag}? (y/N): ")
        if response.lower() != 'y':
            self.print_info("Tag creation skipped")
            return
            
        # Create tag
        message = f"Release {version}"
        self.run_command(["git", "tag", "-a", tag, "-m", message])
        self.print_success(f"Created tag {tag}")
        
        # Push tag
        self.run_command(["git", "push", "origin", tag])
        self.print_success(f"Pushed tag {tag} to origin")
        
    def verify_installation(self):
        """Verify package can be installed"""
        if self.check_only:
            return
            
        self.print_header("Verification")
        
        if self.test_mode:
            self.print_info("To test installation from TestPyPI:")
            print("  pip install --index-url https://test.pypi.org/simple/ kardocore")
        else:
            self.print_info("To test installation from PyPI:")
            print("  pip install kardocore")
            
        self.print_info("To verify:")
        print("  kardo --version")
        print("  python -c 'import kardocore; print(kardocore.__version__)'")
        
    def run(self):
        """Run the publication process"""
        try:
            self.print_header("KardoCore PyPI Publication")
            
            if self.test_mode:
                self.print_info("Mode: TestPyPI (test)")
            elif self.check_only:
                self.print_info("Mode: Check only (no upload)")
            else:
                self.print_info("Mode: Production PyPI")
                
            # Run steps
            self.check_prerequisites()
            version = self.get_version()
            self.check_changelog(version)
            self.clean_build()
            self.build_package()
            self.check_package()
            self.upload_package()
            self.create_git_tag(version)
            self.verify_installation()
            
            # Success
            self.print_header("Publication Complete!")
            self.print_success("All steps completed successfully")
            
            if not self.check_only:
                self.print_info("Next steps:")
                print("  1. Verify installation")
                print("  2. Update README.md with PyPI badge")
                print("  3. Create GitHub release")
                print("  4. Announce on social media")
                
        except KeyboardInterrupt:
            self.print_warning("\nPublication cancelled by user")
            sys.exit(1)
        except Exception as e:
            self.print_error(f"Unexpected error: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Automate KardoCore publication to PyPI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Check package without uploading
  python scripts/publish.py --check
  
  # Publish to TestPyPI for testing
  python scripts/publish.py --test
  
  # Publish to production PyPI
  python scripts/publish.py --prod
        """
    )
    
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--check",
        action="store_true",
        help="Check package without uploading"
    )
    group.add_argument(
        "--test",
        action="store_true",
        help="Upload to TestPyPI (test environment)"
    )
    group.add_argument(
        "--prod",
        action="store_true",
        help="Upload to production PyPI"
    )
    
    args = parser.parse_args()
    
    publisher = PyPIPublisher(
        test_mode=args.test,
        check_only=args.check
    )
    
    publisher.run()


if __name__ == "__main__":
    main()

