"""
    Title: display_data.py
    Author: Brittaney Perry-Morgan
    Date: July 13th, 2025
    Description: Displays data from the willson_financial database.
"""

import os
import mysql.connector
from mysql.connector import errorcode
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def show_table_data(cursor, table_name):
    """
    Function to display all data from a table with dynamic formatting.

    Parameters:
        - cursor: Database cursor object.
        :type cursor: mysql.connector.cursor.MySQLCursor

        - table_name: The name of the table to display data from.
        :type table_name: str
    """
    print(f"\n--- {table_name.upper()} ---")
    try:
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()

        if not rows:
            print(f"No data found in {table_name}.")
            return

        # Get column names from cursor.description
        column_names = [i[0] for i in cursor.description]

        # Print header
        header = " | ".join(f"{name:<20}" for name in column_names)
        print(header)
        print("-" * len(header))

        # Print rows
        for row in rows:
            row_data = " | ".join(f"{str(item):<20}" for item in row)
            print(row_data)

    except mysql.connector.Error as err:
        print(f"Error fetching data from {table_name}: {err}")


def main():
    """
    Main function to connect to the database and display table data.
    """
    db = None
    cursor = None
    try:
        # Get database credentials from environment variables
        db_user = os.getenv("DB_USER")
        db_password = os.getenv("DB_PASSWORD")
        db_host = os.getenv("DB_HOST", "localhost")

        if not db_user or not db_password:
            print(
                "Error: Database Credentials (DB_USER, DB_PASSWORD) Not Found in .env File."
            )
            return

        config = {
            "user": db_user,
            "password": db_password,
            "host": db_host,
            "database": "willson_financial",
            "raise_on_warnings": True,
        }

        db = mysql.connector.connect(**config)
        cursor = db.cursor()

        print("Successfully connected to the 'willson_financial' database.")

        tables_to_show = ["clients", "assets", "transactions", "billings"]
        for table in tables_to_show:
            show_table_data(cursor, table)

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something Is Wrong With Your User Name Or Password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database Does Not Exist")
        else:
            print(f"Error: {err}")
    finally:
        if cursor:
            cursor.close()
        if db and db.is_connected():
            db.close()
            print("\nMySQL Connection Is Closed.")


if __name__ == "__main__":
    main()
