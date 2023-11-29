from dbconfig import dbconfig
from config import config
from add import addEntry
from retrieve import retrieveEntries
from getpass import getpass
import hashlib

# Connect to SQL database
db = dbconfig()
cursor = db.cursor()

# Function to check if master password matches users input
def check_mp():
    while True:
        master_password = getpass("Enter MASTER PASSWORD: ")
        hashed_mp = hashlib.sha256(master_password.encode()).hexdigest()
        cursor.execute("SELECT * FROM secrets")
        result = cursor.fetchall()[0]
        if hashed_mp != result[0]:
            print("Incorrect MASTER PASSWORD.")
        else:
            return [master_password, result[1]]
        
# Main function for password manager
def main():
    decryptPassword = False
    # Check if database already exists
    cursor.execute("SHOW DATABASES LIKE 'pm'")
    if cursor.fetchone() is not None:
        # Prompt user to continue with existing database or overwrite it
        status = input("Password manager already exists, type 'NEW' to overwrite it or continue by pressing 'Enter'.\n")
        if status.upper() == "NEW":
            # Delete Database and reconfigure
            cursor.execute("DROP DATABASE pm")
            config()
    else:
        input("Press 'Enter' when ready to create password manager.")
        config()

    cursor.execute("USE pm")
    # Main function loop where user can enter various commands
    while True:
        print("Commands:")
        print("1. Add entry")
        print("2. Retrieve entries")
        print("3. Exit")

        cmd = input("Enter command (1/2/3): ")
        # Handles when a user wants to enter a record into the password managaer
        if cmd == "1":
            res = check_mp()
            # Get entry values from user
            name = input("Enter Site Name (press Enter if not specified):\n")
            url = input("Enter Site URL (press Enter if not specified):\n")
            username = input("Enter Username (press Enter if not specified):\n")
            email = input("Enter Email (press Enter if not specified):\n")
            # Checks for atleast one entry
            if not (name or url or username or email):
                print("Invalid input. Please provide atleast one entry.")
                continue
            if res is not None:
                addEntry(res[0], res[1], name, url, username, email)

        # Handles when a user wants to retrieve information from password manager
        elif cmd == "2":
            res = check_mp()
            search = {}
            # Building search from user input
            site_name = input("Enter Site Name (press Enter if not specified):\n")
            if site_name:
                search["name"] = site_name

            site_url = input("Enter Site URL (press Enter if not specified):\n")
            if site_url:
                search["url"] = site_url

            username = input("Enter Username (press Enter if not specified):\n")
            if username:
                search["username"] = username

            email = input("Enter Email (press Enter if not specified):\n")
            if email:
                search["email"] = email

            if len(search) == 1:
                show_password = input("Enter 'COPY' to copy password to clipboard:\n")
                if show_password == "COPY":
                    decryptPassword = True

            if res is not None:
                retrieveEntries(res[0], res[1], search, decryptPassword)
        # Handles exiting password manager
        elif cmd == "3":
            print("Exiting.")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")
    # Closes database connection
    db.close()

if __name__ == "__main__":
    main()
