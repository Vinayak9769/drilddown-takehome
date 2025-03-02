import re
import pandas as pd
from sqlalchemy import create_engine
from langchain_core.runnables import RunnableLambda

DATABASE_URL = "sqlite:///database.db"
engine = create_engine(DATABASE_URL)

def execute_sql(output: dict) -> dict:
    print(output)
    raw_sql = output.get("sql", "")
    pattern = r"```sql\s*(.*?)\s*```"
    match = re.search(pattern, raw_sql, re.DOTALL)
    if match:
        sql_code = match.group(1).strip()
    else:
        sql_code = raw_sql.strip()
    with engine.connect() as conn:
        df = pd.read_sql_query(sql=sql_code, con=conn)
    return {"title": output.get("title", "Sales Report"), "df": df}

sql_executor_chain = RunnableLambda(func=execute_sql)
