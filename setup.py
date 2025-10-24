"""
KardoCore Setup Configuration
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

# Read requirements
requirements = [
    "bcrypt>=4.0.0",
    "aiosqlite>=0.19.0",
]

# Optional requirements
extras_require = {
    "postgresql": ["asyncpg>=0.28.0"],
    "mysql": ["aiomysql>=0.2.0"],
    "argon2": ["argon2-cffi>=21.3.0"],
    "dev": [
        "pytest>=7.4.0",
        "pytest-asyncio>=0.21.0",
        "pytest-cov>=4.1.0",
        "black>=23.7.0",
        "mypy>=1.5.0",
    ],
    "all": [
        "asyncpg>=0.28.0",
        "aiomysql>=0.2.0",
        "argon2-cffi>=21.3.0",
    ],
}

setup(
    name="kardocore",
    version="0.2.0",
    author="WebCien",
    author_email="contact@webcien.com",
    description="Modern Python CMS Framework - Fast, Typed, Secure, Modular",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/webcien/Kardo",
    project_urls={
        "Bug Tracker": "https://github.com/webcien/Kardo/issues",
        "Documentation": "https://github.com/webcien/Kardo/blob/main/README.md",
        "Source Code": "https://github.com/webcien/Kardo",
    },
    packages=find_packages(exclude=["tests", "tests.*", "examples", "examples.*"]),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: 3.14",
        "Framework :: AsyncIO",
        "Typing :: Typed",
    ],
    python_requires=">=3.11",
    install_requires=requirements,
    extras_require=extras_require,
    entry_points={
        "console_scripts": [
            "kardo=kardocore.cli.main:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
    keywords=[
        "cms",
        "framework",
        "web",
        "async",
        "database",
        "authentication",
        "theme",
        "template",
        "modern",
        "typed",
        "fast",
        "secure",
        "modular",
    ],
)

