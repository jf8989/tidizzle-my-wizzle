import tkinter as tk
import datetime

class Logger:
    def __init__(self, root):
        self.setup_text_widget(root)

    def setup_text_widget(self, root):
        # Create main container frame
        self.frame = tk.Frame(root)
        self.frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Create text widget with scrollbar
        self.text_widget = tk.Text(self.frame, height=10, width=50, wrap=tk.WORD)
        self.scrollbar = tk.Scrollbar(self.frame, command=self.text_widget.yview)
        self.text_widget.configure(yscrollcommand=self.scrollbar.set)
        
        self.text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def log(self, message, level="INFO"):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        tag_colors = {
            "ERROR": "red",
            "SUCCESS": "green",
            "INFO": "black",
            "DEBUG": "purple",
            "WARN": "orange"
        }
        
        message_with_timestamp = f"[{timestamp}] [{level}] {message}\n"
        self.text_widget.insert(tk.END, message_with_timestamp)
        self.text_widget.tag_add(level, f"end-{len(message_with_timestamp)+1}c", "end-1c")
        self.text_widget.tag_config(level, foreground=tag_colors.get(level, "black"))
        self.text_widget.see(tk.END)