import csv
import os

# Open the original CSV file
with open('pokemon.csv', 'r', encoding='utf-16') as csvfile:
    reader = csv.reader(csvfile, delimiter='\t')
    rows = list(reader)


# Add a header for the image link if not present
if 'image_link' not in rows[0]:
    rows[0].append('image_link')

# Iterate through each row and add the image link
for row in rows[1:]:
    # Check if the row has at least 3 columns (to access row[2])
    if len(row) > 2:
        pokemon_name = row[2].lower()  # Get the Pokemon name and clean up spaces
        image_filename = f"{pokemon_name}.png"  # Adjust the extension if needed
        image_path = os.path.join('static/Pokemon', image_filename)
        row.append(image_path)
    else:
        # Skip rows that don't have enough columns
        print(f"Skipping incomplete row: {row}")

# Write the updated rows to a new CSV file
with open('updated_pokemon.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(rows)
