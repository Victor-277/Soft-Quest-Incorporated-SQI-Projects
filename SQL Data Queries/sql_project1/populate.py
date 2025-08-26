import pandas as pd
import pymysql
import numpy as np

try:
    print("Connecting to the database...")
    mycon = pymysql.connect(
        host="localhost",
        user="root",
        password="victor",
        database="pollution_db2"
    )
    mycursor = mycon.cursor()

    # Load and clean the CSV
    print("Reading the CSV file...")
    data = pd.read_csv('clean.csv')
    print("CSV file loaded successfully!")
    print("Cleaning the data...")
    data.replace({np.nan: None}, inplace=True)
    data['DateTime'] = pd.to_datetime(data['DateTime'], errors='coerce')  # Ensure proper date parsing

    # Verify 2022 data in the CSV
    print("Filtering data for the year 2022...")
    data_2022 = data[data['DateTime'].dt.year == 2022]
    if data_2022.empty:
        print("No 2022 records found in the CSV.")
    else:
        print(f"Found {data_2022.shape[0]} records for 2022 in the CSV.")

    # Location table
    print("Preparing data for insertion into 'location' table...")
    location_query = "INSERT INTO location (SiteID, Location, geo_point_2d) VALUES (%s, %s, %s)"
    location_data = list(zip(data['SiteID'], data['Location'], data['geo_point_2d']))
    print("Inserting data into the 'location' table...")
    mycursor.executemany(location_query, location_data)
    mycon.commit()
    print(f"{mycursor.rowcount} records inserted successfully into 'location' table.")

    # Instrument table
    print("Preparing data for insertion into 'instrument' table...")
    instrument_query = "INSERT INTO instrument (InstrumentType) VALUES (%s)"
    instrument_data = [(row,) for row in data['Instrument Type']]
    print("Inserting data into the 'instrument' table...")
    mycursor.executemany(instrument_query, instrument_data)
    mycon.commit()
    print(f"{mycursor.rowcount} records inserted successfully into 'instrument' table.")

    # Measurement table (ensure 2022 data is included)
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

    # Ensure 2022 data exists in SQL
    print("Validating 2022 data in the database...")
    mycursor.execute("SELECT COUNT(*) FROM measurement WHERE YEAR(DateTime) = 2022")
    count_2022 = mycursor.fetchone()[0]
    if count_2022 > 0:
        print(f"2022 data is already in the database. {count_2022} records found.")
    else:
        print("No 2022 data in the database. Re-inserting 2022 data...")
        measurement_data_2022 = [
            (
                location_ids[index] if index < len(location_ids) else None,
                instrument_ids[index] if index < len(instrument_ids) else None,
                row['Air Pressure'], row['RH'], row['Location'], row['Temperature'], row['SO2'], 
                row['CO'], row['O3'], row['NVPM2.5'], row['PM10'], row['NVPM10'], row['VPM10'], 
                row['PM2.5'], row['VPM2.5'], row['DateTime'], row['NOx'], row['NO2'], row['NO']
            )
            for index, row in data_2022.iterrows()
        ]
        mycursor.executemany(measurement_query, measurement_data_2022)
        mycon.commit()
        print(f"{len(measurement_data_2022)} 2022 records re-inserted into 'measurement' table.")

    print("Database operations completed.")

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























# import pandas as pd
# import pymysql
# import numpy as np

# try:
#     print("Connecting to the database...")
#     mycon = pymysql.connect(
#         host="localhost",
#         user="root",
#         password="victor",
#         database="pollution_db2"
#     )
#     mycursor = mycon.cursor()

#     # Load CSV
#     print("Reading the CSV file...")
#     data = pd.read_csv('clean.csv')
#     print("CSV file loaded successfully!")
#     print("Cleaning the data...")
#     data.replace({np.nan: None}, inplace=True)  

#     #location table
#     print("Preparing data for insertion into 'location' table...")
#     location_query = "INSERT INTO location (SiteID, Location, geo_point_2d) VALUES (%s, %s, %s)"
#     location_data = list(zip(data['SiteID'], data['Location'], data['geo_point_2d']))
#     print("Inserting data into the 'location' table...")
#     mycursor.executemany(location_query, location_data)
#     mycon.commit()
#     print(f"{mycursor.rowcount} records inserted successfully into 'location' table.")

