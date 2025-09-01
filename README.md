# Personal Password Manager

A simple command-line password manager for personal use, built with Python and strong encryption.

## Features

- Secure password storage with AES encryption
- Master password protection
- Add, view, update, and delete passwords
- Encrypted local storage
- Simple command-line interface

## Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd PasswordManager
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the password manager:
```bash
python main.py
```

On first run, you'll be prompted to create a master password. This master password is used to encrypt and decrypt all your stored passwords.

### Menu Options

1. **View passwords** - Display all stored passwords (with option to show/hide password)
2. **Add password** - Add a new password entry
3. **Update password** - Modify existing password entries
4. **Delete password** - Remove password entries
5. **Exit** - Close the application

## Security Features

- Master password hashing using SHA-256
- Password encryption using Fernet (AES 128 in CBC mode)
- Key derivation using PBKDF2 with 100,000 iterations
- Encrypted storage in JSON format

## File Structure

- `main.py` - Main application code
- `requirements.txt` - Python dependencies
- `passwords.json` - Encrypted password storage (created after first use)

## Important Notes

- Keep your master password safe - there's no recovery option if lost
- The `passwords.json` file contains your encrypted passwords
- Never share your password database file with others
- Regular backups of your password database are recommended

## Requirements

- Python 3.6+
- cryptography library

## License

This is a personal project for educational purposes.