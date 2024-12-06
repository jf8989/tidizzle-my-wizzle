"""
File: src/cleaner.py
Project: Tidizzle My Wizzle
Description: Core cleaning functionality implementation.
Author: [Your Name]
Date: [Current Date]
"""

import os
import shutil
from win32com.shell import shell, shellcon
from tkinter import messagebox

class Cleaner:
    def __init__(self, logger):
        self.logger = logger

    def clean_path(self, path):
        self.logger.log(f"Starting cleanup process for path: {path}", "INFO")
        
        if not os.path.exists(path):
            self.logger.log(f"Path validation failed: {path}", "ERROR")
            return False

        self.logger.log(f"Path validation successful: {path}", "DEBUG")
        
        # Calculate initial size for comparison
        try:
            initial_size = self._calculate_path_size(path)
            self.logger.log(f"Initial size of {path}: {initial_size/1024/1024:.2f} MB", "DEBUG")
        except Exception as e:
            self.logger.log(f"Could not calculate initial size: {str(e)}", "WARN")
            initial_size = 0

        response = messagebox.askyesno("Confirm Deletion", f"Do you want to delete '{path}'?")
        self.logger.log(f"User confirmation for {path}: {'Accepted' if response else 'Declined'}", "DEBUG")
        
        if not response:
            self.logger.log(f"Operation skipped by user: {path}", "INFO")
            return False

        try:
            if path == r"C:\$Recycle.Bin":
                return self._clean_recycle_bin()
            elif os.path.isdir(path):
                return self._clean_directory(path)
            elif os.path.isfile(path):
                return self._clean_file(path)
        except Exception as e:
            error_msg = f"Error cleaning {path}: {str(e)}"
            self.logger.log(error_msg, "ERROR")
            messagebox.showerror("Error", error_msg)
            return False

    def _clean_recycle_bin(self):
        self.logger.log("Attempting to empty Recycle Bin...", "DEBUG")
        try:
            shell.SHEmptyRecycleBin(0, "", shellcon.SHERB_NOCONFIRMATION)
            self.logger.log("Recycle Bin emptied successfully", "SUCCESS")
            return True
        except Exception as e:
            self.logger.log(f"Warning during Recycle Bin operation: {str(e)}", "WARN")
            return True  # Consider successful as files are typically deleted despite API errors

    def _clean_directory(self, path):
        self.logger.log(f"Cleaning directory: {path}", "DEBUG")
        shutil.rmtree(path, ignore_errors=True)
        self.logger.log(f"Directory cleaned successfully: {path}", "SUCCESS")
        return True

    def _clean_file(self, path):
        self.logger.log(f"Deleting file: {path}", "DEBUG")
        os.remove(path)
        self.logger.log(f"File deleted successfully: {path}", "SUCCESS")
        return True

    def _calculate_path_size(self, path):
        return sum(
            os.path.getsize(os.path.join(dirpath, f))
            for dirpath, dirnames, filenames in os.walk(path)
            for f in filenames
        ) if os.path.isdir(path) else os.path.getsize(path)