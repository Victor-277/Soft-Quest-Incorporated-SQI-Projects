import pandas as pd
import pymysql
import numpy as np

try:
    print("Connecting to the database...")
    mycon = pymysql.connect(
        host="localhost",
        user="root",
        password="victor",
        database="insert_100"
    )
    mycursor = mycon.cursor()

    # Load CSV
    print("Reading the CSV file...")
    data = pd.read_csv('cropped_clean.csv')
    print("CSV file loaded successfully!")
    print("Cleaning the data...")
    data.replace({np.nan: None}, inplace=True)  

    #location table
    print("Preparing data for insertion into 'location' table...")
    location_query = "INSERT INTO location (SiteID, Location, geo_point_2d) VALUES (%s, %s, %s)"
    location_data = list(zip(data['SiteID'], data['Location'], data['geo_point_2d']))
    print("Inserting data into the 'location' table...")
    mycursor.executemany(location_query, location_data)
    mycon.commit()
    print(f"{mycursor.rowcount} records inserted successfully into 'location' table.")

    #instrument table
    print("Preparing data for insertion into 'instrument' table...")
    instrument_query = "INSERT INTO instrument (InstrumentType) VALUES (%s)"
    instrument_data = [(row,) for row in data['Instrument Type']]
    print("Inserting data into the 'instrument' table...")
    mycursor.executemany(instrument_query, instrument_data)
    mycon.commit()
    print(f"{mycursor.rowcount} records inserted successfully into 'instrument' table.")

    #measurement table
    print("Fetching location and instrument data...")
    mycursor.execute("SELECT locationID FROM location")
    location_ids = [row[0] for row in mycursor.fetchall()]
    mycursor.execute("SELECT instrumentID FROM instrument")
    instrument_ids = [row[0] for row in mycursor.fetchall()]
    print("Preparing data for 'measurement' table...")
    measurement_data = []
    for index, row in data.iterrows():
        location_id = location_ids[index] if index < len(location_ids) else None
        instrument_id = instrument_ids[index] if index < len(instrument_ids) else None

        if location_id and instrument_id:
            measurement_data.append((
                location_id, instrument_id, row['Air Pressure'], row['RH'], row['Location'],
                row['Temperature'], row['SO2'], row['CO'], row['O3'], row['NVPM2.5'],
                row['PM10'], row['NVPM10'], row['VPM10'], row['PM2.5'], row['VPM2.5'],
                row['DateTime'], row['NOx'], row['NO2'], row['NO']
            ))

    if measurement_data:
        print(f"Inserting {len(measurement_data)} records into 'measurement' table...")
        measurement_query = """
            INSERT INTO measurement (locationID, instrumentID, Air_Pressure, RH, Location, Temperature, SO2, CO, O3, NVPM2_5,
            PM10, NVPM10, VPM10, PM2_5, VPM2_5, DateTime, NOx, NO2, NO)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        mycursor.executemany(measurement_query, measurement_data)
        mycon.commit()
        print(f"{mycursor.rowcount} records inserted successfully into 'measurement' table.")
    else:
        print("No data to insert into 'measurement' table.")

    #monitoring table
    print("Preparing data for 'monitoring' table...")
    monitoring_data = []
    for index, row in data.iterrows():
        location_id = location_ids[index] if index < len(location_ids) else None
        if location_id:
            monitoring_data.append((row['DateStart'], row['DateEnd'], row['Current'], location_id))

    if monitoring_data:
        print(f"Inserting {len(monitoring_data)} records into 'monitoring' table...")
        monitoring_query = "INSERT INTO monitoring (DateStart, DateEnd, Current, locationID) VALUES (%s, %s, %s, %s)"
        mycursor.executemany(monitoring_query, monitoring_data)
        mycon.commit()
        print(f"{mycursor.rowcount} records inserted successfully into 'monitoring' table.")
    else:
        print("No data to insert into 'monitoring' table.")

    print("Database operations completed.")

except pymysql.Error as err:
    print(f"Database error: {err}")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    if 'mycursor' in locals() and mycursor:
        mycursor.close()
    if 'mycon' in locals() and mycon:
        mycon.close()
    print("Database connection closed.")

