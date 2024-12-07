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
        self.confirm_all = False

    def clean_path(self, path):
        self.logger.log(f"Starting cleanup process for path: {path}", "INFO")

        if not os.path.exists(path):
            self.logger.log(f"Path validation failed: {path}", "ERROR")
            return False

        self.logger.log(f"Path validation successful: {path}", "DEBUG")

        # Calculate initial size for comparison
        try:
            initial_size = self._calculate_path_size(path)
            self.logger.log(
                f"Initial size of {path}: {initial_size/1024/1024:.2f} MB", "DEBUG"
            )
        except Exception as e:
            self.logger.log(f"Could not calculate initial size: {str(e)}", "WARN")
            initial_size = 0

        # Special handling for Recycle Bin when in bulk mode
        if path == r"C:\$Recycle.Bin" and self.confirm_all:
            try:
                result = self._clean_recycle_bin()
                if result:
                    self.logger.log(
                        "Recycle Bin emptied successfully during bulk operation",
                        "SUCCESS",
                    )
                    return result
            except Exception as e:
                self.logger.log(
                    f"Error cleaning Recycle Bin during bulk operation: {str(e)}",
                    "ERROR",
                )
                return False

        # Skip confirmation if confirm_all is True
        if not self.confirm_all:
            response = messagebox.askyesno(
                "Confirm Deletion", f"Do you want to delete '{path}'?"
            )
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

    def _clean_directory(self, cleaning_path):  # renamed parameter to avoid shadowing
        self.logger.log(f"Cleaning directory: {cleaning_path}", "DEBUG")
        
        # Get the logs directory path
        logs_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')
        
        try:
            for root, dirs, files in os.walk(cleaning_path, topdown=False):
                for name in files:
                    file_path = os.path.join(root, name)
                    # Skip if the file is in our logs directory
                    if logs_dir in file_path:
                        continue
                    try:
                        os.remove(file_path)
                    except Exception as e:
                        self.logger.log(f"Could not remove file {file_path}: {str(e)}", "WARN")
                        
                for name in dirs:
                    dir_path = os.path.join(root, name)
                    # Skip if this is our logs directory
                    if logs_dir in dir_path:
                        continue
                    try:
                        os.rmdir(dir_path)
                    except Exception as e:
                        self.logger.log(f"Could not remove directory {dir_path}: {str(e)}", "WARN")
            
            self.logger.log(f"Directory cleaned successfully: {cleaning_path}", "SUCCESS")
            return True
            
        except Exception as e:
            self.logger.log(f"Error during directory cleanup: {str(e)}", "ERROR")
            return False

    def _clean_file(self, path):
        self.logger.log(f"Deleting file: {path}", "DEBUG")
        os.remove(path)
        self.logger.log(f"File deleted successfully: {path}", "SUCCESS")
        return True

    def _calculate_path_size(self, path):
        return (
            sum(
                os.path.getsize(os.path.join(dirpath, f))
                for dirpath, dirnames, filenames in os.walk(path)
                for f in filenames
            )
            if os.path.isdir(path)
            else os.path.getsize(path)
        )
