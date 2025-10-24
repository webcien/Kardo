"""
KardoCore CLI - Command Line Interface

Main entry point for the kardo command.
"""

import sys
import asyncio
from typing import List, Optional
from kardocore.cli.commands import (
    InitCommand,
    ServeCommand,
    ThemeCommand,
    UserCommand,
    MigrateCommand,
    BuildCommand
)


class KardoCLI:
    """Main CLI application"""
    
    def __init__(self):
        self.commands = {
            "init": InitCommand(),
            "serve": ServeCommand(),
            "theme": ThemeCommand(),
            "user": UserCommand(),
            "migrate": MigrateCommand(),
            "build": BuildCommand(),
        }
    
    def print_help(self):
        """Print help message"""
        print("""
KardoCore CLI - Modern Python CMS Framework

Usage:
  kardo <command> [options]

Commands:
  init       Initialize a new KardoCore project
  serve      Start development server
  theme      Manage themes (install, list, search, etc.)
  user       Manage users (create, list, delete, etc.)
  migrate    Run database migrations
  build      Build project for production

Options:
  -h, --help     Show this help message
  -v, --version  Show version information

Examples:
  kardo init my-project
  kardo serve --port 8000
  kardo theme install wellness-clinic
  kardo user create admin@example.com --role admin
  kardo migrate up
  kardo build --output dist/

For more information on a specific command:
  kardo <command> --help

Documentation: https://github.com/webcien/Kardo
        """)
    
    def print_version(self):
        """Print version information"""
        print("KardoCore v0.2.0")
        print("Python CMS Framework")
        print("https://github.com/webcien/Kardo")
    
    async def run(self, args: List[str]):
        """Run CLI command"""
        if not args or args[0] in ["-h", "--help", "help"]:
            self.print_help()
            return 0
        
        if args[0] in ["-v", "--version", "version"]:
            self.print_version()
            return 0
        
        command_name = args[0]
        command_args = args[1:]
        
        if command_name not in self.commands:
            print(f"Error: Unknown command '{command_name}'")
            print("Run 'kardo --help' for usage information")
            return 1
        
        command = self.commands[command_name]
        
        try:
            return await command.execute(command_args)
        except KeyboardInterrupt:
            print("\nInterrupted by user")
            return 130
        except Exception as e:
            print(f"Error: {e}")
            return 1


def main():
    """Main entry point"""
    cli = KardoCLI()
    args = sys.argv[1:]
    
    try:
        exit_code = asyncio.run(cli.run(args))
        sys.exit(exit_code)
    except KeyboardInterrupt:
        sys.exit(130)


if __name__ == "__main__":
    main()
