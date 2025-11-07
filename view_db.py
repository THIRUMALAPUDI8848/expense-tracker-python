import sqlite3

# Connect to your expense tracker database
conn = sqlite3.connect('expenses.db')

# Execute SQL query to fetch all data from the expenses table
cursor = conn.cursor()
cursor.execute('SELECT * FROM expenses')

# Print each row
print("\n=== All Expenses in Database ===")
for row in cursor.fetchall():
    print(row)

# Close the connection
conn.close()