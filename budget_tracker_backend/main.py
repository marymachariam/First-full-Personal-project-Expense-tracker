from fastapi import FastAPI
from pydantic import BaseModel
from database import connect, get_cursor
import datetime
from fastapi.middleware.cors import CORSMiddleware # for allowing backed to communicate with frontend

app = FastAPI()

#Add the CORS middleware to your FastAPI app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],  
)

# def get_db_cursor():
#     connect = sqlite3.connect('budget_tracker.db')
#     return connect, connect.cursor()

@app.get('/')
def home():
    return {'Message' : 'Welcome to Macharias Smart Budget Tracker API!'}

#the first register endpoint
class RegisterUser(BaseModel):
    username: str
    email: str
    password: str

@app.post("/register")
def register(user: RegisterUser):
    cursor = get_cursor() 
    cursor.execute(
        """
        INSERT INTO users (username, email, password)
        VALUES (?, ?, ?)
        """,
        (user.username, user.email, user.password)
    )
    connect.commit()
    return {"message": "User created successfully!"}



#the login end point
class LoginUser(BaseModel):
    email: str
    password: str

@app.post("/login")
def login(user: LoginUser):
    cursor = get_cursor() 
    cursor.execute(
        """
        SELECT * FROM users WHERE email = ?
        """,
        (user.email,)
    )

    db_user = cursor.fetchone()

    if not db_user:
        return {"error": "Invalid email or password"}

    stored_password = db_user[3]

    if user.password != stored_password:
        return {"error": "Invalid email or password"}

    return {
        "message": "Login successful" }


#crud for transactions
class Transaction(BaseModel):
    user_id: int
    amount: float
    category_id: int
    type: str   
    description: str
    date: str

#post a transaction
@app.post("/transactions")
def create_transaction(transaction: Transaction):
    cursor = get_cursor() 
    cursor.execute(
        """
        INSERT INTO transactions
        (user_id, category_id, amount, type, description, date)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            transaction.user_id,
            transaction.category_id,
            transaction.amount,
            transaction.type,
            transaction.description,
            transaction.date
        )
    )

    connect.commit()

    return {
        "message": "Transaction added successfully"
    }



#get all transactions
@app.get("/transactions")
def get_transactions():
    cursor = get_cursor() 
    cursor.execute("SELECT * FROM transactions")

    transactions = cursor.fetchall()

    return {
        "transactions": transactions
    }


#get one transaction
@app.get("/transactions/{transaction_id}")
def get_transaction(transaction_id: int):
    cursor = get_cursor() 
    cursor.execute(
        "SELECT * FROM transactions WHERE transaction_id = ?",
        (transaction_id,)
    )

    transaction = cursor.fetchone()

    if transaction is None:
        return {"message": "Transaction not found"}

    return {
        "transaction": transaction
    }


#update a transaction
@app.put("/transactions/{transaction_id}")
def update_transaction(transaction_id: int, transaction: Transaction):
    cursor = get_cursor() 
    cursor.execute(
        """
        UPDATE transactions
        SET user_id = ?,
            category_id = ?,
            amount = ?,
            type = ?,
            description = ?,
            date = ?
        WHERE transaction_id = ?
        """,
        (
            transaction.user_id,
            transaction.category_id,
            transaction.amount,
            transaction.type,
            transaction.description,
            transaction.date,
            transaction_id
        )
    )
    if cursor.rowcount == 0:
        return {"message": "Transaction not found"}
    connect.commit()
    return {"message": "Transaction updated successfully"}


#delete a transaction
@app.delete("/transactions/{transaction_id}")
def delete_transaction(transaction_id: int):
    cursor = get_cursor() 
    cursor.execute(
        "DELETE FROM transactions WHERE transaction_id = ?",
        (transaction_id,)
    )
    if cursor.rowcount == 0:
        return {"message": "Transaction not found"}
    connect.commit()

    return {
        "message": "Transaction deleted successfully"
    }


#CRUD for categories
class Category(BaseModel):
    user_id: int
    category_name: str

#creating a category
@app.post("/categories")
def create_category(category: Category):
    cursor = get_cursor() 
    cursor.execute(
        """
        INSERT INTO categories (user_id, category_name)
        VALUES (?, ?)
        """,
        (category.user_id, category.category_name)
    )

    connect.commit()

    return {
        "message": "Category created successfully"
    }

#getting all categories
@app.get("/categories")
def get_categories():
    cursor = get_cursor() 
    cursor.execute(
        "SELECT * FROM categories"
    )

    categories = cursor.fetchall()

    return {
        "categories": categories
    }

#getting one category
@app.get("/categories/{category_id}")
def get_category(category_id: int):
    cursor = get_cursor() 
    cursor.execute(
        """
        SELECT * FROM categories
        WHERE category_id = ?
        """,
        (category_id,)
    )

    category = cursor.fetchone()

    if category is None:
        return {
            "message": "Category not found"
        }

    return {
        "category": category
    }

#updating a category
@app.put("/categories/{category_id}")
def update_category(category_id: int, category: Category):
    cursor = get_cursor() 
    cursor.execute(
        """
        UPDATE categories
        SET user_id = ?, category_name = ?
        WHERE category_id = ?
        """,
        (
            category.user_id,
            category.category_name,
            category_id
        )
    )

    connect.commit()

    return {
        "message": "Category updated successfully"
    }

#deleting a category
@app.delete("/categories/{category_id}")
def delete_category(category_id: int):
    cursor = get_cursor() 
    cursor.execute(
        """
        DELETE FROM categories
        WHERE category_id = ?
        """,
        (category_id,)
    )

    connect.commit()

    return {
        "message": "Category deleted successfully"
    }

#the budget crud
class Budget(BaseModel):
    user_id: int
    category_id: int
    amount: float
    month: int
    year: int

#creating a budget
@app.post("/budgets")
def create_budget(budget: Budget):
    cursor = get_cursor() 
    cursor.execute(
        """
        INSERT INTO budgets
        (user_id, category_id, amount, month, year)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            budget.user_id,
            budget.category_id,
            budget.amount,
            budget.month,
            budget.year
        )
    )

    connect.commit()

    return {
        "message": "Budget created successfully"
    }

