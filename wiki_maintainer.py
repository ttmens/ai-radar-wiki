#!/usr/bin/env python3
"""
Hermes Wiki Maintainer (v2)
Manages the local Markdown wiki based on incoming intelligence from Cron jobs.
Based on Karpathy's LLM Wiki concept.

Usage:
    python wiki_maintainer.py --data '{"updates": [{"category": "entities", "name": "OpenAI", "content": "New update..."}]}'
"""

import os
import sys
import re
import json
import argparse
from datetime import datetime

WIKI_ROOT = os.path.expanduser("~/hermes-wiki")

def slugify(name):
    """Convert name to a valid filename."""
    name = name.lower().strip()
    name = re.sub(r'[^\w\s-]', '', name)
    name = re.sub(r'[\s]+', '-', name)
    return name

def update_or_create(category, name, content, date=None):
    """
    Appends content to a wiki page. If the page doesn't exist, it creates it with a header.
    Category should be a directory name inside WIKI_ROOT (e.g., 'entities', 'topics').
    """
    if not date:
        date = datetime.now().strftime("%Y-%m-%d")
    
    dir_path = os.path.join(WIKI_ROOT, category)
    os.makedirs(dir_path, exist_ok=True)
    
    filename = f"{slugify(name)}.md"
    filepath = os.path.join(dir_path, filename)
    
    # Content formatting
    entry = f"\n### {date}\n{content.strip()}\n"
    
    if os.path.exists(filepath):
        # Append to existing file
        with open(filepath, "a", encoding="utf-8") as f:
            f.write(entry)
        print(f"✅ Updated: {filepath}")
    else:
        # Create new file with header
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(f"# {name}\n\n**Created:** {date}\n\n## Timeline\n")
            f.write(entry)
        print(f"✨ Created: {filepath}")

def main():
    parser = argparse.ArgumentParser(description="Update Local Wiki")
    parser.add_argument("--data", type=str, required=True, help="JSON string containing updates")
    args = parser.parse_args()

    try:
        payload = json.loads(args.data)
        updates = payload.get("updates", [])
        
        if not updates:
            print("No updates found in payload.")
            return

        for update in updates:
            update_or_create(
                category=update.get("category", "entities"),
                name=update.get("name", "Unknown"),
                content=update.get("content", ""),
                date=update.get("date")
            )
            
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