#     #instrument table
#     print("Preparing data for insertion into 'instrument' table...")
#     instrument_query = "INSERT INTO instrument (InstrumentType) VALUES (%s)"
#     instrument_data = [(row,) for row in data['Instrument Type']]
#     print("Inserting data into the 'instrument' table...")
#     mycursor.executemany(instrument_query, instrument_data)
#     mycon.commit()
#     print(f"{mycursor.rowcount} records inserted successfully into 'instrument' table.")

#     #measurement table
#     print("Fetching location and instrument data...")
#     mycursor.execute("SELECT locationID FROM location")
#     location_ids = [row[0] for row in mycursor.fetchall()]
#     mycursor.execute("SELECT instrumentID FROM instrument")
#     instrument_ids = [row[0] for row in mycursor.fetchall()]
#     print("Preparing data for 'measurement' table...")
#     measurement_data = []
#     for index, row in data.iterrows():
#         location_id = location_ids[index] if index < len(location_ids) else None
#         instrument_id = instrument_ids[index] if index < len(instrument_ids) else None

#         if location_id and instrument_id:
#             measurement_data.append((
#                 location_id, instrument_id, row['Air Pressure'], row['RH'], row['Location'],
#                 row['Temperature'], row['SO2'], row['CO'], row['O3'], row['NVPM2.5'],
#                 row['PM10'], row['NVPM10'], row['VPM10'], row['PM2.5'], row['VPM2.5'],
#                 row['DateTime'], row['NOx'], row['NO2'], row['NO']
#             ))

#     if measurement_data:
#         print(f"Inserting {len(measurement_data)} records into 'measurement' table...")
#         measurement_query = """
#             INSERT INTO measurement (locationID, instrumentID, Air_Pressure, RH, Location, Temperature, SO2, CO, O3, NVPM2_5,
#             PM10, NVPM10, VPM10, PM2_5, VPM2_5, DateTime, NOx, NO2, NO)
#             VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
#         """
#         mycursor.executemany(measurement_query, measurement_data)
#         mycon.commit()
#         print(f"{mycursor.rowcount} records inserted successfully into 'measurement' table.")
#     else:
#         print("No data to insert into 'measurement' table.")

#     #monitoring table
#     print("Preparing data for 'monitoring' table...")
#     monitoring_data = []
#     for index, row in data.iterrows():
#         location_id = location_ids[index] if index < len(location_ids) else None
#         if location_id:
#             monitoring_data.append((row['DateStart'], row['DateEnd'], row['Current'], location_id))

#     if monitoring_data:
#         print(f"Inserting {len(monitoring_data)} records into 'monitoring' table...")
#         monitoring_query = "INSERT INTO monitoring (DateStart, DateEnd, Current, locationID) VALUES (%s, %s, %s, %s)"
#         mycursor.executemany(monitoring_query, monitoring_data)
#         mycon.commit()
#         print(f"{mycursor.rowcount} records inserted successfully into 'monitoring' table.")
#     else:
#         print("No data to insert into 'monitoring' table.")

#     print("Database operations completed.")

# except pymysql.Error as err:
#     print(f"Database error: {err}")

# except Exception as e:
#     print(f"An error occurred: {e}")

# finally:
#     if 'mycursor' in locals() and mycursor:
#         mycursor.close()
#     if 'mycon' in locals() and mycon:
#         mycon.close()
#     print("Database connection closed.")

# # Simple chatbot
# # def chatbot(input_text):
# #     responses = {
# #         "hello": "Hi there! How can I help you?",
# #         "how are you?": "I'm just a bot, but I'm doing fine. What about you?",
# #         "bye": "Goodbye! Have a nice day!"
# #     }
# #     return responses.get(input_text.lower(), "I'm sorry, I don't understand that.")

# # # Test the chatbot
# # while True:
# #     user_input = input("You: ")
# #     if user_input.lower() == "bye":
# #         print("Chatbot:", chatbot(user_input))
# #         break
# #     print("Chatbot:", chatbot(user_input))
