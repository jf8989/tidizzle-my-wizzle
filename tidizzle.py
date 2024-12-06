import os
import shutil
import tkinter as tk
from tkinter import messagebox

def validate_path(path):
    if os.path.exists(path):
        return True
    else:
        print(f"[INFO] Path not found: {path}")
        return False

def clean_path(path):
    if validate_path(path):
        user_input = input(f"[CONFIRM] Do you want to delete '{path}'? (yes/no): ").strip().lower()
        if user_input == 'yes':
            try:
                if os.path.isdir(path):
                    shutil.rmtree(path)
                    print(f"[SUCCESS] Cleaned: {path}")
                elif os.path.isfile(path):
                    os.remove(path)
                    print(f"[SUCCESS] Deleted File: {path}")
            except Exception as e:
                print(f"[ERROR] Could not delete {path}: {str(e)}")
        else:
            print(f"[SKIP] Skipped: {path}")

def generate_report(paths_cleaned, paths_failed):
    print("\n[REPORT] Paths cleaned successfully:")
    for path in paths_cleaned:
        print(f"  - {path}")

    print("\n[REPORT] Paths not found or inaccessible:")
    for path in paths_failed:
        print(f"  - {path}")

def main():
    paths_to_clean = [
        r"C:\Windows\Temp",
        r"C:\Users\YourUser\AppData\Local\Temp",
        # Add more paths from your list here
    ]

    paths_cleaned = []
    paths_failed = []

    for path in paths_to_clean:
        if validate_path(path):
            clean_path(path)
            paths_cleaned.append(path)
        else:
            paths_failed.append(path)

    generate_report(paths_cleaned, paths_failed)

def run_gui():
    paths_to_clean = [
        r"C:\Windows\Temp",
        r"C:\Users\YourUser\AppData\Local\Temp",
        r"C:\$Recycle.Bin",
        r"C:\Users\YourUser\AppData\Local\Google\Chrome\User Data\Default\Cache",
        r"C:\Users\YourUser\AppData\Local\Microsoft\Edge\User Data\Default\Cache",
        r"C:\Users\YourUser\AppData\Local\Mozilla\Firefox\Profiles\[Perfil]\cache2",
    ]

    def execute_clean():
        selected_paths = []
        for index, path_var in enumerate(path_vars):
            if path_var.get():
                selected_paths.append(paths_to_clean[index])

        if not selected_paths:
            messagebox.showinfo("Info", "No paths selected for cleaning.")
            return

        paths_cleaned = []
        paths_failed = []

        for path in selected_paths:
            if validate_path(path):
                clean_path(path)
                paths_cleaned.append(path)
            else:
                paths_failed.append(path)

        # Show summary report
        report = "Paths cleaned successfully:\n"
        for path in paths_cleaned:
            report += f"  - {path}\n"

        report += "\nPaths not found or inaccessible:\n"
        for path in paths_failed:
            report += f"  - {path}\n"

        messagebox.showinfo("Cleaning Report", report)

    root = tk.Tk()
    root.title("Tidizzle My Wizzle Cleaner")

    tk.Label(root, text="Select paths to clean:").pack(anchor="w")

    path_vars = []
    for path in paths_to_clean:
        var = tk.BooleanVar()
        chk = tk.Checkbutton(root, text=path, variable=var)
        chk.pack(anchor="w")
        path_vars.append(var)

    tk.Button(root, text="Clean Selected Paths", command=execute_clean).pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    run_gui()  # Run the GUI for now
