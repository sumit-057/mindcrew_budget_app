# mindcrew_budget_app
Pro-Spend is a simple full-stack budgeting web application that helps users manage their budgets and expenses, track spending, and predict potential overspending based on daily expenditure trends. It’s built with Flask for the backend and uses HTML, CSS, and JavaScript for the frontend. Data is stored in a MySQL database using SQLAlchemy ORM.
Pro-Spend Budget App

Pro-Spend is a simple budgeting web application that helps users manage budgets and expenses, track spending, and predict potential overspending based on daily expenditure trends. It uses Flask for the backend, MySQL for the database, and HTML/CSS/JavaScript for the frontend.

🛠 Features

Add and manage budgets with start and end dates.

Track expenses under specific budgets.

View budget details including total spent.

See all expenses for each budget.

Get predictions if a budget is on track or likely to overspend.

💻 Technologies Used

Backend: Python, Flask, Flask-SQLAlchemy

Database: MySQL

Frontend: HTML, CSS, JavaScript

Tools: Postman (for API testing)

📂 Project Structure
``` bash
Pro-Spend-Budget-App/
│
├─ backend/
│   └─ app.py               # Flask backend
│
├─ frontend/
│   ├─ index.html           # Frontend HTML
│   ├─ style.css            # CSS for styling
│   └─ script.js            # JavaScript for frontend logic
│
└─ README.md
```

🚀 Installation & Setup
1. Clone the repository:
``` bash
git clone https://github.com/<your-username>/<your-repo-name>.git
cd <your-repo-name>
```

3. Backend setup
``` bash

Create a virtual environment:

python -m venv venv
```


Activate the virtual environment:

Windows:
``` bash

venv\Scripts\activate


Mac/Linux:

source venv/bin/activate


Install dependencies:

pip install Flask Flask-SQLAlchemy PyMySQL
```


Setup MySQL database:

CREATE DATABASE flask_db;


Update app.py with your MySQL credentials if needed.

Run the backend:
``` bash

python backend/app.py
```

3. Frontend setup

Open the frontend folder.

You can open index.html directly in a browser or serve via a local server:
``` bash
cd frontend
python -m http.server 8000
```

Open browser at: http://localhost:8000

🌐 API Endpoints
Endpoint	Method	Description
``` bash
/budgets	GET	Get all budgets
/budgets	POST	Add a new budget
/expenses	POST	Add a new expense
/budgets/<budget_id>/expenses	GET	Get all expenses for a budget
/budgets/<budget_id>/prediction	GET	Check if budget is on track or overspending
```
📝 Usage

Open the frontend in your browser.

Add a Budget: Fill the form and click Add Budget.

Add an Expense: Select a budget, fill expense details, click Add Expense.

View Expenses: Click View Expenses under a budget to see all expenses.

Check Prediction: Click Prediction under a budget to see spending forecast.

⚡ Future Improvements

User authentication for multiple users.

Graphical dashboard with charts for budgets and expenses.

Export budgets and expenses to CSV or PDF.

Notifications for overspending alerts.
