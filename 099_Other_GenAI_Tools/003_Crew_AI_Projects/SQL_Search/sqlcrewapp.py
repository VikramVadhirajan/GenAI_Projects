import streamlit as st
from crewai_tools import NL2SQLTool
from crewai import Agent, Task, Crew, Process
import time
from sqlalchemy import create_engine, text


## Helper function to get DB information and tables
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
            columns = conn.execute(
                text(f"DESCRIBE {table}")
            ).fetchall()

            schema_text += f"\nTable: {table}\nColumns:\n"

            for col in columns:
                schema_text += f"- {col[0]} ({col[1]})\n"

    return schema_text


# -----------------------------
# Sidebar Inputs
# -----------------------------
st.sidebar.title("⚙️ Configure your Database Connection...")


mysql_user = st.sidebar.text_input("User", value="root")
mysql_password = st.sidebar.text_input("Password", type="password")
mysql_host = st.sidebar.text_input("Host", value="localhost")


# Load databases
if "databases" not in st.session_state:
    st.session_state.databases = []

if st.sidebar.button("📂 Load Databases"):
    dbs, error = get_databases(mysql_user, mysql_password, mysql_host)

    if error:
        st.sidebar.error(error)
    else:
        st.session_state.databases = dbs
        st.sidebar.success("Databases loaded!")

# Select database
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

question = st.text_input(
    "Enter your question",
    placeholder="e.g. Which company has raised highest funds in Germany?"
)

run_button = st.button("🚀 Run Query")

# -----------------------------
# Main UI
# -----------------------------
st.title("🧠 SQL Search Query CrewAI ")
st.write("Ask business questions directly from your database using AI.")


# -----------------------------
# Run Logic
# -----------------------------

if not selected_db:
    st.warning("Select a database first")
    st.stop()

if not selected_tables:
    st.warning("Select at least one table")
    st.stop()

if run_button:
    
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        try:
            with st.spinner("Running CrewAI..."):

                # Tool
                mysql_tool = NL2SQLTool(db_uri=db_uri)

                # Schema (static for now)
                schema = get_selected_schema(db_uri,selected_tables)

                # Agent
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

                # Task
                task = Task(
                    description=f"""
                    Answer the user question using SQL.

                    Steps:
                    1. Generate SQL query
                    2. Execute using MySQL tool
                    3. Return:
                       - SQL query
                       - Result
                       - Explanation

                    User question: {question}
                    """,
                    expected_output="Only the final answer",
                    agent=sql_agent
                )

                # Crew
                crew = Crew(
                    agents=[sql_agent],
                    tasks=[task],
                    process=Process.sequential,
                    verbose=False
                )

                # Run
                start_time = time.time()
                result = crew.kickoff()
                end_time = time.time()
                execution_time = end_time - start_time


            # -----------------------------
            # Output
            # -----------------------------
            # st.success("✅ Query Executed Successfully")

            st.subheader("📊 Result")
            st.success(result.raw)
            st.info(f"⏱️ Execution Time: {execution_time:.2f} seconds")

        except Exception as e:
            st.error(f"❌ Error: {str(e)}")