##DEPRECATED IN FAVOR OF HARDCODED SCHEDULE 


import csv
# Create extended data for the table
extended_data = []
for b in range(30, 15, -1):  # From 30 down to 16 (inclusive)
    for a in range(1, 16):   # Numbers 1 through 15
        extended_data.append((a, b))
for d in range(1, 16):  # From 1 up to 15 (inclusive)
    for c in range(16, 31):  # Numbers 16 through 30
        extended_data.append((c, d))



# Define the file path for the extended table
extended_file_path = r"C:\Users\georg\Desktop\nonconference.csv"

# Write extended data to the CSV file
with open(extended_file_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['A', 'B'])  # Write the header
    writer.writerows(extended_data)  # Write the extended data rows

