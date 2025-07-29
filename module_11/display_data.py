"""
    Title: display_data.py
    Author: Brittaney Perry-Morgan
    Date: July 20th, 2025
    Description: Displays data from the willson_financial database.
"""

import os
import mysql.connector
from constants import (
    NEW_CLIENT_REPORT,
    AVG_ASSETS_REPORT,
    HIGH_TRANSACTION_CLIENTS_REPORT,
)
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
        # Define a list of columns that should be formatted as currency.
        currency_columns = {
            "assets": ["asset_value"],
            "transactions": ["amount"],
            "billings": ["bill_amount"],
        }

        if table_name in currency_columns:
            cols_to_format = currency_columns[table_name]
            cursor.execute(f"SHOW COLUMNS FROM {table_name}")
            all_columns = [col[0] for col in cursor.fetchall()]

            select_expressions = []
            for col in all_columns:
                if col in cols_to_format:
                    select_expressions.append(
                        f"CONCAT('$', FORMAT({col}, 2, 'en_US')) AS {col}"
                    )
                else:
                    select_expressions.append(col)

            query = f"SELECT {', '.join(select_expressions)} FROM {table_name}"
        else:
            query = f"SELECT * FROM {table_name}"

        cursor.execute(query)
        rows = cursor.fetchall()

        if not rows:
            print(f"No Data Found in {table_name}.")
            return

        column_names = [i[0] for i in cursor.description]

        header = " | ".join(f"{name:<20}" for name in column_names)
        print(header)
        print("-" * len(header))

        for row in rows:
            row_data = " | ".join(f"{str(item):<20}" for item in row)
            print(row_data)

    except mysql.connector.Error as err:
        print(f"Error Fetching Data from {table_name}: {err}")


def get_new_client_report(cursor):
    """
    Generates a report on new clients per month for the last 6 months.

    Parameters:
        - cursor: Database cursor object.
        :type cursor: mysql.connector.cursor.MySQLCursor
    """
    print("\n\n-- NEW CLIENT REPORT --")
    try:
        cursor.execute(NEW_CLIENT_REPORT)
        rows = cursor.fetchall()
        for row in rows:
            print(f"Month: {row[0]}, Year: {row[1]}, New Clients: {row[2]}")
    except mysql.connector.Error as err:
        print(f"Error Fetching New Client Report: {err}")


def get_avg_assets_report(cursor):
    """
    Generates a report on the average total asset value per client.

    Parameters:
        - cursor: Database cursor object.
        :type cursor: mysql.connector.cursor.MySQLCursor
    """
    print("\n\n-- AVERAGE ASSETS REPORT --")
    try:
        cursor.execute(AVG_ASSETS_REPORT)
        rows = cursor.fetchall()
        for row in rows:
            print(f"Average Client Assets: {row[0]}")
    except mysql.connector.Error as err:
        print(f"Error Fetching Average Assets Report: {err}")


def get_available_dates(cursor):
    """
    Fetches distinct years and months from the transactions table.

    Parameters:
        - cursor: Database cursor object.

    Returns:
        A dictionary mapping years to a list of months.
    """
    try:
        cursor.execute(
            "SELECT DISTINCT YEAR(txn_date), MONTH(txn_date) FROM transactions ORDER BY 1, 2"
        )
        dates = {}
        for year, month in cursor.fetchall():
            if year not in dates:
                dates[year] = []
            dates[year].append(month)
        return dates
    except mysql.connector.Error as err:
        print(f"Error Fetching Available Dates: {err}")
        return {}


def prompt_for_date(available_dates):
    """
    Prompts the user to select a year and month from available dates.

    If only one year is available, it is selected automatically.

    Parameters:
        - available_dates: A dictionary of available years and months.
        :type available_dates: dict

    Returns:
        - A tuple containing the selected year and month.
        :rtype: tuple
    """
    if not available_dates:
        print("No Transaction Data Available to Generate a Report.")
        return None, None

    available_years = list(available_dates.keys())

    if len(available_years) == 1:
        year = available_years[0]
        print(f"\n({year}) Selected Automatically.")
    else:
        # Prompt for year
        while True:
            print("\nAvailable Years:", available_years)
            try:
                year = int(input("Select a Year: "))
                if year in available_dates:
                    break
                else:
                    print("Invalid Year. Please Select from the Available Options.")
            except ValueError:
                print("Invalid Input. Please Enter a Number.")

    while True:
        print(f"\nAvailable Months for {year}: {available_dates[year]}")
        try:
            month = int(input("Select a Month: "))
            if month in available_dates[year]:
                break
            else:
                print("***Invalid Month. Please Select from the Available Options.\n")
        except ValueError:
            print("***Invalid Input. Please Enter a Number.\n")

    return year, month


def get_high_transaction_clients_report(cursor, year, month):
    """
    Generates a report on clients with the highest number of transactions.

    Parameters:
        - cursor: Database cursor object.
        :type cursor: mysql.connector.cursor.MySQLCursor

        - year: The year to filter the report by.
        :type year: int

        - month: The month to filter the report by.
        :type month: int
    """
    print(f"\n\n-- HIGH TRANSACTION CLIENTS REPORT FOR {year}-{month:02d} --")
    try:
        cursor.execute(HIGH_TRANSACTION_CLIENTS_REPORT, (year, month))

        result_found = False
        while True:
            if rows := cursor.fetchall():
                result_found = True
                columns = [i[0] for i in cursor.description]
                print(" | ".join(f"{col:<25}" for col in columns))
                print("-" * (28 * len(columns)))
                for row in rows:
                    print(" | ".join(f"{str(item):<25}" for item in row))
                print("\n")

            if not cursor.nextset():
                break

        if not result_found:
            print(
                f"No Clients Found with More than 10 Transactions in {year}-{month:02d}.\n"
            )

    except mysql.connector.Error as err:
        print(f"Error Fetching High Transaction Clients Report: {err}")


def main():
    """
    Main Function to Connect to the Database and Display Table Data.
    """
    db = None
    cursor = None
    try:
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

        print("Successfully Connected to the 'willson_financial' Database.")

        tables_to_show = ["clients", "assets", "transactions", "billings"]
        for table in tables_to_show:
            show_table_data(cursor, table)

        get_new_client_report(cursor)
        get_avg_assets_report(cursor)

        available_dates = get_available_dates(cursor)
        year, month = prompt_for_date(available_dates)

        get_high_transaction_clients_report(cursor, year, month)

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
