"""
File: src/gui.py
Project: Tidizzle My Wizzle
Description: Main GUI implementation using tkinter.
Author: [Your Name]
Date: [Current Date]
"""

import tkinter as tk
from tkinter import messagebox
from .logger import Logger
import os
from .cleaner import Cleaner
from .utils import get_paths_to_clean, calculate_path_size

class CleanerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Tidizzle My Wizzle Cleaner")
        self.root.geometry("800x600")
        
        self.setup_gui()
        self.logger.log("Application started", "INFO")
        
    def setup_gui(self):
        # Create main container
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Create top frame for checkboxes
        self.top_frame = tk.Frame(main_frame)
        self.top_frame.pack(fill=tk.X, pady=5)
        
        # Setup logger
        self.logger = Logger(main_frame)
        
        # Initialize cleaner
        self.cleaner = Cleaner(self.logger)
        
        # Setup path selection
        self.setup_path_selection()
        
    def setup_path_selection(self):
        tk.Label(self.top_frame, text="Select paths to clean:").pack(anchor="w")
        
        self.paths_to_clean = get_paths_to_clean()
        self.path_vars = []
        
        for path in self.paths_to_clean:
            var = tk.BooleanVar()
            chk = tk.Checkbutton(self.top_frame, text=path, variable=var)
            chk.pack(anchor="w")
            self.path_vars.append(var)
            
        tk.Button(self.top_frame, text="Clean Selected Paths", 
                 command=self.execute_clean).pack(pady=10)
        
    def execute_clean(self):
        selected_paths = [
            path for path, var in zip(self.paths_to_clean, self.path_vars)
            if var.get()
        ]
        
        self.logger.log(f"Selected paths for cleaning: {len(selected_paths)}", "INFO")
        
        if not selected_paths:
            self.logger.log("No paths selected for cleaning", "WARN")
            messagebox.showinfo("Info", "No paths selected for cleaning.")
            return

        paths_cleaned = []
        paths_failed = []

        for path in selected_paths:
            if self.cleaner.clean_path(path):
                paths_cleaned.append(path)
                self.logger.log(f"Successfully cleaned: {path}", "SUCCESS")
            else:
                paths_failed.append(path)
                self.logger.log(f"Failed to clean: {path}", "ERROR")

        self.show_report(paths_cleaned, paths_failed)

    def show_report(self, paths_cleaned, paths_failed):
        total_space_freed = sum(
            calculate_path_size(path) for path in paths_cleaned
            if os.path.exists(path)
        )

        report = "Paths cleaned successfully:\n"
        for path in paths_cleaned:
            report += f"  - {path}\n"

        if paths_failed:
            report += "\nPaths not found or inaccessible:\n"
            for path in paths_failed:
                report += f"  - {path}\n"

        report += f"\nTotal disk space freed: {total_space_freed / (1024 * 1024):.2f} MB"
        
        self.logger.log("Cleaning operation completed", "INFO")
        self.logger.log(report, "INFO")
        messagebox.showinfo("Cleaning Report", report)