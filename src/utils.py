"""
File: src/utils.py
Project: Tidizzle My Wizzle
Description: Utility functions for path management and calculations.
Author: [Your Name]
Date: [Current Date]
"""

import os

def get_user_home_path():
    return os.path.expanduser('~')

def get_paths_to_clean():
    user_home = get_user_home_path()
    return [
        r"C:\Windows\Temp",
        os.path.join(user_home, "AppData", "Local", "Temp"),
        r"C:\$Recycle.Bin",
        os.path.join(user_home, "AppData", "Local", "Google", "Chrome", "User Data", "Default", "Cache"),
        os.path.join(user_home, "AppData", "Local", "Microsoft", "Edge", "User Data", "Default", "Cache"),
        os.path.join(user_home, "AppData", "Local", "Mozilla", "Firefox", "Profiles", "[Perfil]", "cache2"),
        os.path.join(user_home, "AppData", "Roaming", "Code"),
    ]

def calculate_path_size(path):
    """Calculate the size of a path (file or directory)"""
    total_size = 0
    if os.path.isdir(path):
        for dirpath, dirnames, filenames in os.walk(path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                try:
                    total_size += os.path.getsize(fp)
                except OSError:
                    pass
    else:
        total_size = os.path.getsize(path)
    return total_size

def validate_path(path):
    return os.path.exists(path)