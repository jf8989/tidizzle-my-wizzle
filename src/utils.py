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
    firefox_profile_dir = os.path.join(user_home, "AppData", "Local", "Mozilla", "Firefox", "Profiles")
    # Get the first profile directory if it exists
    firefox_cache_path = ""
    if os.path.exists(firefox_profile_dir):
        profiles = [d for d in os.listdir(firefox_profile_dir) if d.endswith('.default-release')]
        if profiles:
            firefox_cache_path = os.path.join(firefox_profile_dir, profiles[0], "cache2")

    return [
        # System Temps
        r"C:\Windows\Temp",
        os.path.join(user_home, "AppData", "Local", "Temp"),
        r"C:\$Recycle.Bin",
        
        # Browsers
        os.path.join(user_home, "AppData", "Local", "Google", "Chrome", "User Data", "Default", "Cache"),
        os.path.join(user_home, "AppData", "Local", "Google", "Chrome", "User Data", "Default", "Code Cache"),
        os.path.join(user_home, "AppData", "Local", "Google", "Chrome", "User Data", "Default", "GPUCache"),
        os.path.join(user_home, "AppData", "Local", "Microsoft", "Edge", "User Data", "Default", "Cache"),
        os.path.join(user_home, "AppData", "Local", "Microsoft", "Edge", "User Data", "Default", "Code Cache"),
        os.path.join(user_home, "AppData", "Local", "Microsoft", "Edge", "User Data", "Default", "GPUCache"),
        firefox_cache_path,
        
        # VS Code
        os.path.join(user_home, "AppData", "Roaming", "Code", "Cache"),
        os.path.join(user_home, "AppData", "Roaming", "Code", "CachedData"),
        os.path.join(user_home, "AppData", "Roaming", "Code", "CachedExtensions"),
        os.path.join(user_home, "AppData", "Roaming", "Code", "Code Cache"),
        os.path.join(user_home, "AppData", "Roaming", "Code", "Crashpad"),
        os.path.join(user_home, "AppData", "Roaming", "Code", "GPUCache"),
        
        # Windows System Caches
        os.path.join(os.environ.get('SystemRoot', 'C:\\Windows'), 'SoftwareDistribution\\Download'),
        os.path.join(os.environ.get('SystemRoot', 'C:\\Windows'), 'Prefetch'),
        
        # Windows Update Cache
        os.path.join(user_home, "AppData", "Local", "Microsoft", "Windows", "INetCache"),
        os.path.join(user_home, "AppData", "Local", "Microsoft", "Windows", "Temporary Internet Files"),
        
        # Windows Thumbnail Cache
        os.path.join(user_home, "AppData", "Local", "Microsoft", "Windows", "Explorer", "thumbcache_*.db")
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