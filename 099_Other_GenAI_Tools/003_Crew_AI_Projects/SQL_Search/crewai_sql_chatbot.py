
import streamlit as st
from crewai_tools import NL2SQLTool
from crewai import Agent, Task, Crew, Process
import time
from sqlalchemy import create_engine, text

# -----------------------------
# Session Memory (Chat History)
# -----------------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


def get_context():
    history = st.session_state.chat_history
    return "\n".join([f"{m['role']}: {m['content']}" for m in history[-10:]])


def add_to_memory(user, bot):
    st.session_state.chat_history.append({"role": "user", "content": user})
    st.session_state.chat_history.append({"role": "assistant", "content": bot})


# -----------------------------
# DB Helpers
# -----------------------------
def get_databases(mysql_user, mysql_password, mysql_host):
    try:
        uri = f"mysql+mysqlconnector://{mysql_user}:{mysql_password}@{mysql_host}"
        engine = create_engine(uri)

        with engine.connect() as conn:
            result = conn.execute(text("SHOW DATABASES")).fetchall()

        return [row[0] for row in result], None

    except Exception as e:
        return [], str(e)


def get_tables(db_uri):
    engine = create_engine(db_uri)
    with engine.connect() as conn:
        tables = conn.execute(text("SHOW TABLES")).fetchall()
    return [list(t)[0] for t in tables]


def get_selected_schema(db_uri, selected_tables):
    engine = create_engine(db_uri)
    schema_text = ""

    with engine.connect() as conn:
        for table in selected_tables:
            columns = conn.execute(text(f"DESCRIBE {table}")).fetchall()

            schema_text += f"\nTable: {table}\nColumns:\n"

            for col in columns:
                schema_text += f"- {col[0]} ({col[1]})\n"

    return schema_text


# -----------------------------
# Sidebar Config
# -----------------------------
st.sidebar.title("⚙️ Database Configuration")

mysql_user = st.sidebar.text_input("User", value="root")
mysql_password = st.sidebar.text_input("Password", type="password")
mysql_host = st.sidebar.text_input("Host", value="localhost")

if "databases" not in st.session_state:
    st.session_state.databases = []

if st.sidebar.button("📂 Load Databases"):
    dbs, error = get_databases(mysql_user, mysql_password, mysql_host)

    if error:
        st.sidebar.error(error)
    else:
        st.session_state.databases = dbs
        st.sidebar.success("Databases loaded!")

selected_db = st.sidebar.selectbox(
    "🗄️ Select Database",
    options=st.session_state.databases
)

if selected_db:
    db_uri = f"mysql+mysqlconnector://{mysql_user}:{mysql_password}@{mysql_host}/{selected_db}"

if "tables" not in st.session_state:
    st.session_state.tables = []

if st.sidebar.button("📊 Load Tables"):
    try:
        st.session_state.tables = get_tables(db_uri)
        st.sidebar.success("Tables loaded!")
    except Exception as e:
        st.sidebar.error(e)

selected_tables = st.sidebar.multiselect(
    "📋 Select Tables",
    options=st.session_state.tables
)


# -----------------------------
# Main UI
# -----------------------------
st.title("🤖 SQL Chatbot with Memory")
st.write("Ask questions about your database like a conversation.")

# Display chat history
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Chat input
question = st.chat_input("Ask your database question...")

# -----------------------------
# Chat Logic
# -----------------------------
if question:
    if not selected_db:
        st.warning("Select a database first")
        st.stop()

    if not selected_tables:
        st.warning("Select at least one table")
        st.stop()

    # Show user message
    st.session_state.chat_history.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.write(question)

    # Assistant response
    with st.chat_message("assistant"):
        with st.spinner("Running CrewAI..."):
            try:
                start_time = time.time()

                mysql_tool = NL2SQLTool(db_uri=db_uri)
                schema = get_selected_schema(db_uri, selected_tables)
                context = get_context()

                sql_agent = Agent(
                    role="SQL Analyst",
                    goal="Answer business questions using MySQL database",
                    backstory=f"""
                    You are an expert SQL analyst.

                    Database schema:
                    {schema}

                    Only generate SELECT queries.
                    Do NOT modify database.
                    """,
                    tools=[mysql_tool],
                    verbose=False
                )

                task = Task(
                    description=f"""
                    Previous conversation:
                    {context}

                    Current question:
                    {question}

                    Steps:
                    1. Generate SQL query
                    2. Execute query
                    3. Return result + explanation

                    Only SELECT queries.
                    """,
                    expected_output="Final answer",
                    agent=sql_agent
                )

                crew = Crew(
                    agents=[sql_agent],
                    tasks=[task],
                    process=Process.sequential,
                    verbose=False
                )

                result = crew.kickoff()
                response_text = result.raw if hasattr(result, "raw") else str(result)

                st.write(response_text)
                add_to_memory(question, response_text)

                end_time = time.time()
                st.info(f"⏱️ Execution Time: {end_time - start_time:.2f} seconds")

            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
