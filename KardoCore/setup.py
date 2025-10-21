"""
Setup configuration for KardoCore
"""

from setuptools import setup, find_packages
from pathlib import Path

# Leer README
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

# Leer versión
version = "0.0.9"

setup(
    name="kardocore",
    version=version,
    author="Juan Quezada",
    author_email="",
    description="Framework Python Híbrido, Modular e IA-Ready",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/webcien/KardoCore",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Framework :: AsyncIO",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
    ],
    python_requires=">=3.11",
    install_requires=[
        # Servidor ASGI
        "uvicorn>=0.30.0",
        # No usamos Pydantic - tenemos nuestro propio sistema
        # No usamos Starlette - tenemos nuestro propio ASGI
    ],
    extras_require={
        "dev": [
            "pytest>=8.0.0",
            "pytest-asyncio>=0.23.0",
            "black>=24.0.0",
            "mypy>=1.8.0",
        ],
        "docs": [
            "mkdocs>=1.5.0",
            "mkdocs-material>=9.5.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "kardo=kardocore.cli.installer:main",
            "krd=kardocore.cli.installer:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)

