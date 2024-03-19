from datetime import datetime
import os 
import pandas as pd
from google.cloud import bigquery

def SQL_query(account_bigquery_secret, sql_path_folder, sql_path_file, last_execution_date = ""):
    """Execute a BigQuery SQL query and return the result as a DataFrame.
    :sql_path_file: The name of the SQL file to be executed.
    Returns:
        :df: A DataFrame containing the result of the SQL query.
    """
    sql_path = f"{sql_path_folder}/{sql_path_file}"
    with open(sql_path, "r") as file:
        sql = file.read()
    if last_execution_date != "":
        sql = sql.replace("WHERE date(updated_at) > DATE_SUB(CURRENT_DATE, INTERVAL 1 DAY)", f"WHERE date(updated_at) > DATE_SUB(\"{last_execution_date}\", INTERVAL 1 DAY)")
    
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = account_bigquery_secret
    client = bigquery.Client()
    df = client.query(sql).to_dataframe()
    return df
