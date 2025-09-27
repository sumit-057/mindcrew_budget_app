from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import date, datetime, timedelta

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:sumit%400605@localhost:3306/flask_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
flask_db = SQLAlchemy(app)

# ----------------------------
# Database Models
# ----------------------------
class Budget(flask_db.Model):
    id = flask_db.Column(flask_db.Integer, primary_key=True)
    name = flask_db.Column(flask_db.String(50), nullable=False)
    amount = flask_db.Column(flask_db.Float, nullable=False)
    start_date = flask_db.Column(flask_db.Date, nullable=False)
    end_date = flask_db.Column(flask_db.Date, nullable=False)
    expenses = flask_db.relationship('Expense', backref='budget', lazy=True)

class Expense(flask_db.Model):
    id = flask_db.Column(flask_db.Integer, primary_key=True)
    budget_id = flask_db.Column(flask_db.Integer, flask_db.ForeignKey('budget.id'), nullable=False)
    description = flask_db.Column(flask_db.String(100))
    amount = flask_db.Column(flask_db.Float, nullable=False)
    date = flask_db.Column(flask_db.Date, nullable=False)

# ----------------------------
# Create flask_db
# ----------------------------
with app.app_context():
    flask_db.create_all()

# ----------------------------
# CORS Handling
# ----------------------------
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

# ----------------------------
# Routes
# ----------------------------

# Add a new budget
@app.route('/budgets', methods=['POST', 'OPTIONS'])
def add_budget():
    if request.method == 'OPTIONS':
        return '', 200
    data = request.get_json()
    try:
        budget = Budget(
            name=data['name'],
            amount=data['amount'],
            start_date=datetime.strptime(data['start_date'], "%Y-%m-%d").date(),
            end_date=datetime.strptime(data['end_date'], "%Y-%m-%d").date()
        )
        flask_db.session.add(budget)
        flask_db.session.commit()
        return jsonify({"message": "Budget added successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Get all budgets
@app.route('/budgets', methods=['GET'])
def get_budgets():
    budgets = Budget.query.all()
    result = []
    for b in budgets:
        total_spent = sum(e.amount for e in b.expenses)
        result.append({
            "id": b.id,
            "name": b.name,
            "amount": b.amount,
            "start_date": str(b.start_date),
            "end_date": str(b.end_date),
            "spent": total_spent
        })
    return jsonify(result)

# Add a new expense
@app.route('/expenses', methods=['POST', 'OPTIONS'])
def add_expense():
    if request.method == 'OPTIONS':
        return '', 200
    data = request.get_json()
    try:
        expense = Expense(
            budget_id=data['budget_id'],
            description=data.get('description', ''),
            amount=data['amount'],
            date=datetime.strptime(data['date'], "%Y-%m-%d").date()
        )
        flask_db.session.add(expense)
        flask_db.session.commit()
        return jsonify({"message": "Expense added successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Get all expenses for a budget
@app.route('/budgets/<int:budget_id>/expenses', methods=['GET'])
def get_expenses(budget_id):
    budget = Budget.query.get_or_404(budget_id)
    expenses = [
        {"id": e.id, "description": e.description, "amount": e.amount, "date": str(e.date)}
        for e in budget.expenses
    ]
    return jsonify(expenses)

# Prediction endpoint
@app.route('/budgets/<int:budget_id>/prediction', methods=['GET'])
def predict_budget(budget_id):
    budget = Budget.query.get_or_404(budget_id)
    total_days = (budget.end_date - budget.start_date).days + 1
    days_passed = (date.today() - budget.start_date).days + 1
    days_passed = max(days_passed, 1)  # prevent division by zero
    current_spend = sum(e.amount for e in budget.expenses)
    avg_daily_spend = current_spend / days_passed
    projected_total = avg_daily_spend * total_days

    if projected_total <= budget.amount:
        return jsonify({"status": "on_track", "message": "You are on track to stay within your budget."})
    else:
        days_until_overspend = budget.amount / avg_daily_spend
        overspend_date = budget.start_date + timedelta(days=days_until_overspend)
        return jsonify({
            "status": "overspending",
            "message": f"At this rate, you will overspend your budget by {overspend_date}"
        })

# ----------------------------
# Run the app
# ----------------------------
if __name__ == '__main__':
    app.run(debug=True)
