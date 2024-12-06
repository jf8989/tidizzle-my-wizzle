import os
import sys
import tkinter as tk
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
                messagebox.showerror("Admin Rights Required", 
                                   "This application needs to run with administrative privileges.\n"
                                   f"Error: {str(e)}")
                sys.exit(1)
        else:
            root = tk.Tk()
            app = CleanerGUI(root)
            root.mainloop()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to check/obtain admin rights: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    run_as_admin()