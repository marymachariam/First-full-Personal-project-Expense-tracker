"use client";

import { useState, useEffect } from "react";
import {
  getDashboard,
  getCategorySummary,
  getMonthlySpending,
  getBudgetVsSpending,
  getAlerts,
} from "../lib/api";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  PieChart,
  Pie,
  Cell,
  Legend,
  ResponsiveContainer,
} from "recharts";

const COLORS = ["#6366f1", "#22d3ee", "#f59e0b", "#10b981", "#ef4444"];

export default function DashboardPage() {
  const [summary, setSummary] = useState(null);
  const [categories, setCategories] = useState([]);
  const [monthly, setMonthly] = useState([]);
  const [budgetVs, setBudgetVs] = useState([]);
  const [alerts, setAlerts] = useState([]);

  useEffect(() => {
    async function fetchAll() {
      const [s, c, m, b, a] = await Promise.all([
        getDashboard(),
        getCategorySummary(),
        getMonthlySpending(),
        getBudgetVsSpending(),
        getAlerts(),
      ]);
      setSummary(s);
      setCategories(c.category_summary);
      setMonthly(m.monthly_spending);
      setBudgetVs(b.budget_vs_actual);
      setAlerts(a.alerts);
    }
    fetchAll();
  }, []);

  if (!summary) return <p style={{ padding: "2rem" }}>Loading dashboard...</p>;

  return (
    <div style={{ padding: "2rem", fontFamily: "sans-serif", background: "#f1f5f9", minHeight: "100vh" }}>
      <h1 style={{ fontSize: "1.8rem", marginBottom: "1.5rem", color: "#1e293b" }}>
         Budget Tracker Dashboard
      </h1>

      {/* Summary Cards */}
      <div style={{ display: "grid", gridTemplateColumns: "repeat(4, 1fr)", gap: "1rem", marginBottom: "2rem" }}>
        <div style={{ background: "#6366f1", color: "white", borderRadius: "12px", padding: "1.5rem" }}>
          <p style={{ margin: 0, fontSize: "0.85rem", opacity: 0.8 }}>Total Income</p>
          <h2 style={{ margin: "0.5rem 0 0", fontSize: "1.6rem" }}>Ksh {summary.total_income}</h2>
        </div>
        <div style={{ background: "#ef4444", color: "white", borderRadius: "12px", padding: "1.5rem" }}>
          <p style={{ margin: 0, fontSize: "0.85rem", opacity: 0.8 }}>Total Expenses</p>
          <h2 style={{ margin: "0.5rem 0 0", fontSize: "1.6rem" }}>Ksh {summary.total_expenses}</h2>
        </div>
        <div style={{ background: "#10b981", color: "white", borderRadius: "12px", padding: "1.5rem" }}>
          <p style={{ margin: 0, fontSize: "0.85rem", opacity: 0.8 }}>Remaining Balance</p>
          <h2 style={{ margin: "0.5rem 0 0", fontSize: "1.6rem" }}>Ksh {summary.remaining_balance}</h2>
        </div>
        <div style={{ background: "#f59e0b", color: "white", borderRadius: "12px", padding: "1.5rem" }}>
          <p style={{ margin: 0, fontSize: "0.85rem", opacity: 0.8 }}>Transactions</p>
          <h2 style={{ margin: "0.5rem 0 0", fontSize: "1.6rem" }}>{summary.number_of_transactions}</h2>
        </div>
      </div>

      {/* Charts Row */}
      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "1.5rem", marginBottom: "2rem" }}>

        {/* Bar Chart - Monthly Spending */}
        <div style={{ background: "white", borderRadius: "12px", padding: "1.5rem" }}>
          <h3 style={{ marginTop: 0, color: "#1e293b" }}> Monthly Spending</h3>
          <ResponsiveContainer width="100%" height={250}>
            <BarChart data={monthly}>
              <XAxis dataKey="month" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="amount" fill="#6366f1" radius={[6, 6, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Pie Chart - Category Breakdown */}
        <div style={{ background: "white", borderRadius: "12px", padding: "1.5rem" }}>
          <h3 style={{ marginTop: 0, color: "#1e293b" }}>Spending by Category</h3>
          <ResponsiveContainer width="100%" height={250}>
            <PieChart>
              <Pie
                data={categories}
                dataKey="amount"
                nameKey="category"
                cx="50%"
                cy="50%"
                outerRadius={90}
                label
              >
                {categories.map((_, index) => (
                  <Cell key={index} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip />
              <Legend />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Budget vs Spending Table */}
      <div style={{ background: "white", borderRadius: "12px", padding: "1.5rem", marginBottom: "2rem" }}>
        <h3 style={{ marginTop: 0, color: "#1e293b" }}>Budget vs Actual Spending</h3>
        <table style={{ width: "100%", borderCollapse: "collapse" }}>
          <thead>
            <tr style={{ background: "#f8fafc" }}>
              <th style={{ padding: "0.75rem", textAlign: "left", color: "#64748b" }}>Category</th>
              <th style={{ padding: "0.75rem", textAlign: "left", color: "#64748b" }}>Budget</th>
              <th style={{ padding: "0.75rem", textAlign: "left", color: "#64748b" }}>Spent</th>
              <th style={{ padding: "0.75rem", textAlign: "left", color: "#64748b" }}>Difference</th>
            </tr>
          </thead>
          <tbody>
            {budgetVs.map((row, i) => (
              <tr key={i} style={{ borderTop: "1px solid #f1f5f9" }}>
                <td style={{ padding: "0.75rem" }}>{row.category}</td>
                <td style={{ padding: "0.75rem" }}>Ksh {row.budget}</td>
                <td style={{ padding: "0.75rem" }}>Ksh {row.spent}</td>
                <td style={{ padding: "0.75rem", color: row.difference < 0 ? "#ef4444" : "#10b981", fontWeight: "bold" }}>
                  Ksh {row.difference}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Alerts */}
      <div style={{ background: "white", borderRadius: "12px", padding: "1.5rem" }}>
        <h3 style={{ marginTop: 0, color: "#1e293b" }}> Spending Alerts</h3>
        {alerts.length === 0 && <p style={{ color: "#64748b" }}>No alerts at the moment</p>}
        {alerts.map((alert, i) => (
          <div key={i} style={{
            padding: "1rem",
            borderRadius: "8px",
            marginBottom: "0.75rem",
            background: alert.status === "OVERSPENT" ? "#fef2f2" : "#f0fdf4",
            borderLeft: `4px solid ${alert.status === "OVERSPENT" ? "#ef4444" : "#10b981"}`
          }}>
            <strong>{alert.category}</strong> —
            {alert.status === "OVERSPENT"
              ? ` Overspent by Ksh ${alert.over_by}`
              : ` Within budget ✓`}
          </div>
        ))}
      </div>
    </div>
  );
}