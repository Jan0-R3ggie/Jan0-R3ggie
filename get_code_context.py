import os

# Specify the project directory
project_dir = r"C:\Users\User\OneDrive\Desktop\Projects\SBA_cliniek\SB_Cliniek#2\Final_V2"

# Use a fixed name for the output file in the current directory
output_file = os.path.join(project_dir, "code_context.txt")

# Remove the output file if it exists
if os.path.exists(output_file):
    os.remove(output_file)

def read_files():
    for root, dirs, files in os.walk(project_dir):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, project_dir)
                print(f"Including file: {relative_path}")
                with open(output_file, "a", encoding="utf-8") as f:
                    f.write(f"// File: {relative_path}\n")
                    with open(file_path, "r", encoding="utf-8") as source_file:
                        f.write(source_file.read())
                    f.write("\n")

# Call the function to read the Python files
read_files()
print("Done.")