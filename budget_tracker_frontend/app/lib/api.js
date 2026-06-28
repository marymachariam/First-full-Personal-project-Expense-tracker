const BASE_URL = "http://127.0.0.1:8000";

// Auth
// for registering a user
export async function registerUser(data) {
  const res = await fetch(`${BASE_URL}/register`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  return res.json();
}

// for a user to login
export async function loginUser(data) {
  const res = await fetch(`${BASE_URL}/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  return res.json();
}

// Transactions
export async function getTransactions() {
  const res = await fetch(`${BASE_URL}/transactions`);
  return res.json();
}

export async function createTransaction(data) {
  const res = await fetch(`${BASE_URL}/transactions`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  return res.json();
}

export async function deleteTransaction(id) {
  const res = await fetch(`${BASE_URL}/transactions/${id}`, {
    method: "DELETE",
  });
  return res.json();
}

// Categories
export async function getCategories() {
  const res = await fetch(`${BASE_URL}/categories`);
  return res.json();
}

export async function createCategory(data) {
  const res = await fetch(`${BASE_URL}/categories`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  return res.json();
}

// Budgets
export async function getBudgets() {
  const res = await fetch(`${BASE_URL}/budgets`);
  return res.json();
}

export async function createBudget(data) {
  const res = await fetch(`${BASE_URL}/budgets`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  return res.json();
}

// Dashboard
export async function getDashboard() {
  const res = await fetch(`${BASE_URL}/dashboard`);
  return res.json();
}

export async function getCategorySummary() {
  const res = await fetch(`${BASE_URL}/dashboard/category-summary`);
  return res.json();
}

export async function getMonthlySpending() {
  const res = await fetch(`${BASE_URL}/dashboard/monthly-spending`);
  return res.json();
}

export async function getBudgetVsSpending() {
  const res = await fetch(`${BASE_URL}/dashboard/budget-vs-spending`);
  return res.json();
}

export async function getAlerts() {
  const res = await fetch(`${BASE_URL}/dashboard/alerts`);
  return res.json();
}