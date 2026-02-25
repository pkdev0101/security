#!/usr/bin/env python3

import os
import re
from collections import Counter

APT_SOURCES = [
    "/etc/apt/sources.list",
    "/etc/apt/sources.list.d/"
]

def get_source_files():
    files = []
    for path in APT_SOURCES:
        if os.path.isfile(path):
            files.append(path)
        elif os.path.isdir(path):
            for file in os.listdir(path):
                if file.endswith(".list"):
                    files.append(os.path.join(path, file))
    return files

def check_https(lines, filename):
    print(f"\n[+] Checking HTTPS usage in {filename}")
    for line in lines:
        if line.strip().startswith("deb ") and "http://" in line:
            print(f"  ⚠ Insecure HTTP repo found: {line.strip()}")

def check_signed_by(lines, filename):
    print(f"\n[+] Checking signed-by option in {filename}")
    for line in lines:
        if line.strip().startswith("deb ") and "signed-by=" not in line:
            print(f"  ⚠ Missing signed-by option: {line.strip()}")

def check_duplicates(all_repos):
    print("\n[+] Checking duplicate repositories")
    repo_counts = Counter(all_repos)
    for repo, count in repo_counts.items():
        if count > 1:
            print(f"  ⚠ Duplicate repo found ({count} times): {repo}")

def check_permissions(file):
    print(f"\n[+] Checking file permissions for {file}")
    mode = os.stat(file).st_mode
    if mode & 0o002:
        print(f"  ⚠ File is world-writable: {file}")

def check_apt_key():
    print("\n[+] Checking deprecated apt-key usage")
    if os.path.exists("/etc/apt/trusted.gpg"):
        print("  ⚠ Deprecated apt-key keyring detected: /etc/apt/trusted.gpg")

def main():
    print("=== APT Repository Security Audit ===")
    source_files = get_source_files()
    all_repos = []

    for file in source_files:
        try:
            with open(file, "r") as f:
                lines = f.readlines()

            check_https(lines, file)
            check_signed_by(lines, file)
            check_permissions(file)

            for line in lines:
                if line.strip().startswith("deb "):
                    all_repos.append(line.strip())

        except Exception as e:
            print(f"Error reading {file}: {e}")

    check_duplicates(all_repos)
    check_apt_key()

    print("\n=== Audit Complete ===")

if __name__ == "__main__":
    main()
