# VaultBoxX

VaultBoxX is a desktop password manager built with Python, MongoDB, CustomTkinter, and cryptography. It includes a modern dark GUI for saving, viewing, searching, deleting, and generating credentials.

This project is designed as a learning and portfolio project that demonstrates Python desktop development, database integration, password encryption, and modular application structure.

## Features

- Master password login
- Encrypted password storage
- Modern CustomTkinter desktop GUI
- Dashboard with credential statistics
- Add credential form
- Searchable credential list
- Hidden passwords by default
- Show password and copy password actions
- Delete credential confirmation popup
- Password generator with length slider
- Theme switch and about section
- Original console version included

## Tech Stack

- Python
- CustomTkinter
- MongoDB
- PyMongo
- cryptography

## Project Structure

```text
VaultBoxX/
|-- app.py
|-- auth.py
|-- database.py
|-- encryption.py
|-- gui.py
|-- password_generator.py
|-- requirements.txt
|-- screens/
|   |-- __init__.py
|   |-- add_credential.py
|   |-- base.py
|   |-- dashboard.py
|   |-- login_screen.py
|   |-- password_generator_page.py
|   |-- settings.py
|   |-- view_credentials.py
|-- test_db.py
|-- test_encryption.py
```

## Installation

Clone the repository:

```powershell
git clone https://github.com/your-username/VaultBoxX.git
cd VaultBoxX
```

Create and activate a virtual environment:

```powershell
python -m venv .venv
.venv\Scripts\activate
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

## MongoDB Setup

VaultBoxX uses a local MongoDB database. Make sure MongoDB is installed and running on your machine.

The current connection string is defined in `database.py`:

```text
mongodb://localhost:27017
```

The app uses:

```text
Database: vaultboxx
Collection: credentials
```

## Run the GUI

Start the desktop app:

```powershell
python gui.py
```

Default demo master password:

```text
mysecret123
```

## Run the Console Version

The original command-line version is still available:

```powershell
python app.py
```

## Run Tests

Run the included test files:

```powershell
python test_encryption.py
python test_db.py
```

## Backend Modules

The GUI imports and uses the existing backend modules:

- `auth.py` verifies the master password.
- `database.py` handles MongoDB credential storage.
- `encryption.py` encrypts and decrypts passwords.
- `password_generator.py` creates random passwords.

## Security Notice

VaultBoxX is an educational project and should not be used as a production password manager without additional security review.

Current limitations:

- The demo master password is hardcoded in `auth.py`.
- There is no first-time user setup flow.
- There is no account recovery flow.
- Credential deletion currently uses the website name.
- Secrets are not loaded from environment variables.

Recommended production improvements:

- Store a salted hash of the master password instead of a hardcoded value.
- Add first-time setup for the master password.
- Use environment variables for configuration.
- Delete credentials by MongoDB `_id`.
- Add stronger automated tests.
- Package the app as a desktop executable.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
