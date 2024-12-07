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
        self.root.title("Tidizzle My Wizzle")
        self.root.geometry("800x600")
        
        self.setup_gui()
        self.logger.log("Application started", "INFO")
        
    def setup_gui(self):
        # Create main container
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Create canvas for scrolling
        canvas = tk.Canvas(main_frame)
        scrollbar = tk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        
        # Create top frame for checkboxes (now inside a scrollable frame)
        self.top_frame = tk.Frame(canvas)
        
        # Configure the canvas
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack scrollbar and canvas
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        
        # Create window inside canvas
        canvas_frame = canvas.create_window((0,0), window=self.top_frame, anchor="nw")
        
        # Setup logger below the scrollable area
        self.logger = Logger(main_frame)
        
        # Initialize cleaner
        self.cleaner = Cleaner(self.logger)
        
        # Setup path selection
        self.setup_path_selection()
        
        # Configure canvas scrolling region whenever the frame size changes
        def configure_scroll_region(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        
        def configure_canvas_width(event):
            canvas.itemconfig(canvas_frame, width=event.width)
        
        self.top_frame.bind("<Configure>", configure_scroll_region)
        canvas.bind("<Configure>", configure_canvas_width)
        
        # Bind mouse wheel to scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
    
    def setup_path_selection(self):
        # Add Select All checkbox
        self.select_all_var = tk.BooleanVar()
        select_all_chk = tk.Checkbutton(
            self.top_frame, 
            text="Select All",
            variable=self.select_all_var,
            command=self.toggle_all_paths
        )
        select_all_chk.pack(anchor="w")
        
        # Get all paths
        self.paths_to_clean = get_paths_to_clean()
        self.path_vars = []
        
        # Create category frames
        categories = {
            "System Temps": [p for p in self.paths_to_clean if any(x in p for x in ['Windows\\Temp', 'Local\\Temp', 'Recycle.Bin'])],
            "Browsers": [p for p in self.paths_to_clean if any(x in p for x in ['Chrome', 'Edge', 'Firefox'])],
            "VS Code": [p for p in self.paths_to_clean if 'Code' in p],
            "Windows System": [p for p in self.paths_to_clean if any(x in p for x in ['Windows', 'Explorer', 'INetCache', 'Prefetch'])]
        }
        
        # Create frames for each category
        for category, paths in categories.items():
            if paths:  # Only create frame if there are paths in this category
                category_frame = tk.LabelFrame(self.top_frame, text=category, padx=5, pady=5)
                category_frame.pack(fill="x", padx=5, pady=5)
                
                for path in paths:
                    var = tk.BooleanVar()
                    chk = tk.Checkbutton(category_frame, text=path, variable=var)
                    chk.pack(anchor="w")
                    self.path_vars.append((var, path))
            
        tk.Button(self.top_frame, text="Clean Selected Paths", 
                command=self.execute_clean).pack(pady=10)
    
    def toggle_all_paths(self):
        """Toggle all path checkboxes based on Select All state"""
        state = self.select_all_var.get()
        for var, _ in self.path_vars:
            var.set(state)
    
    def execute_clean(self):
        # Indent the following lines by 4 spaces inside this method.
        selected_paths = [
            path for var, path in self.path_vars
            if var.get()
        ]
        
        self.logger.log(f"Selected paths for cleaning: {len(selected_paths)}", "INFO")
        
        if not selected_paths:
            self.logger.log("No paths selected for cleaning", "WARN")
            messagebox.showinfo("Info", "No paths selected for cleaning.")
            return
        
        # Ask for bulk confirmation if multiple paths are selected
        if len(selected_paths) > 1:
            confirm_msg = f"You have selected {len(selected_paths)} paths to clean.\nDo you want to approve all deletions at once?"
            bulk_confirm = messagebox.askyesnocancel("Confirm Bulk Operation", confirm_msg)
            
            if bulk_confirm is None:  # User clicked Cancel
                self.logger.log("Cleaning operation cancelled by user", "INFO")
                return
            
            self.cleaner.confirm_all = bulk_confirm
        
        paths_cleaned = []
        paths_failed = []
        
        # Process Recycle Bin first if it's in the selection
        bin_path = r"C:\$Recycle.Bin"
        if bin_path in selected_paths:
            if self.cleaner.clean_path(bin_path):
                paths_cleaned.append(bin_path)
                self.logger.log(f"Successfully cleaned: {bin_path}", "SUCCESS")
            else:
                paths_failed.append(bin_path)
                self.logger.log(f"Failed to clean: {bin_path}", "ERROR")
            selected_paths.remove(bin_path)
        
        # Then process remaining paths
        for path in selected_paths:
            try:
                if self.cleaner.clean_path(path):
                    paths_cleaned.append(path)
                    self.logger.log(f"Successfully cleaned: {path}", "SUCCESS")
                else:
                    paths_failed.append(path)
                    self.logger.log(f"Failed to clean: {path}", "ERROR")
            except Exception as e:
                paths_failed.append(path)
                self.logger.log(f"Error during cleaning {path}: {str(e)}", "ERROR")
        
        self.show_report(paths_cleaned, paths_failed)

    def show_report(self, paths_cleaned, paths_failed):
        # This method should be aligned at the same indentation level as other methods in the class.
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
