import os
import shutil

def validate_path(path):
    if os.path.exists(path):
        return True
    else:
        print(f"[INFO] Path not found: {path}")
        return False

def clean_path(path):
    if validate_path(path):
        try:
            # Only delete if it's a directory (safe guard)
            if os.path.isdir(path):
                shutil.rmtree(path)
                print(f"[SUCCESS] Cleaned: {path}")
            elif os.path.isfile(path):
                os.remove(path)
                print(f"[SUCCESS] Deleted File: {path}")
        except Exception as e:
            print(f"[ERROR] Could not delete {path}: {str(e)}")

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

if __name__ == "__main__":
    main()
