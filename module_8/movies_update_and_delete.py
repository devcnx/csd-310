import mysql.connector
from mysql.connector import errorcode
from dotenv import load_dotenv
import os

load_dotenv()

config = {
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASS"),
    "host": os.getenv("DB_HOST"),
    "database": os.getenv("DB_NAME"),
    "raise_on_warnings": True,
}


def show_films(cursor, title):
    """Function to display films with joined genre and studio info."""
    print(f"\n\n-- {title} --")
    query = (
        "SELECT film_name AS Name, film_director AS Director, genre_name AS Genre, studio_name AS 'Studio Name' "
        "FROM film "
        "INNER JOIN genre ON film.genre_id = genre.genre_id "
        "INNER JOIN studio ON film.studio_id = studio.studio_id;"
    )
    cursor.execute(query)
    rows = cursor.fetchall()
    print(f"{'-' * 70}")
    print(
        "{:<20} {:<20} {:<10} {:<20}".format("Name", "Director", "Genre", "Studio Name")
    )
    print(f"{'-' * 70}")
    for row in rows:
        print("{:<20} {:<20} {:<10} {:<20}".format(*row))


try:
    db = mysql.connector.connect(**config)
    cursor = db.cursor()

    # Re-initialize the database by executing the SQL script
    print("\nRe-initializing database...")
    # Construct the absolute path to the SQL file relative to this script's location
    sql_file_path = os.path.join(os.path.dirname(__file__), "db_init_2022.sql")
    with open(sql_file_path, "r") as sql_file:
        sql_script = sql_file.read()

    # Split the script into individual statements and execute them
    sql_commands = sql_script.split(";")
    for command in sql_commands:
        if command.strip() != "":
            cursor.execute(command)
    print("\nDatabase re-initialized successfully.")
    db.commit()

    # 1. Display films before insertion
    show_films(cursor, "DISPLAYING FILMS")

    # First, get the studio_id for Warner Bros
    cursor.execute(
        "SELECT studio_id FROM studio WHERE studio_name = %s", ("Warner Bros",)
    )
    studio_result = cursor.fetchone()
    if studio_result is None:
        print("Warner Bros studio not found in database")
        exit(1)
    studio_id = studio_result[0]

    # Next, get the genre_id for SciFi
    cursor.execute("SELECT genre_id FROM genre WHERE genre_name = %s", ("SciFi",))
    genre_result = cursor.fetchone()
    if genre_result is None:
        print("SciFi genre not found in database")
        exit(1)
    genre_id = genre_result[0]

    # Now insert the film with the obtained IDs
    insert_film = (
        "INSERT INTO film (film_name, film_releaseDate, film_runtime, film_director, studio_id, genre_id) "
        "VALUES (%s, %s, %s, %s, %s, %s)"
    )
    cursor.execute(
        insert_film,
        ("Inception", "2010", 148, "Christopher Nolan", studio_id, genre_id),
    )
    db.commit()

    # 2. Display films after insertion
    show_films(cursor, "DISPLAYING FILMS AFTER INSERT")

    update_query = (
        "UPDATE film SET genre_id = (SELECT genre_id FROM genre WHERE genre_name = 'Horror') "
        "WHERE film_name = 'Alien';"
    )
    cursor.execute(update_query)
    db.commit()

    # 3. Display films after update
    show_films(cursor, "DISPLAYING FILMS AFTER UPDATE - Changed Alien to Horror")

    # 4. Delete 'Gladiator'
    cursor.execute("DELETE FROM film WHERE film_name = 'Gladiator';")
    db.commit()

    # 5. Display films after deletion
    show_films(cursor, "DISPLAYING FILMS AFTER DELETE")

except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("\n  The supplied username or password are invalid")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("\n  The specified database does not exist")
    else:
        print(err)
finally:
    cursor.close()
    db.close()
