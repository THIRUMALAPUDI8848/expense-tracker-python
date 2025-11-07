import sqlite3
import csv

# Connect to your SQLite database
conn = sqlite3.connect('expenses.db')
cursor = conn.cursor()

# Fetch all data from expenses table
cursor.execute('SELECT * FROM expenses')
rows = cursor.fetchall()

# Get column names
column_names = [description[0] for description in cursor.description]
# Calculate total of the last column (amount)
# Each row = (id, date, category, description, amount)
total = sum([row[4] for row in rows]) if rows else 0

# Write to CSV file
with open('expenses.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(column_names)  # Write header row
    writer.writerows(rows)         # Write data rows

conn.close()
print(" Data exported successfully to 'expenses.csv'")