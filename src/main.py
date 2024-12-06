"""
File: src/main.py
Project: Tidizzle My Wizzle
Description: Main entry point for the application. Handles admin privileges and GUI initialization.
Author: [Your Name]
Date: [Current Date]
"""

import os
import sys
import traceback
import tkinter as tk
from datetime import datetime
from tkinter import messagebox
from ctypes import windll
from win32com.shell import shell
from .gui import CleanerGUI  # Changed to absolute import

def main():
    root = tk.Tk()
    app = CleanerGUI(root)
    root.mainloop()

try:
    import tkinter as tk
    print("Tkinter successfully imported")
except ImportError as e:
    print(f"Error importing tkinter: {e}")

def log_error(error):
    with open('error_log.txt', 'a') as f:
        f.write(f"\n{'-'*50}\n")
        f.write(f"Error occurred at: {datetime.now()}\n")
        f.write(traceback.format_exc())

def run_as_admin():
    try:
        print("Checking admin privileges...")
        is_admin = windll.shell32.IsUserAnAdmin()
        
        if not is_admin:
            print("Not running as admin, attempting to elevate privileges...")
            script = os.path.abspath(sys.argv[0])
            params = f"-m src.main"  # Modified to use module syntax
            
            try:
                shell.ShellExecuteEx(
                    lpVerb='runas',
                    lpFile=sys.executable,
                    lpParameters=params,
                    nShow=1  # Added to show the window
                )
                print("Elevation request sent. Closing current instance.")
                sys.exit(0)
                
            except Exception as e:
                error_msg = f"Failed to obtain admin rights: {str(e)}"
                print(error_msg)
                messagebox.showerror(
                    "Admin Rights Required",
                    "This application needs administrative privileges.\n"
                    f"Error: {str(e)}"
                )
                sys.exit(1)
        
        return is_admin
        
    except Exception as e:
        print(f"Error checking admin privileges: {str(e)}")
        raise

if __name__ == "__main__":
    print("Main block started")
    try:
        run_as_admin()
        
        # Initialize the main window
        root = tk.Tk()
        app = CleanerGUI(root)
        root.mainloop()
        
    except Exception as e:
        log_error(e)
        print(f"Error occurred: {e}")
        print("Check error_log.txt for details")
        input("Press Enter to exit...")