#!/usr/bin/env python3
"""
plant_flicks.py 🌱

Performs the flick ritual:
- Walks the Git-rooted directory tree starting from `shill`.
- Appends symbolic graffiti to:
    • one dotfile per directory
    • one hidden dotfile per *file* (e.g., `.index.html.flick`)
- Commits each flick with a unique message.
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

def flick_to_file(target_path, repo_root):
    graffiti = generate_graffiti()
    with open(target_path, 'a') as f:
        f.write(graffiti)
    rel_path = os.path.relpath(target_path, start=repo_root)
    git_commit(target_path, f" {rel_path}", repo_root)
    print(f"✅ {rel_path}")

def git_commit(file_path, message, repo_root):
    try:
        subprocess.run(["git", "add", file_path], cwd=repo_root, check=True)
        subprocess.run(["git", "commit", "-m", message], cwd=repo_root, check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Git commit failed for {file_path}: {e}")

def plant_flicks(base_dir):
    repo_root = find_git_root(base_dir)
    flicked = 0
    visited_dirs = set()

    for root, dirs, files in os.walk(base_dir):
        # Flick once per folder
        if root not in visited_dirs:
            folder_flick = os.path.join(root, f".{random_tag().lower()}")
            try:
                flick_to_file(folder_flick, repo_root)
                flicked += 1
                visited_dirs.add(root)
            except Exception as e:
                print(f"❌ Folder flick failed in {root}: {e}")

        # Flick once per file
        for filename in files:
            try:
                full_path = os.path.join(root, filename)
                basename = os.path.basename(filename)
                flick_file = os.path.join(root, f".{basename}.flick")
                flick_to_file(flick_file, repo_root)
                flicked += 1
            except Exception as e:
                print(f"❌ File flick failed for {filename}: {e}")

    print(f"\n🌿 Ritual complete: {flicked} flicks planted across folders and files.")

if __name__ == "__main__":
    plant_flicks(BASE_DIR)
