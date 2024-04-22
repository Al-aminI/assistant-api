import os

# Display the current environment variables
print("Before deletion:")
for key, value in os.environ.items():
    print(f"{key}: {value}")

# Specify the variable you want to remove
variable_to_remove = "env name"

# Check if the variable exists before removing it
if variable_to_remove in os.environ:
    del os.environ[variable_to_remove]
    print(f"\n{variable_to_remove} has been removed from the environment.\n")
else:
    print(f"\n{variable_to_remove} does not exist in the environment.\n")

# Display the environment variables after deletion
print("After deletion:")
for key, value in os.environ.items():
    print(f"{key}: {value}")
