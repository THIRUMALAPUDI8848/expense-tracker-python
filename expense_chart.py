import sqlite3
import matplotlib.pyplot as plt


# Connect to the database

conn = sqlite3.connect('expenses.db')
cursor = conn.cursor()


# Fetch monthly totals

cursor.execute("""
    SELECT 
        SUBSTR(date, 1, 7) AS month,  -- Extract YYYY-MM from date
        SUM(amount) AS total
    FROM expenses
    GROUP BY month
    ORDER BY month;
""")

rows = cursor.fetchall()
conn.close()

 
# Prepare data for chart
months = [row[0] for row in rows]
totals = [row[1] for row in rows]


# Create bar chart
plt.figure(figsize=(8, 5))
plt.bar(months, totals, color='steelblue')

plt.title("Monthly Expense Chart", fontsize=14, fontweight='bold')
plt.xlabel("Month (YYYY-MM)")
plt.ylabel("Total Expenses (₹)")
plt.grid(axis='y', linestyle='--', alpha=0.6)

# Add values on top of bars
for i, total in enumerate(totals):
    plt.text(i, total + 5, f"₹{total:.2f}", ha='center')

plt.tight_layout()
plt.show()


# Category-wise Expense Chart

conn = sqlite3.connect('expenses.db')
cursor = conn.cursor()

cursor.execute("""
    SELECT category, SUM(amount)
    FROM expenses
    GROUP BY category
    ORDER BY SUM(amount) DESC;
""")
rows = cursor.fetchall()
conn.close()

categories = [r[0] for r in rows]
totals = [r[1] for r in rows]

plt.figure(figsize=(8, 5))
plt.bar(categories, totals, color='teal')
plt.title("Expenses by Category", fontsize=14, fontweight='bold')
plt.xlabel("Category")
plt.ylabel("Total Spent (₹)")
plt.grid(axis='y', linestyle='--', alpha=0.6)
plt.tight_layout()
plt.show()


