import glob
import fileinput

# Set the search string and file extension
search_string = "required_version"
file_extension = "*.tf"

# Find all files with the specified extension
files = glob.glob(file_extension)
print(files)

# Loop through each file and search for the string
found = False
for line in fileinput.input(files, inplace=True):
    if search_string in line:
        # Replace the string with a new value
        # line = line.replace(search_string, "new value")
        # print(f"found {search_string} in {line} in {files}")
        found = True
    # Print the line to stdout
    print(line, end="")

if found:
    print(f"found {search_string} in {files}")
