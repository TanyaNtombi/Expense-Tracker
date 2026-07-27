import sqlite3


def create_database():
    connection = sqlite3.connect("expenses.db")
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL,
            category TEXT,
            date TEXT,
            description TEXT
        )
    """)

    connection.commit()
    connection.close()


def add_expense(amount, category, date, description):
    connection = sqlite3.connect("expenses.db")
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO expenses (amount, category, date, description)
        VALUES (?, ?, ?, ?)
    """, (amount, category, str(date), description))

    connection.commit()
    connection.close()


def get_expenses():
    connection = sqlite3.connect("expenses.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT amount, category, date, description
        FROM expenses
        ORDER BY date DESC
    """)

    expenses = cursor.fetchall()

    connection.close()

    return expenses


def get_summary():
    connection = sqlite3.connect("expenses.db")
    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM expenses")
    total_expenses = cursor.fetchone()[0]

    cursor.execute("SELECT SUM(amount) FROM expenses")
    total_spent = cursor.fetchone()[0]

    if total_spent is None:
        total_spent = 0

    cursor.execute("SELECT MAX(amount) FROM expenses")
    largest_expense = cursor.fetchone()[0]

    if largest_expense is None:
        largest_expense = 0

    cursor.execute("SELECT COUNT(DISTINCT category) FROM expenses")
    total_categories = cursor.fetchone()[0]

    connection.close()

    return total_expenses, total_spent, largest_expense, total_categories
def get_category_totals():
    connection = sqlite3.connect("expenses.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT category, SUM(amount)
        FROM expenses
        GROUP BY category
        ORDER BY SUM(amount) DESC
    """)

    data = cursor.fetchall()

    connection.close()

    return data

def delete_expense(amount, category, date, description):
    connection = sqlite3.connect("expenses.db")
    cursor = connection.cursor()

    cursor.execute("""
        DELETE FROM expenses
        WHERE amount = ?
        AND category = ?
        AND date = ?
        AND description = ?
    """, (amount, category, date, description))

    connection.commit()
    connection.close()


def get_monthly_spending():
    connection = sqlite3.connect("expenses.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT 
            substr(date, 1, 7) AS month,
            SUM(amount)
        FROM expenses
        GROUP BY month
        ORDER BY month
    """)

    monthly_data = cursor.fetchall()

    connection.close()

    return monthly_data