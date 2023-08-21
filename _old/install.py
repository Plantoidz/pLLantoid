import os
import subprocess

# Step 0: Install the requirements
subprocess.call(['pip3', 'install', '-r', 'requirements.txt'])

# # Optional: Download the nltk stopwords dataset
# import nltk
# nltk.download('stopwords')

print("Packages installed.")

# Step 1: Go up one level and check the 'modes' subdirectory
parent_directory = '..'
modes_subdirectory = os.path.join(parent_directory, 'modes')

# Step 2: Get directory names inside 'modes'
mode_names = []
if os.path.exists(modes_subdirectory):
    mode_names = [name for name in os.listdir(modes_subdirectory) if os.path.isdir(os.path.join(modes_subdirectory, name))]

# Step 3: Check and create the 'working' directory
working_directory = os.path.join(parent_directory, 'working')
if not os.path.exists(working_directory):
    os.makedirs(working_directory)

# Step 4: Create subdirectories mirroring the directory names from 'modes'
for mode_name in mode_names:
    mode_working_directory = os.path.join(working_directory, mode_name)
    
    if not os.path.exists(mode_working_directory):
        os.makedirs(mode_working_directory)

    # Step 5: Create subdirectories 'analysis', 'audio', 'media', 'recordings' inside each directory
    subdirs = ['analysis', 'audio', 'media', 'recordings']
    for subdir in subdirs:
        subdir_path = os.path.join(mode_working_directory, subdir)
        if not os.path.exists(subdir_path):
            os.makedirs(subdir_path)

print("Directories created where necessary.")
print("Installation complete.")
