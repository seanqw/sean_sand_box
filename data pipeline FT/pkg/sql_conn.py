import pyodbc
import pandas as pd
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

#query = 'select state, tax_rate from fuel_irp where dt_start = DATEADD(DAY, 1, EOMONTH(GETDATE(), -2)) group by state, tax_rate'

def query(month_start):
    #driver = 'ODBC Driver 17 for SQL Server'
    #server = 'analyticssql' 
    #database = 'psAnalytics' 
    #trusted_connection = 'yes'
    driver = os.getenv('db_driver')
    server = os.getenv('db_server')
    database =  os.getenv('db_database')
    trusted_connection = os.getenv('db_trusted_connection')

    sql_file_path = os.path.join(os.path.dirname(__file__), 'query.sql')
    #query = f"select state, tax_rate as 'Tax Rate' from fuel_irp where dt_start=? group by state, tax_rate"
    try:
        with open(sql_file_path, 'r') as f:
            query = f.read()
    except Exception as e:
        print(f'Read sql File Error: {e}')

    try:
        with pyodbc.connect(f'DRIVER={driver};SERVER={server};DATABASE={database};Trusted_Connection={trusted_connection}') as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, month_start)
                rows = cursor.fetchall()
                row_columns = [col[0] for col in cursor.description]

        return pd.DataFrame.from_records(rows,columns=row_columns)

    except pyodbc.Error as ex:
        sqlstate = ex.args[0]
        print(f"Database error: {sqlstate} - {ex}")
        return pd.DataFrame()  #empty
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return pd.DataFrame()


#Test:
if __name__=='__main__':
    month_start_date = datetime(2025, 6, 1).date()
    df = query(month_start_date)

    if not df.empty:
        print(df.head(5))
    else:
        print('No data retrieved or an error occurred.')
