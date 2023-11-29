import mysql.connector

# Function to configure and return database connection
def dbconfig():
    try:
        pm_db = mysql.connector.connect(
            host="localhost",
            user="pm",
            password="password_manager123"
        )
    except Exception as e:
        print("Error: ", e)

    return pm_db