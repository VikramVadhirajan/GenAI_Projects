import sqlite3
import pandas as pd

## connect to sqllite
connection=sqlite3.connect("MandatoryFills.db")



## create the table
df=pd.read_excel(r"C:\14_Langchain\000_Learning_Center\004_SQL_Chatbot\Mandatory_fill.xlsx")

print(df.head())

df.to_sql('Mandatory', connection, if_exists='replace', index=False)


## Commit your changes in the database

connection.close()
