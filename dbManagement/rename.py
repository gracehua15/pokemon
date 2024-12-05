import os

folder = '/workspaces/139649920/pokemon/dbManagement/Pokemon'

for filename in os.listdir(folder):
    if '-' in filename:
        new_name = filename.split('-')[0] + ".jpg"  # Adjust the extension as needed
        os.rename(os.path.join(folder, filename), os.path.join(folder, new_name))
