import os

def create_folders_and_files():
    # Ask for the main folder name
    folder_name = input("What is the folder name? ").strip()
    if not folder_name:
        print("Error: Folder name cannot be empty.")
        return

    # Create the main folder (if it doesn't exist)
    os.makedirs(folder_name, exist_ok=True)
    print(f"Folder '{folder_name}' is ready.")

    # Ask for file names
    files_input = input("What are the files to create in the folder? (Separate by commas): ").strip()
    if not files_input:
        print("No files specified. Exiting.")
        return

    # Split input by commas and clean up each filename
    raw_filenames = [name.strip() for name in files_input.split(',') if name.strip()]

    # Validate and create each file
    for raw_name in raw_filenames:
        # Ensure the name contains a dot and has a non-empty extension
        if '.' not in raw_name or raw_name.startswith('.') or raw_name.endswith('.'):
            print(f"Skipping invalid filename: '{raw_name}' (must contain a valid extension like 'file.txt')")
            continue

        # Construct full path
        file_path = os.path.join(folder_name, raw_name)

        # Avoid overwriting existing files (optional: remove this if overwriting is acceptable)
        if os.path.exists(file_path):
            print(f"File '{raw_name}' already exists. Skipping.")
            continue

        # Create the file (empty)
        try:
            with open(file_path, 'w') as f:
                pass  # Creates an empty file
            print(f"Created file: '{raw_name}'")
        except OSError as e:
            print(f"Failed to create file '{raw_name}': {e}")

if __name__ == "__main__":
    create_folders_and_files()
