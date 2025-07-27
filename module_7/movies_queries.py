"""
Name: Brittaney Perry-Morgan
Date: Sunday, June 29th, 2025
Assignment: Module 7.2 Movies: Table Queries

Purpose: Queries the movies database and prints the results.

Imports:
    - os: Used to interact with the operating system.
    - mysql.connector: Used to connect to MySQL database.
    - errorcode: Used to handle MySQL errors.
    - load_dotenv: Used to interact with the `.env` file.
"""

import os
import mysql.connector
from mysql.connector import errorcode
from dotenv import load_dotenv

load_dotenv()

try:
    # Establish database connection using os.getenv() to retrieve variables
    db = mysql.connector.connect(
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
    )
    cursor = db.cursor()

    # Query 1: Select all from the studio table
    print("-- STUDIO TABLE --")
    cursor.execute("SELECT studio_id, studio_name FROM studio")
    for row in cursor.fetchall():
        print(row)
    print("\n")  # Add space for readability

    # Query 2: Select all from the genre table
    print("-- GENRE TABLE --")
    cursor.execute("SELECT genre_id, genre_name FROM genre")
    for row in cursor.fetchall():
        print(row)
    print("\n")

    # Query 3: Select movies with runtime < 120 minutes
    print("-- FILMS WITH RUNTIME LESS THAN 2 HOURS --")
    cursor.execute("SELECT film_name FROM film WHERE film_runtime < 120")
    for row in cursor.fetchall():
        print(row)
    print("\n")

    # Query 4: Group films by director
    print("-- FILMS GROUPED BY DIRECTOR --")
    cursor.execute("SELECT film_director, film_name FROM film ORDER BY film_director")

    current_director = ""
    for director, film_name in cursor.fetchall():
        if director != current_director:
            current_director = director
            print(f"Director: {current_director}")
        print(f"  - {film_name}")

except mysql.connector.Error as err:
    print(f"Error: {err}")

finally:
    # Close connections
    if "cursor" in locals() and cursor is not None:
        cursor.close()
    if "db" in locals() and db.is_connected():
        db.close()
        print("\nDatabase connection closed.")
