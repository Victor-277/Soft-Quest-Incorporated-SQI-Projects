import pandas as pd
import pymysql
import numpy as np
import os

# MySQL database connection setup
try:
    print("Connecting to MySQL database...")
    conn = pymysql.connect(
        host="localhost",
        user="root",
        password="victor",  
        database="chinook"
    )
    cursor = conn.cursor()
    print("Connected successfully!")

    # Chinook CSV files
    csv_files = [
        "Artist.csv",
        "Album.csv",
        "Genre.csv",
        "MediaType.csv",
        "Track.csv",
        "Employee.csv",
        "Customer.csv",
        "Invoice.csv",
        "InvoiceLine.csv",
        "Playlist.csv",
        "PlaylistTrack.csv"
    ]

    for file in csv_files:
        table_name = file.replace(".csv", "")
        print(f"Loading {file} into {table_name}...")

        if not os.path.exists(file):
            print(f"File not found: {file}")
            continue

        try:
            df = pd.read_csv(file)

            # Convert NaN to None so MySQL can accept NULL
            df.replace({np.nan: None}, inplace=True)

            # Build INSERT query
            cols = ", ".join(df.columns)
            placeholders = ", ".join(["%s"] * len(df.columns))
            insert_query = f"INSERT INTO {table_name} ({cols}) VALUES ({placeholders})"

            cursor.executemany(insert_query, df.values.tolist())
            conn.commit()
            print(f"{cursor.rowcount} rows inserted into '{table_name}'")
        except Exception as e:
            print(f"Error loading {file}: {e}")

except pymysql.Error as err:
    print(f"Database error: {err}")
except Exception as e:
    print(f"General error: {e}")
finally:
    if 'cursor' in locals():
        cursor.close()
    if 'conn' in locals():
        conn.close()
    print("Database connection closed.")
