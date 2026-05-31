import sqlite3
import pandas as pd

from google.cloud import bigquery


def upload_tickets_to_bigquery():

    # -----------------------------
    # Read SQLite
    # -----------------------------

    conn1 = sqlite3.connect(
        "company2.db"
    )

    df1 = pd.read_sql_query(
        """
        SELECT *
        FROM ticket_table
        """,
        conn1
    )

    conn1.close()

    # -----------------------------
    # BigQuery Authentication
    # -----------------------------

    client1 = bigquery.Client.from_service_account_json(
        "my-project-key.json"
    )

    # -----------------------------
    # Destination Table
    # -----------------------------

    table_id1 = (
        "my-project.customer_support.ticket_table"
    )
	
	
	# ==========================================
    # Delete Existing Rows
    # ==========================================

    delete_sql1 = f"""DELETE FROM my-project.customer_support.ticket_table WHERE TRUE """

    job1 = client1.query(delete_sql1)

    job1.result()

    print("Existing rows deleted from BigQuery table")
	
	
	

    # -----------------------------
    # Upload
    # -----------------------------

    job1 = client1.load_table_from_dataframe(
        df1,
        table_id1
    )

    job1.result()

    print(
        f"{len(df1)} rows uploaded"
    )