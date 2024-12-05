import sqlite3
import csv
import os

# Step 1: Connect to the database
db_path = 'pokemon.db'  # Path to your SQLite database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Step 2: Create the table (if it doesn't already exist)
cursor.execute('''
CREATE TABLE IF NOT EXISTS pokemon (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    national_number INTEGER NOT NULL,
    generation TEXT NOT NULL,
    name TEXT NOT NULL,
    primary_type TEXT NOT NULL,
    secondary_type TEXT NOT NULL,
    description TEXT NOT NULL,
    image_link TEXT NOT NULL
)
''')

# Step 3: Read the CSV and insert its data into the database
csv_file_path = '/workspaces/139649920/pokemon/dbManagement/pokemon_abridged.csv'  # Path to your CSV file

if not os.path.exists(csv_file_path):
    print(f"Error: CSV file not found at {csv_file_path}")
    exit(1)

with open(csv_file_path, 'r', encoding='utf-8', errors='ignore') as csvfile:
    reader = csv.reader(csvfile)
    headers = next(reader)  # Read and skip the header row

    # Insert each row into the database
    for row in reader:
        cursor.execute('''
        INSERT INTO pokemon (national_number, generation, name, primary_type, secondary_type, description, image_link)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', row)

# Step 4: Commit and close the connection
conn.commit()
conn.close()

print("CSV data imported successfully!")
