import re
import os


# Import secret patterns for detecting sensitive information
from sensitive_info_detector.patterns import secret_patterns


# function to check for sensitive information from demo.txt
def check_for_secrets(file_path):
    try:
        with open(file_path, "r") as file:
            content = file.read()
            for pattern in secret_patterns:
                # Search for each pattern in the file content
                if re.search(pattern, content):
                    return True
        return False
    # Handle the FileNotFoundError exception
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return False


# file path to be checked for sensitive information
file_path = os.path.join(os.path.dirname(__file__), "demo.txt")
print(check_for_secrets(file_path))
