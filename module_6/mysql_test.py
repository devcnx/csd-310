"""
Name: Brittaney Perry-Morgan
Date: Sunday, June 29th, 2025
Assignment: Module 6.2 Movies: Setup

Purpose: Connect to MySQL database and test connection.

Imports:
    - mysql.connector: Used to connect to MySQL database.
    - errorcode: Used to handle MySQL errors.
    - dotenv: Used to interact with the `.env` file.
    - dotenv_values: Used to load environment variables from the `.env` file.
"""

from dotenv import load_dotenv
import os

load_dotenv()

import mysql.connector
from mysql.connector import errorcode

if __name__ == "__main__":
    config = {
        "user": os.getenv("DB_USER"),
        "password": os.getenv("DB_PASS"),
        "host": os.getenv("DB_HOST"),
        "database": os.getenv("DB_NAME"),
        "port": os.getenv("DB_PORT"),
        "raise_on_warnings": True,
        "auth_plugin": "caching_sha2_password",
    }

    db = None
    try:
        db = mysql.connector.connect(**config)
        print(f"\nUser {os.getenv("DB_USER")} Connected")
        print(f"Host {os.getenv("DB_HOST")}")
        print(f"Database {os.getenv("DB_NAME")}")
        input("\n\nPress Enter to Continue...")
    except mysql.connector.Error as error:
        if error.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("The Supplied Username or Password is Invalid")
        elif error.errno == errorcode.ER_BAD_DB_ERROR:
            print("The Specified Database Does Not Exist")
        else:
            print(f"Error: {error}")
    finally:
        if db and db.is_connected():
            db.close()
