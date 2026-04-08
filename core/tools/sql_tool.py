# core/tools/sql_tool.py
import sqlite3
from pydantic import BaseModel, Field
from langchain_core.tools import tool

# --- 初始化内存数据库 ---
conn = sqlite3.connect(':memory:', check_same_thread=False)
cursor = conn.cursor()
cursor.execute("CREATE TABLE employees (id INTEGER, name TEXT, department TEXT, salary REAL)")
cursor.execute("INSERT INTO employees VALUES (1, 'Alice', 'Engineering', 25000)")
cursor.execute("INSERT INTO employees VALUES (2, 'Bob', 'Marketing', 18000)")
cursor.execute("INSERT INTO employees VALUES (3, 'Charlie', 'Engineering', 22000)")
conn.commit()


class SQLQueryInput(BaseModel):
    query: str = Field(..., description="要执行的 SQL SELECT 语句。表名: employees, 字段: id, name, department, salary")


@tool(args_schema=SQLQueryInput)
def execute_sql_query(query: str) -> str:
    """当用户询问关于员工、薪资或部门统计等结构化数据时，使用此工具执行 SQL 查询。"""
    print(f"\n[🛠️ 工具] 正在执行数据库查询: {query}")

    # 基础安全检查
    forbidden = ['DROP', 'DELETE', 'UPDATE', 'INSERT', 'ALTER']
    if any(k in query.upper() for k in forbidden):
        return "错误：由于安全原因，仅允许 SELECT 查询操作。"

    try:
        cursor.execute(query)
        rows = cursor.fetchall()
        if not rows:
            return "查询成功，但未找到匹配记录。"
        return "查询结果:\n" + "\n".join([f"- {row}" for row in rows])
    except Exception as e:
        return f"SQL 执行错误: {str(e)}。请检查语法后重试。"