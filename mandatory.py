import os
import csv

def find_common_lines(folder):
    # Get all CSV files in the folder
    files = [f for f in os.listdir(folder) if f.endswith(".csv")]
    if not files:
        print("No CSV files found in the folder.")
        return

    # Initialize a set to store common lines
    common_lines = None

    # Process each file
    for file in files:
        file_path = os.path.join(folder, file)
        with open(file_path, 'r') as csvfile:
            reader = csv.reader(csvfile)
            # Skip the header row
            next(reader, None)
            # Read all lines in the current file
            lines = set(tuple(row) for row in reader)
            # Intersect with the common lines set
            if common_lines is None:
                common_lines = lines
            else:
                common_lines &= lines

    # Print the common lines
    if common_lines:
        print("Lines common to all files:")
        for line in common_lines:
            print(",".join(line))
    else:
        print("No common lines found across all files.")

if __name__ == "__main__":
    solutions_folder = "solutions"
    find_common_lines(solutions_folder)