# Password Manager (GUI)

A simple and secure password manager built in Python using a Tkinter graphical interface. The application allows users to safely store, manage, and update account credentials locally using an encrypted vault.

## Features

- Master key protected vault
- Encrypted password storage
- Tkinter-based GUI
- Add, edit, and delete accounts
- Show/Hide password toggle
- Account list sorting
- Local secure storage
- Account information update window

## Screenshots

*(Add screenshots of the GUI here later if you want)*

## Installation

### 1. Clone the repository

git clone https://github.com/KevinCaudell/Secure-Password-Manager-GUI.git

### 2. Move into project directory

cd Secure-Password-Manager-GUI

### 3. Run the Program

python main.py

## Usage

1. Launch the application
2. Create or enter your master key
3. Add Accounts with usernames and passwords
4. Select an account to view details
5. Use the Show/Hide button to reveal passwords
6. Modify account Information using the Change Info Window
7. Delete account by account name
8. Filter through accounts A --> Z or Z --> A or by search

## Security Notes

* Passwords are stored locally in encrypted form
* The masterkey is needed to unlock vault
* Do not share your masterkey
* Keep your vault file private

## Project Structure

```
main.py         # Runs Program
gui.py          # GUI Setup
guiFuncs.py     # GUI helper functions
vault.py        # Vault handling and encryption logic
utilities.py    # Helper utilities
```

## Contributing

Contributions, suggestions, and improvements are welcome. Feel free to open an issue or submit a pull request.

## License

This project is licensed under MIT License.

