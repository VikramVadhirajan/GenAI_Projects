# 🧠 NL2SQL AI Query App (Streamlit + CrewAI)

An interactive AI-powered application that converts **natural language questions into SQL queries** and executes them on a MySQL database.

Built using **Streamlit, CrewAI, and NL2SQL Tool**, this app enables users to query databases without writing SQL manually.

---

## 🚀 Features

- 🔗 Connect to any MySQL database dynamically  
- 📂 Load available databases and tables  
- 📋 Select specific tables for querying  
- 🧠 Convert natural language → SQL using CrewAI  
- ⚡ Execute queries and display results instantly  
- ⏱️ Track execution time  
- 🔒 Ensures only `SELECT` queries are generated (safe querying)

---

## 🛠️ Tech Stack

- Python
- Streamlit
- CrewAI
- SQLAlchemy
- MySQL Connector
- NL2SQL Tool

---

## 📸 Application Flow

1. Enter MySQL credentials  
2. Load databases  
3. Select a database  
4. Load tables  
5. Select required tables  
6. Ask a question in plain English  
7. Get:
   - Generated SQL query  
   - Query results  
   - Explanation  

---

## ⚙️ Installation

```bash
pip install streamlit crewai crewai-tools sqlalchemy mysql-connector-python
```

---

## ▶️ Run the App

```bash
streamlit run app.py
```

---

## 🧠 Example Queries

- "Which company has raised the highest funding?"
- "Show top 5 customers by revenue"
- "What is the average sales per region?"

---

## 🔐 Safety Design

- Only `SELECT` queries are allowed  
- Prevents database modification  
- Schema-aware query generation  

---

## 📂 Project Structure

```
.
├── app.py
├── README.md
└── requirements.txt
```

---

## 💡 Key Highlights

- Uses **AI Agents (CrewAI)** for query generation  
- Dynamically builds **database schema context**  
- Enables **business users to query data without SQL knowledge**  

---

## 🌐 Future Improvements

- Add support for PostgreSQL & SQLite  
- Query history tracking  
- Visualization (charts, dashboards)  
- Authentication layer  

---

## 👨‍💻 Author

**Vikram Vadhirajan**  
- 🌐 Portfolio: https://vikramvadhirajan.github.io/Portfolio-Website/  
- 💼 LinkedIn: https://linkedin.com/in/yourprofile  
- 📧 Email: yourmail@gmail.com  

---

## ⭐ Show Your Support

If you like this project, give it a ⭐ on GitHub!
