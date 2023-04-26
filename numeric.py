version_string = "1.2"

# Split the version string into its parts and extract the value
version_parts = version_string.split(" ")
if len(version_parts) == 2:
    semver_version = version_parts[1]
    print(semver_version)
if len(version_parts) == 1:
    print(isfloat(version_parts[0]))
    if version_parts[0].isnumeric() or isfloat(version_parts[0]):
        semver_version = version_parts[0]
        print(semver_version)
else:
    print("No semver version found in input string")


def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False
