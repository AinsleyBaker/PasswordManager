from dbconfig import dbconfig
from getpass import getpass
import string
import random
import hashlib

# Function to configure database and master password
def config():
    # Define possible characters
    characters = string.ascii_letters + string.digits + string.punctuation
    # Connect to SQL database
    db = dbconfig()
    cursor = db.cursor()
    # Create and use database
    try:
        cursor.execute("CREATE DATABASE pm")
        cursor.execute("USE pm")
    except Exception as e:
        print("Error: ", e)
    # Format and create 'secrets' and 'manager' tables
    print("-"*80)
    print("Database 'pm' created successfully.")
    print("-"*80)
    cursor.execute("CREATE TABLE secrets (masterkey_hash varchar(100) NOT NULL, device_secret varchar(100) NOT NULL)")
    print("Table 'secrets' created successfully.")
    print("-"*80)
    cursor.execute("CREATE TABLE manager (name varchar(30), url varchar(100), username varchar(30), email varchar(30), password varchar(50))")
    print("Table 'manager' created successfully.")
    print("-"*80)


    while True:
        input_pass = getpass("Choose a MASTER PASSWORD or type 'CHOOSE FOR ME' to randomly generate:")
        # Generating random master password
        if  input_pass.upper() == "CHOOSE FOR ME":
            master_pass = "".join(random.choices(characters, k = 16))
            print("-"*80)
            print("This is your master password, make sure to remember it: ", master_pass)
            print("-"*80)
            input("Press 'Enter' to continue: ")
            break
        # Validating user's master password
        else:
            if len(input_pass) > 10:
                if is_valid_password(input_pass):
                    print("-"*80)
                    if input_pass == getpass("Re-Enter MASTER PASSWORD: "):
                        master_pass = input_pass
                        print("-"*80)
                        print("This is your master password, make sure to remember it: ", master_pass)
                        print("-"*80)
                        input("Press 'Enter' to continue: ")
                        break
                    else:
                        print("-"*80)
                        print("Passwords do not match.")
                        print("-"*80)
                else:
                    print("-"*80)
                    print("Password must contain atleast 1 number, letter and special character.")
                    print("-"*80)
            else:
                print("-"*80)
                print("Password must be at least 10 characters long.")
                print("-"*80)

    # Hash master password using SHA-256
    hashed_mp = hashlib.sha256(master_pass.encode()).hexdigest()
    print("-"*80)
    print("Successfully generated hashed master password.")
    print("-"*80)
    # Generate random device secret
    ds = "".join(random.choices(characters, k = 10))
    print("Successfully generated device secret.")
    print("-"*80)
    # Insert hashed master password and device secret into 'secrets' table
    cursor.execute("INSERT INTO secrets (masterkey_hash, device_secret) VALUES(%s, %s)", (hashed_mp, ds))
    db.commit()
    print("Successfully added to database.")
    print("-"*80)
    print("Configuration complete.")
    print("-"*80)

# Function to check if a password is valid
def is_valid_password(password):
    number = False
    letter = False
    special_char = False
    # Check if password contains at least one number, one letter and one special character
    for char in password:
        if char.isdigit():
            number = True
        elif char.isalpha():
            letter = True
        elif char in string.punctuation:
            special_char = True
    return number and letter and special_char