import csv
# Create extended data for the table
extended_data = []

#Different conference games - 2 games x 15 games
for b in range(30, 15, -1):  # From 30 down to 16 (inclusive)
    for a in range(1, 16):   # Numbers 1 through 15
        extended_data.append((a, b))
for d in range(1, 16):  # From 1 up to 15 (inclusive)
    for c in range(16, 31):  # Numbers 16 through 30
        extended_data.append((c, d))

#Same division games - 4 games x 4 teams
#Includes games where a single team is both home and away and will need to be deleted in the data_manager
for div_1_home in range(1,5):
    for div_1_away in range(1,5):
        extended_data.append((div_1_home, div_1_away))
        extended_data.append((div_1_home, div_1_away))

for div_2_home in range(5,11):
    for div_2_away in range(5,11):
        extended_data.append((div_2_home, div_2_away))
        extended_data.append((div_2_home, div_2_away))

for div_3_home in range(11,16):
    for div_3_away in range(11,16):
        extended_data.append((div_3_home, div_3_away))
        extended_data.append((div_3_home, div_3_away))

for div_4_home in range(16,21):
    for div_4_away in range(16,21):
        extended_data.append((div_4_home, div_4_away))
        extended_data.append((div_4_home, div_4_away))

for div_5_home in range(21,26):
    for div_5_away in range(21,26):
        extended_data.append((div_5_home, div_5_away))
        extended_data.append((div_5_home, div_5_away))

for div_6_home in range(26,31):
    for div_6_away in range(26,31):
        extended_data.append((div_6_home, div_6_away))
        extended_data.append((div_6_home, div_6_away))

# Define the file path for the extended table
extended_file_path = r"C:\Users\georg\Desktop\nonconference.csv"

# Write extended data to the CSV file
with open(extended_file_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['A', 'B'])  # Write the header
    writer.writerows(extended_data)  # Write the extended data rows

