from crewai_tools import NL2SQLTool

# ✅ Use MySQLTool instead
mysql_tool = NL2SQLTool(
    db_uri="mysql+pymysql://root:FBG_123@127.0.0.1:3306/world_layoffs"
)





