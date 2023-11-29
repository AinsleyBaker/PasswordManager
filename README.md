# PasswordManager
A local secure password manager that uses python and MySQL. Uses SHA-512 for hasing passwords, PBKDF2 for deriving a key and AES-256 for encrypting stored passwords.
Users must configurate password manager beforehand and will be prompted to enter a master password or auto generate a 16 character long password they must remember.
Allows users to enter in site name, site url, username, email and manually or auto generate secure password.
Users can retreieve entries and decide whether to hide or copy password to clipboard.
