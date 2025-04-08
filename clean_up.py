import os

def clear_solutions(folder):
    # Get all files in the folder
    files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
    if not files:
        print("No files found in the folder.")
        return

    # Delete each file
    for file in files:
        file_path = os.path.join(folder, file)
        os.remove(file_path)
        print(f"Deleted: {file_path}")

    print("All files in the solutions folder have been deleted.")

if __name__ == "__main__":
    solutions_folder = "solutions"
    if os.path.exists(solutions_folder):
        clear_solutions(solutions_folder)
    else:
        print(f"The folder '{solutions_folder}' does not exist.")