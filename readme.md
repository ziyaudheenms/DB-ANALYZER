# 🚀 DB ANALYZER: Interact with Databases in Human Language

---

## 🌟 Project Overview

**DB ANALYZER** is a next-generation tool that empowers anyone—regardless of technical background—to interact with databases using plain English. Harnessing the power of Large Language Models, DB ANALYZER eliminates the need for SQL expertise, making data access simple, fast, and intuitive.

---

## ❓ The Problem

Many professionals—store managers, business officers, analysts—need to extract insights from databases like PostgreSQL. However, complex SQL queries can be a major roadblock for non-technical users, slowing down decision-making and limiting access to valuable data.

---

## ✅ Our Solution

**DB ANALYZER** bridges this gap with an easy-to-use interface:

1. **Ask in English:** Type your question in natural language.
2. **Automatic SQL Generation:** The system translates your question into a valid SQL command.
3. **Execution & Refinement:** It runs the command, then refines the results into a clear, human-readable answer.

> **Empowering everyone to access data—no SQL required!**

---

## 🛠️ Technology Stack

- **Frontend UI:** [Streamlit](https://streamlit.io/) (Python)
- **Core Logic:** Python + [LangChain](https://www.langchain.com/)
- **Large Language Model:** Google Gemini 2.5 Flash

---

## ⚙️ How It Works

### 🔹 SQL Database Executor

- **Connect:** Enter your PostgreSQL connection string.
- **Analyze:** The agent inspects your database structure (tables, columns).
- **Query:** Ask your question in English.
- **Generate & Execute:** The agent creates and runs the SQL command.
- **Refine:** Results are transformed into a user-friendly response.

---

### 🔹 CSV File Executor

- **Upload:** Add your CSV file.
- **Convert:** The agent loads data into a temporary SQLite database (as recommended by LangChain).
- **Query & Visualize:** Ask questions and get instant answers, including automatic charts (e.g., bar charts) for data visualization.
- **Insight Generation:** Receive detailed analysis and insights from your CSV data.

---

## 🎯 Key Benefits

- **No SQL Knowledge Needed:** Anyone can use it.
- **Fast & Accurate:** Get answers in seconds.
- **Visual Insights:** Automatic chart generation for CSV data.
- **Versatile:** Works with both SQL databases and CSV files.

---

> **Unlock the power of your data—no coding required!**

---