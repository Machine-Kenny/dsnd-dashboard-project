from sqlite3 import connect
from pathlib import Path
from functools import wraps
import pandas as pd

db_path = Path(__file__).parent / "employee_events.db"
class QueryMixin:
    def pandas_query(self, sql_query):
        with connect(db_path) as connection:
            return pd.read_sql_query(sql_query, connection)

    def query(self, sql_query):
        with connect(db_path) as connection:
            cursor = connection.cursor()
            result = cursor.execute(sql_query).fetchall()
        return result
    
 
def query(func):
    """
    Decorator that runs a standard sql execution
    and returns a list of tuples
    """

    @wraps(func)
    def run_query(*args, **kwargs):
        query_string = func(*args, **kwargs)
        connection = connect(db_path)
        cursor = connection.cursor()
        result = cursor.execute(query_string).fetchall()
        connection.close()
        return result
    
    return run_query
