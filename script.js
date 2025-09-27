const API_URL = "http://127.0.0.1:5000";

// Load budgets for dropdown and list
async function loadBudgets() {
    const res = await fetch(`${API_URL}/budgets`);
    const budgets = await res.json();

    const budgetSelect = document.getElementById("expense-budget");
    budgetSelect.innerHTML = '<option value="">Select Budget</option>';

    const budgetsList = document.getElementById("budgets-list");
    budgetsList.innerHTML = "";

    budgets.forEach(b => {
        // Dropdown
        const option = document.createElement("option");
        option.value = b.id;
        option.textContent = b.name;
        budgetSelect.appendChild(option);

        // List
        const div = document.createElement("div");
        div.className = "list-item";
        div.innerHTML = `<strong>${b.name}</strong> - Amount: ${b.amount} - Spent: ${b.spent} 
            <button onclick="loadExpenses(${b.id})">View Expenses</button>
            <button onclick="checkPrediction(${b.id})">Prediction</button>`;
        budgetsList.appendChild(div);
    });
}

// Add Budget
document.getElementById("budget-form").addEventListener("submit", async (e) => {
    e.preventDefault();
    const data = {
        name: document.getElementById("budget-name").value,
        amount: parseFloat(document.getElementById("budget-amount").value),
        start_date: document.getElementById("budget-start").value,
        end_date: document.getElementById("budget-end").value
    };
    await fetch(`${API_URL}/budgets`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(data)
    });
    e.target.reset();
    loadBudgets();
});

// Add Expense
document.getElementById("expense-form").addEventListener("submit", async (e) => {
    e.preventDefault();
    const data = {
        budget_id: parseInt(document.getElementById("expense-budget").value),
        description: document.getElementById("expense-description").value,
        amount: parseFloat(document.getElementById("expense-amount").value),
        date: document.getElementById("expense-date").value
    };
    await fetch(`${API_URL}/expenses`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(data)
    });
    e.target.reset();
    loadBudgets();
});

// Load expenses for a budget
async function loadExpenses(budgetId) {
    const res = await fetch(`${API_URL}/budgets/${budgetId}/expenses`);
    const expenses = await res.json();

    const expensesList = document.getElementById("expenses-list");
    expensesList.innerHTML = "";
    expenses.forEach(e => {
        const div = document.createElement("div");
        div.className = "list-item";
        div.textContent = `${e.description} - Amount: ${e.amount} - Date: ${e.date}`;
        expensesList.appendChild(div);
    });
}

// Check budget prediction
async function checkPrediction(budgetId) {
    const res = await fetch(`${API_URL}/budgets/${budgetId}/prediction`);
    const data = await res.json();
    alert(`${data.status.toUpperCase()}: ${data.message}`);
}

// Initial load
loadBudgets();
