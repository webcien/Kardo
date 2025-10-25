#!/bin/bash

# KardoCore PyPI Publication Script
# Version: 0.2.0
# Date: 2025-10-25

set -e  # Exit on error

echo "🚀 KardoCore v0.2.0 - PyPI Publication Script"
echo "=============================================="
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if we're in the right directory
if [ ! -f "pyproject.toml" ]; then
    echo -e "${RED}Error: pyproject.toml not found. Are you in the Kardo directory?${NC}"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo -e "${YELLOW}Creating virtual environment...${NC}"
    python3.11 -m venv .venv
    .venv/bin/pip install --upgrade pip build twine
fi

# Step 1: Clean previous builds
echo -e "${YELLOW}Step 1: Cleaning previous builds...${NC}"
rm -rf dist/ build/ *.egg-info
echo -e "${GREEN}✓ Cleaned${NC}"
echo ""

# Step 2: Build distributions
echo -e "${YELLOW}Step 2: Building distributions...${NC}"
.venv/bin/python -m build
echo -e "${GREEN}✓ Built${NC}"
echo ""

# Step 3: Verify distributions
echo -e "${YELLOW}Step 3: Verifying distributions...${NC}"
.venv/bin/twine check dist/*
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Verification passed${NC}"
else
    echo -e "${RED}✗ Verification failed${NC}"
    exit 1
fi
echo ""

# Step 4: Show files
echo -e "${YELLOW}Step 4: Generated files:${NC}"
ls -lh dist/
echo ""

# Step 5: Ask for confirmation
echo -e "${YELLOW}Step 5: Ready to publish${NC}"
echo ""
echo "The following files will be uploaded to PyPI:"
echo "  - dist/kardocore-0.2.0-py3-none-any.whl"
echo "  - dist/kardocore-0.2.0.tar.gz"
echo ""
read -p "Do you want to continue? (yes/no): " confirm

if [ "$confirm" != "yes" ]; then
    echo -e "${YELLOW}Publication cancelled${NC}"
    exit 0
fi

# Step 6: Choose PyPI or TestPyPI
echo ""
echo "Choose destination:"
echo "  1) PyPI (production)"
echo "  2) TestPyPI (testing)"
read -p "Enter choice (1 or 2): " choice

if [ "$choice" = "2" ]; then
    REPOSITORY="testpypi"
    echo -e "${YELLOW}Publishing to TestPyPI...${NC}"
else
    REPOSITORY="pypi"
    echo -e "${YELLOW}Publishing to PyPI...${NC}"
fi

# Step 7: Get token
echo ""
echo "Enter your PyPI API token (starts with pypi-):"
read -s token
echo ""

# Step 8: Upload
if [ "$REPOSITORY" = "testpypi" ]; then
    .venv/bin/twine upload --repository testpypi dist/* -u __token__ -p "$token"
else
    .venv/bin/twine upload dist/* -u __token__ -p "$token"
fi

if [ $? -eq 0 ]; then
    echo ""
    echo -e "${GREEN}=============================================="
    echo -e "✓ Successfully published to $REPOSITORY!"
    echo -e "=============================================="
    echo ""
    
    if [ "$REPOSITORY" = "pypi" ]; then
        echo "View at: https://pypi.org/project/kardocore/0.2.0/"
        echo ""
        echo "Install with:"
        echo "  pip install kardocore"
    else
        echo "View at: https://test.pypi.org/project/kardocore/0.2.0/"
        echo ""
        echo "Install with:"
        echo "  pip install --index-url https://test.pypi.org/simple/ kardocore"
    fi
    echo -e "${NC}"
else
    echo ""
    echo -e "${RED}✗ Publication failed${NC}"
    echo "Please check the error message above"
    exit 1
fi

# Step 9: Create Git tag
echo ""
read -p "Do you want to create a Git tag v0.2.0? (yes/no): " create_tag

if [ "$create_tag" = "yes" ]; then
    git tag -a v0.2.0 -m "Release v0.2.0 - Full CMS with Admin Panel"
    echo -e "${GREEN}✓ Tag created${NC}"
    echo ""
    read -p "Do you want to push the tag to GitHub? (yes/no): " push_tag
    
    if [ "$push_tag" = "yes" ]; then
        git push origin v0.2.0
        echo -e "${GREEN}✓ Tag pushed to GitHub${NC}"
    fi
fi

echo ""
echo -e "${GREEN}🎉 All done!${NC}"

