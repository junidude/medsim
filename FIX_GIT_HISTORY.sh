#!/bin/bash
# Fix Git history to remove API keys

echo "Fixing Git history to remove sensitive data..."

# Option 1: If you just made the initial commit, we can amend it
echo "Amending the last commit..."
git add CLAUDE.md
git commit --amend -m "Initial commit: MedSim medical education platform (API keys removed)"

# Force push to overwrite the remote
echo "Force pushing to GitHub..."
git push -f origin main

echo "Done! The repository should now be clean of API keys."