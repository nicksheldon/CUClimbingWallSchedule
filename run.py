from z3 import *
import csv
import os
import shutil

def run_schedule(run_number, staff_availability, shift_letters, days, x):
    # Create new optimizer and add constraints.
    opt = Optimize()

    # Hard constraint: Each staff must be assigned exactly two shifts.
    for staff, allowed in staff_availability.items():
        available_shifts = [shift for shift in allowed if shift in shift_letters]
        terms = [If(x[(staff, shift)], 1, 0) for shift in available_shifts]
        opt.add(Sum(terms) == 2)

    # Hard constraint: Each shift must have exactly two staff assigned.
    for shift in shift_letters:
        terms = []
        for staff, allowed in staff_availability.items():
            if shift in allowed:
                terms.append(If(x[(staff, shift)], 1, 0))
        opt.add(Sum(terms) == 2)

    # Soft constraint: minimize staff having multiple shifts on the same day.
    penalty_terms = []
    for staff, allowed in staff_availability.items():
        for day, shifts in days.items():
            available_shifts = [shift for shift in allowed if shift in shifts]
            if available_shifts:
                assigned = [If(x[(staff, shift)], 1, 0) for shift in available_shifts]
                count = Sum(assigned)
                penalty = If(count > 1, count - 1, 0)
                penalty_terms.append(penalty)
    opt.minimize(Sum(penalty_terms))

    # Solve the constraints.
    if opt.check() == sat:
        model = opt.model()
        # Build a dictionary of shift assignments.
        shift_assignments = {}
        for shift in shift_letters:
            assigned_staff = []
            for staff, allowed in staff_availability.items():
                if shift in allowed and model.evaluate(x[(staff, shift)]):
                    assigned_staff.append(staff)
            shift_assignments[shift] = assigned_staff
        return shift_assignments
    else:
        return None

def check_duplicate_solutions():
    folder = "solutions"
    files = [f for f in os.listdir(folder) if f.endswith(".csv")]
    seen = {}
    for f in files:
        path = os.path.join(folder, f)
        with open(path, 'r') as file:
            content = file.read().strip()
        if content in seen:
            os.remove(path)
            print(f"Removed duplicate solution: {f}")
        else:
            seen[content] = f

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
        for line in common_lines:
            print(",".join(line))
    else:
        print("No common lines found across all files.")

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

def main():
    # Ensure the solutions folder exists and is empty
    solutions_folder = "solutions"
    if os.path.exists(solutions_folder):
        shutil.rmtree(solutions_folder)  # Remove the folder and its contents
    os.makedirs(solutions_folder)  # Create a fresh, empty folder

    # Build a dictionary {staff: set(allowed_shifts)}
    staff_availability = {}
    with open('responses.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if len(row) < 3:
                continue
            name = row[1].strip()
            allowed_str = row[2].strip().strip('"')
            allowed_shifts = {s.strip() for s in allowed_str.split(',')}
            staff_availability[name] = allowed_shifts

    # Define allowed shift letters A-R.
    shift_letters = [chr(x) for x in range(ord('A'), ord('R') + 1)]

    # Define days and their shifts.
    days = {
        "Monday": {"A", "B", "C", "D"},
        "Tuesday": {"E", "F", "G", "H"},
        "Wednesday": {"I", "J", "K"},
        "Thursday": {"L", "M", "N", "O"},
        "Friday": {"P", "Q", "R"}
    }

    # Create Boolean variables for each (staff, shift) pair where shift is available.
    # We'll reuse the same variables x across runs.
    x = {}
    for staff, allowed in staff_availability.items():
        for shift in allowed:
            if shift in shift_letters:
                x[(staff, shift)] = Bool(f"{staff}_{shift}")

    # Ensure the solutions folder exists.
    os.makedirs("solutions", exist_ok=True)

    # Run the schedule 10 times and store each result.
    print("Searching:")
    for i in range(10):
        result = run_schedule(i, staff_availability, shift_letters, days, x)
        filename = os.path.join("solutions", f"solution_{i+1}.csv")
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL)
            #writer.writerow(["Shift", "Staff", "Staff"])
            if result is not None:
                for shift in shift_letters:
                    assigned = result.get(shift, [])
                    # Ensure exactly two staff are written, even if the result is incomplete.
                    first_staff = assigned[0] if len(assigned) > 0 else ""
                    second_staff = assigned[1] if len(assigned) > 1 else ""
                    writer.writerow([shift, first_staff, second_staff])
            else:
                writer.writerow(["No solution found", "", ""])
        print(f"Solution {i+1} saved to {filename}")

    # After generating the files, remove duplicate csvs.
    check_duplicate_solutions()

    print("********************************************")
    print("The following assignments are mandatory:")
    find_common_lines("solutions")
    print("********************************************")
    print("Now clean up your mess")
    print("Save your solutions and press 'enter' to reset:")
    # Wait for Enter key press to call the cleanup function
    while True:
        user_input = input()
        if user_input == "":
            clear_solutions("solutions")
            print("Solutions folder has been cleared.")
            break
        elif user_input == "help":
            print("Ask nick, and try again")
        else:
            print("Wrong key. Just press 'Enter' :/")

if __name__ == "__main__":
    main()

    # After exiting the while loop, create the "whats_left.txt" file
    with open(os.path.join("solutions", "whats_left.txt"), "w") as file:
        file.write("wrong way")