#getting alll budgets
@app.get("/budgets")
def get_budgets():
    cursor = get_cursor() 
    cursor.execute(
        "SELECT * FROM budgets"
    )

    budgets = cursor.fetchall()

    return {
        "budgets": budgets
    }

#getting one budget
@app.get("/budgets/{budget_id}")
def get_budget(budget_id: int):
    cursor = get_cursor() 
    cursor.execute(
        """
        SELECT * FROM budgets
        WHERE budget_id = ?
        """,
        (budget_id,)
    )

    budget = cursor.fetchone()

    if budget is None:
        return {
            "message": "Budget not found"
        }

    return {
        "budget": budget
    }

#updating the budget
@app.put("/budgets/{budget_id}")
def update_budget(budget_id: int, budget: Budget):
    cursor = get_cursor() 
    cursor.execute(
        """
        UPDATE budgets
        SET user_id = ?,
            category_id = ?,
            amount = ?,
            month = ?,
            year = ?
        WHERE budget_id = ?
        """,
        (
            budget.user_id,
            budget.category_id,
            budget.amount,
            budget.month,
            budget.year,
            budget_id
        )
    )

    if cursor.rowcount == 0:
        return {
            "message": "Budget not found"
        }

    connect.commit()

    return {
        "message": "Budget updated successfully"
    }

# deleting a budget
@app.delete("/budgets/{budget_id}")
def delete_budget(budget_id: int):
    cursor = get_cursor() 
    cursor.execute(
        """
        DELETE FROM budgets
        WHERE budget_id = ?
        """,
        (budget_id,)
    )

    if cursor.rowcount == 0:
        return {
            "message": "Budget not found"
        }

    connect.commit()

    return {
        "message": "Budget deleted successfully"
    }


#milestone 2 - createing the dashboard logic
@app.get("/dashboard")
def dashboard():
    cursor = get_cursor() 
    cursor.execute("""
        SELECT SUM(amount)
        FROM transactions
        WHERE type = 'income'
    """)
    income = cursor.fetchone()[0]

    cursor.execute("""
        SELECT SUM(amount)
        FROM transactions
        WHERE type = 'expense'
    """)
    expense = cursor.fetchone()[0]

    income = income or 0
    expense = expense or 0

    balance = income - expense
    cursor.execute("""
        SELECT COUNT(*)
        FROM transactions
    """)
    #count all transactions
    transaction_count = cursor.fetchone()[0]


    #highest amounted category
    cursor.execute("""
    SELECT
        c.category_name,
        SUM(t.amount) AS total_spent
    FROM transactions t
    JOIN categories c
    ON t.category_id = c.category_id
    WHERE t.type = 'expense'
    GROUP BY c.category_name
    ORDER BY total_spent DESC
    LIMIT 1
    """)

    highest = cursor.fetchone()
    if highest:
        highest_category = highest[0]
    else:
        highest_category = "None"

    return {
        "total_income": income,
        "total_expenses": expense,
        "remaining_balance": balance,
        "number_of_transactions": transaction_count,
        "highest_expense_category": highest_category

    }

#creating charts and readings
@app.get("/dashboard/category-summary")
def category_summary():
    cursor = get_cursor() 
    cursor.execute("""
        SELECT
            c.category_name,
            SUM(t.amount) AS total_spent
        FROM transactions t
        JOIN categories c
        ON t.category_id = c.category_id
        WHERE t.type = 'expense'
        GROUP BY c.category_name
        ORDER BY total_spent DESC
    """)

    rows = cursor.fetchall()
    summary = []

    for row in rows:
        summary.append({
            "category": row[0],
            "amount": row[1]
        })

    return {
        "category_summary": summary
    }

