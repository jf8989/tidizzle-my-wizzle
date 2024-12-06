"""
File: src/logger.py
Project: Tidizzle My Wizzle
Description: Custom logging implementation with GUI integration and file logging capabilities.
Author: [Your Name]
Date: [Current Date]
"""

import os
import tkinter as tk
from datetime import datetime
from typing import Optional, Dict, Union

class Logger:
    def __init__(self, root: Union[tk.Tk, tk.Frame]):
        """
        Initialize the logger with both GUI and file logging capabilities.
        
        Args:
            root (Union[tk.Tk, tk.Frame]): The root tkinter window or frame for GUI logging
        """
        self.setup_text_widget(root)
        self.setup_file_logging()
        
        # Log initial message
        self.log("Logger initialized successfully", "INFO")
        
    def setup_text_widget(self, root: Union[tk.Tk, tk.Frame]) -> None:
        """
        Setup the text widget for GUI logging.
        
        Args:
            root (Union[tk.Tk, tk.Frame]): The root tkinter window or frame
        """
        try:
            # Create main container frame
            self.frame = tk.Frame(root)
            self.frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
            
            # Create text widget with scrollbar
            self.text_widget = tk.Text(self.frame, height=10, width=50, wrap=tk.WORD)
            self.scrollbar = tk.Scrollbar(self.frame, command=self.text_widget.yview)
            self.text_widget.configure(yscrollcommand=self.scrollbar.set)
            
            # Pack widgets
            self.text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
        except Exception as e:
            print(f"Error setting up text widget: {str(e)}")
            raise

    def setup_file_logging(self) -> None:
        """
        Setup file logging with automatic directory creation and rotation.
        """
        try:
            # Create logs directory in the same directory as the script
            self.log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')
            os.makedirs(self.log_dir, exist_ok=True)
            
            # Create new log file with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            self.log_file = os.path.join(self.log_dir, f'tidizzle_{timestamp}.log')
            
            # Create the file and write header
            with open(self.log_file, 'w', encoding='utf-8') as f:
                f.write(f"Log started at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("-" * 80 + "\n")
                
        except Exception as e:
            print(f"Error setting up file logging: {str(e)}")
            raise

    def log(self, message: str, level: str = "INFO") -> None:
        """
        Log a message to both GUI and file with timestamp and level.
        
        Args:
            message (str): The message to log
            level (str): The logging level (INFO, ERROR, SUCCESS, DEBUG, WARN)
        """
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            tag_colors: Dict[str, str] = {
                "ERROR": "red",
                "SUCCESS": "green",
                "INFO": "black",
                "DEBUG": "purple",
                "WARN": "orange"
            }
            
            # Format message with timestamp and level
            message_with_timestamp = f"[{timestamp}] [{level}] {message}\n"
            
            # Log to GUI
            self.log_to_gui(message_with_timestamp, level, tag_colors)
            
            # Log to file
            self.log_to_file(message_with_timestamp)
            
        except Exception as e:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            error_message = f"[{timestamp}] [ERROR] Logging error: {str(e)}\n"
            # Attempt to write to file directly in case of GUI error
            self.log_to_file(error_message)

    def log_to_gui(self, message: str, level: str, tag_colors: Dict[str, str]) -> None:
        """
        Log a message to the GUI text widget.
        
        Args:
            message (str): The formatted message to log
            level (str): The logging level
            tag_colors (Dict[str, str]): Dictionary mapping levels to colors
        """
        try:
            self.text_widget.insert(tk.END, message)
            self.text_widget.tag_add(level, f"end-{len(message)+1}c", "end-1c")
            self.text_widget.tag_config(level, foreground=tag_colors.get(level, "black"))
            self.text_widget.see(tk.END)
        except Exception as e:
            print(f"Error logging to GUI: {str(e)}")
            raise

    def log_to_file(self, message: str) -> None:
        """
        Log a message to the log file.
        
        Args:
            message (str): The formatted message to log
        """
        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(message)
        except Exception as e:
            print(f"Error logging to file: {str(e)}")
            raise

    def get_log_file_path(self) -> str:
        """
        Get the current log file path.
        
        Returns:
            str: The path to the current log file
        """
        return self.log_file

    def clear_gui_log(self) -> None:
        """
        Clear the GUI text widget.
        """
        try:
            self.text_widget.delete('1.0', tk.END)
            self.log("Log cleared", "INFO")
        except Exception as e:
            print(f"Error clearing GUI log: {str(e)}")
            raise