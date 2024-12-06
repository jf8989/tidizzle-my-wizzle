"""
File: src/main.py
Project: Tidizzle My Wizzle
Description: Main entry point for the application. Handles admin privileges and GUI initialization.
Author: [Your Name]
Date: [Current Date]
"""

import os
import sys
import tkinter as tk
from datetime import datetime
from tkinter import messagebox
from ctypes import windll
from win32com.shell import shell
from .gui import CleanerGUI

def run_as_admin():
    try:
        is_admin = windll.shell32.IsUserAnAdmin()
        if not is_admin:
            # If not admin, try to elevate privileges
            script = os.path.abspath(sys.argv[0])
            params = ' '.join([script] + sys.argv[1:])
            try:
                ret = shell.ShellExecuteEx(lpVerb='runas',
                                         lpFile=sys.executable,
                                         lpParameters=params)
                sys.exit()
            except Exception as e:
                # Log the error and show message box
                error_msg = f"Failed to obtain admin rights: {str(e)}"
                print(error_msg)  # This will be captured in a log file
                messagebox.showerror("Admin Rights Required", 
                                   "This application needs to run with administrative privileges.\n"
                                   f"Error: {str(e)}")
                sys.exit(1)
        else:
            # Create log directory if it doesn't exist
            log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')
            os.makedirs(log_dir, exist_ok=True)
            
            # Redirect stdout and stderr to a log file
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            log_file = os.path.join(log_dir, f'tidizzle_{timestamp}.log')
            sys.stdout = open(log_file, 'w')
            sys.stderr = sys.stdout
            
            print(f"Application started at {datetime.now()}")
            
            root = tk.Tk()
            app = CleanerGUI(root)
            root.mainloop()
            
    except Exception as e:
        error_msg = f"Critical error: {str(e)}"
        print(error_msg)  # This will be captured in the log file
        messagebox.showerror("Error", error_msg)
        sys.exit(1)

if __name__ == "__main__":
    run_as_admin()