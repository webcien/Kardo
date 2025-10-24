"""
Base Command Class

Abstract base class for all CLI commands.
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
import argparse


class BaseCommand(ABC):
    """Base class for CLI commands"""
    
    name: str = ""
    description: str = ""
    
    def __init__(self):
        self.parser = self._create_parser()
    
    def _create_parser(self) -> argparse.ArgumentParser:
        """Create argument parser for this command"""
        parser = argparse.ArgumentParser(
            prog=f"kardo {self.name}",
            description=self.description,
            add_help=True
        )
        self._add_arguments(parser)
        return parser
    
    @abstractmethod
    def _add_arguments(self, parser: argparse.ArgumentParser):
        """Add command-specific arguments"""
        pass
    
    @abstractmethod
    async def execute(self, args: List[str]) -> int:
        """Execute the command"""
        pass
    
    def parse_args(self, args: List[str]) -> argparse.Namespace:
        """Parse command arguments"""
        return self.parser.parse_args(args)
    
    def print_success(self, message: str):
        """Print success message"""
        print(f"✅ {message}")
    
    def print_error(self, message: str):
        """Print error message"""
        print(f"❌ {message}")
    
    def print_info(self, message: str):
        """Print info message"""
        print(f"ℹ️  {message}")
    
    def print_warning(self, message: str):
        """Print warning message"""
        print(f"⚠️  {message}")
