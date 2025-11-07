import csv
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
# app.py
from models import add_expense, get_all_expenses, search_by_category, total_expense

def print_expense(row):
    print(f"ID: {row['id']}\tDate: {row['date']}\tCategory: {row['category']}\tDescription: {row['description']}\tAmount: {row['amount']}")

def menu():
    while True:
        print("\n=== Expense Tracker ===")
        print("1. Add expense")
        print("2. View all expenses")
        print("3. Search by category")
        print("4. Show total expense")
        print("5. View Category-wise Chart")
        print("6. View Monthly Expense Chart")
        print("7. Export Data (csv / Excel")
        print("8. Exit")
        
        choice = input("Enter choice: ").strip()

        if choice == "1":
            date = input("Date (YYYY-MM-DD): ")
            category = input("Category (e.g., Food, Travel): ")
            description = input("Description: ")
            amount = float(input("Amount: "))
            add_expense(date, category, description, amount)
            print("Expense added successfully!")

        elif choice == "2":
            expenses = get_all_expenses()
            if not expenses:
                print("No expenses found.")
            for row in expenses:
                print_expense(row)

        elif choice == "3":
            cat = input("Enter category to search: ")
            results = search_by_category(cat)
            if not results:
                print("No expenses found in this category.")
            for row in results:
                print_expense(row)

        elif choice == "4":
            total = total_expense()
            print(f"Total Expense: {total}")
        
        elif choice == "5":
            show_category_chart()
            break
        
        elif choice == "6":
            show_monthly_chart()

        elif choice == "7":
            export_data()
         
        elif choice == "8":
            print("Goodbye!")
        else:
            print("Invalid choice. Try again.")

def show_category_chart():
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

    plt.figure(figsize=(8,5))
    plt.bar(categories, totals, color='teal')
    plt.title("Expenses by Category", fontsize=14, fontweight='bold')
    plt.xlabel("Category")
    plt.ylabel("Total Spent (₹)")
    plt.tight_layout()
    plt.show()
   
def show_monthly_chart():
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            SUBSTR(date, 1, 7) AS month, 
            SUM(amount) AS total
        FROM expenses
        GROUP BY month
        ORDER BY month;
    """)
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        print("No expenses found to display.")
        return

    months = [r[0] for r in rows]
    totals = [r[1] for r in rows]

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

def export_data():
    print("\nChoose export format:")
    print("1. Export to CSV")
    print("2. Export to Excel")
    choice = input("Enter choice: ").strip()

    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM expenses")
    rows = cursor.fetchall()
    column_names = [desc[0] for desc in cursor.description]
    conn.close()

    if not rows:
        print("No data to export.")
        return

    if choice == "1":
        # Export to CSV
        with open("expenses_export.csv", "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(column_names)
            writer.writerows(rows)
        print(" Data exported to 'expenses_export.csv' successfully!")

    elif choice == "2":
        # Export to Excel (needs pandas)
        df = pd.DataFrame(rows, columns=column_names)
        total_amount = df['amount'].sum()

    # Add a blank row and a total row
        total_row = pd.DataFrame([{"id": "", "date": "", "category": "",    "description": "Total", "amount": total_amount}])
        df = pd.concat([df, total_row], ignore_index=True)
        df.to_excel("expenses_export.xlsx", index=False)
        print(" Data exported to 'expenses_export.xlsx' successfully!")

    else:
        print("Invalid choice.")

 
if __name__ == "__main__":

    menu()
     
