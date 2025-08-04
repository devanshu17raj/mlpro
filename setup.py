from setuptools import find_packages, setup
from typing import List
import os # Import os module for path handling

HYPEN_E_DOT = '-e .'

def get_requirements(file_path: str) -> List[str]:
    '''
    This function will return the list of requirements by parsing the file.
    It handles newlines, comments, and the '-e .' directive.
    '''
    requirements = []
    with open(file_path) as file_obj:
        lines = file_obj.readlines()
        for line in lines:
            line = line.strip() # Remove leading/trailing whitespace and newline characters

            # Ignore empty lines and lines that are full comments
            if not line or line.startswith('#'):
                continue

            # Remove inline comments (anything after '#')
            if '#' in line:
                line = line.split('#')[0].strip()

            # Skip the editable install directive
            if line == HYPEN_E_DOT:
                continue

            requirements.append(line)

    return requirements

# Get the directory of the current setup.py file
# This helps in locating requirements.txt relative to setup.py
current_dir = os.path.dirname(os.path.abspath(__file__))
requirements_file_path = os.path.join(current_dir, 'requirements.txt')

# Read the requirements from the requirements.txt file using the robust function
install_requires = get_requirements(requirements_file_path)

# You can keep these debug prints temporarily if you want to verify again
print(f"DEBUG: Final install_requires passed to setup(): {install_requires}")

setup(
    name='mlproject',
    version='0.0.1',
    author='devanshu',
    author_email='devanshu17raj@gmail.com',
    packages=find_packages(),
    install_requires=install_requires # Use the parsed and filtered list here
)