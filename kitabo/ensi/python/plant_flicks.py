#!/usr/bin/env python3
"""
plant_flicks.py 🌱

Performs the flick ritual:
- Walks the Git-rooted directory tree starting from shill.
- Appends symbolic graffiti to existing dotfiles or creates new ones in each folder.
- Appends to hidden files adjacent to regular files too.
- Commits each flick individually with a unique message.
"""

import os
import random
import string
from datetime import datetime
import subprocess

# Dynamically resolve Git root from script location
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))

def random_tag():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=4))

def random_filename():
    return f".{''.join(random.choices(string.ascii_lowercase, k=random.randint(4, 8)))}"

def generate_graffiti():
    timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
    tag = random_tag()
    return f"# flick {timestamp}-{tag}\n"

def find_git_root(start_path):
    current = os.path.abspath(start_path)
    while current != "/":
        if os.path.isdir(os.path.join(current, ".git")):
            return current
        current = os.path.dirname(current)
    raise RuntimeError("❌ Git root not found.")

def get_or_create_flick_path(folder):
    existing = [f for f in os.listdir(folder) if f.startswith('.') and not f.startswith('..')]
    flicks = [f for f in existing if os.path.isfile(os.path.join(folder, f))]
    if flicks:
        return os.path.join(folder, random.choice(flicks))  # Append to existing
    else:
        return os.path.join(folder, random_filename())      # Create new

def flick_file(file_path):
    """Add graffiti to a hidden file adjacent to a normal file."""
    folder = os.path.dirname(file_path)
    return get_or_create_flick_path(folder)

def git_commit(file_path, message, repo_root):
    try:
        subprocess.run(["git", "add", file_path], cwd=repo_root, check=True)
        subprocess.run(["git", "commit", "-m", message], cwd=repo_root, check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Git commit failed for {file_path}: {e}")

def plant_flicks(base_dir):
    repo_root = find_git_root(base_dir)
    flicked = 0
    visited_folders = set()

    for root, dirs, files in os.walk(base_dir):
        # Flick the folder itself (once)
        if root not in visited_folders:
            try:
                flick_path = get_or_create_flick_path(root)
                with open(flick_path, 'a') as f:
                    graffiti = generate_graffiti()
                    f.write(graffiti)
                rel_path = os.path.relpath(flick_path, start=repo_root)
                git_commit(flick_path, f" {rel_path}", repo_root)
                print(f"✅ {rel_path}")
                flicked += 1
                visited_folders.add(root)
            except Exception as e:
                print(f"❌ Folder flick failed in {root}: {e}")

        # Now flick adjacent to each file
        for file in files:
            file_path = os.path.join(root, file)
            try:
                flick_path = flick_file(file_path)
                with open(flick_path, 'a') as f:
                    graffiti = generate_graffiti()
                    f.write(graffiti)
                rel_path = os.path.relpath(flick_path, start=repo_root)
                git_commit(flick_path, f" {rel_path}", repo_root)
                print(f"✅ {rel_path}")
                flicked += 1
            except Exception as e:
                print(f"❌ File flick failed for {file_path}: {e}")

    print(f"\n🌿 Ritual complete: {flicked} flicks planted (folders + files).")

if __name__ == "__main__":
    plant_flicks(BASE_DIR)