#monthyl spending end point
@app.get("/dashboard/monthly-spending")
def monthly_spending():
    cursor = get_cursor() 
    cursor.execute("""
        SELECT
            strftime('%Y-%m', date) AS month,
            SUM(amount) AS total_spent
        FROM transactions
        WHERE type = 'expense'
        GROUP BY month
        ORDER BY month
    """)

    rows = cursor.fetchall()
    result = []

    for row in rows:
        result.append({
            "month": row[0],
            "amount": row[1]
        })

    return {
        "monthly_spending": result
    }

#top expenses end points
@app.get("/dashboard/top-expenses")
def top_expenses():
    cursor = get_cursor() 
    cursor.execute("""
        SELECT
            description,
            amount,
            date
        FROM transactions
        WHERE type = 'expense'
        ORDER BY amount DESC
        LIMIT 5
    """)

    rows = cursor.fetchall()

    result = [
        {
            "description": row[0],
            "amount": row[1],
            "date": row[2]
        }
        for row in rows
    ]

    return {
        "top_expenses": result
    }

#Recent 5 transactions
@app.get("/dashboard/recent-transactions")
def recent_transactions():
    cursor = get_cursor() 
    cursor.execute("""
        SELECT
            description,
            amount,
            type,
            date
        FROM transactions
        ORDER BY date DESC
        LIMIT 5
    """)

    rows = cursor.fetchall()

    result = [
        {
            "description": row[0],
            "amount": row[1],
            "type": row[2],
            "date": row[3]
        }
        for row in rows
    ]

    return {
        "recent_transactions": result
    }


#the actual budget vs spending
@app.get("/dashboard/budget-vs-spending")
def budget_vs_spending():
    cursor = get_cursor() 
    cursor.execute("""
        SELECT
            c.category_name,
            b.amount AS budget,
            COALESCE(SUM(t.amount), 0) AS spent
        FROM budgets b
        JOIN categories c ON b.category_id = c.category_id
        LEFT JOIN transactions t
            ON t.category_id = b.category_id
            AND t.type = 'expense'
        GROUP BY b.category_id
    """)

    rows = cursor.fetchall()

    result = []

    for row in rows:
        budget = row[1]
        spent = row[2]

        result.append({
            "category": row[0],
            "budget": budget,
            "spent": spent,
            "difference": budget - spent
        })

    return {
        "budget_vs_actual": result
    }


#highest spending month
@app.get("/dashboard/highest-spending-month")
def highest_spending_month():
    cursor = get_cursor() 
    cursor.execute("""
        SELECT
            strftime('%Y-%m', date) AS month,
            SUM(amount) AS total_spent
        FROM transactions
        WHERE type = 'expense'
        GROUP BY month
        ORDER BY total_spent DESC
        LIMIT 1
    """)

    row = cursor.fetchone()

    if not row:
        return {"highest_spending_month": None}

    return {
        "highest_spending_month": {
            "month": row[0],
            "amount": row[1]
        }
    }

#end of month spending prediction
@app.get("/dashboard/prediction")
def end_of_month_prediction():
    cursor = get_cursor() 
    # 1. Get current month spending
    cursor.execute("""
        SELECT SUM(amount)
        FROM transactions
        WHERE type = 'expense'
        AND strftime('%Y-%m', date) = strftime('%Y-%m', 'now')
    """)

    result = cursor.fetchone()[0]
    spent_so_far = result or 0

    # 2. Get current day + days in month
    today = datetime.date.today()
    day_of_month = today.day

    next_month = today.replace(day=28) + datetime.timedelta(days=4)
    days_in_month = (next_month - datetime.timedelta(days=next_month.day)).day

    # 3. Predict
    if day_of_month == 0:
        prediction = 0
    else:
        daily_avg = spent_so_far / day_of_month
        prediction = daily_avg * days_in_month

    return {
        "spent_so_far": spent_so_far,
        "predicted_month_end_spending": round(prediction, 2)
    }

#alets system
@app.get("/dashboard/alerts")
def spending_alerts():
    cursor = get_cursor() 
    cursor.execute("""
        SELECT
            c.category_name,
            b.amount AS budget,
            COALESCE(SUM(t.amount), 0) AS spent
        FROM budgets b
        JOIN categories c ON b.category_id = c.category_id
        LEFT JOIN transactions t
            ON t.category_id = b.category_id
            AND t.type = 'expense'
        GROUP BY b.category_id
    """)

    rows = cursor.fetchall()

    alerts = []

    for row in rows:
        category = row[0]
        budget = row[1]
        spent = row[2]

        over_by = spent - budget

        if spent > budget:
            status = "OVERSPENT"
        else:
            status = "OK"
            over_by = 0

        alerts.append({
            "category": category,
            "budget": budget,
            "spent": spent,
            "status": status,
            "over_by": over_by
        })

    return {
        "alerts": alerts
    }