#!/usr/bin/env python3
"""
Simple Password Manager
A basic command-line password manager for personal use
"""

import sys
import json
import os
from getpass import getpass
import hashlib
from cryptography.fernet import Fernet
import base64


class PasswordManager:
    def __init__(self, data_file="passwords.json"):
        self.data_file = data_file
        self.master_password_hash = None
        self.cipher_suite = None
        self.passwords = {}
        
    def start(self):
        print("=== Personal Password Manager ===")
        if not os.path.exists(self.data_file):
            print("First time setup - creating new password database")
            self.setup_master_password()
        else:
            print("Enter your master password to continue")
            if not self.authenticate():
                print("Authentication failed!")
                sys.exit(1)
        
        self.main_menu()
    
    def setup_master_password(self):
        while True:
            master_pass = getpass("Create a master password: ")
            confirm_pass = getpass("Confirm master password: ")
            
            if master_pass == confirm_pass:
                self.master_password_hash = self._hash_password(master_pass)
                key = self._derive_key(master_pass)
                self.cipher_suite = Fernet(key)
                self.save_data()
                print("Master password created successfully!")
                break
            else:
                print("Passwords don't match. Try again.")
    
    def authenticate(self):
        try:
            with open(self.data_file, 'r') as f:
                data = json.load(f)
                stored_hash = data.get('master_hash')
        except:
            return False
            
        master_pass = getpass("Master password: ")
        if self._hash_password(master_pass) == stored_hash:
            key = self._derive_key(master_pass)
            self.cipher_suite = Fernet(key)
            self.load_data()
            return True
        return False
    
    def main_menu(self):
        while True:
            print("\n--- Password Manager ---")
            print("1. View passwords")
            print("2. Add password")
            print("3. Update password")
            print("4. Delete password")
            print("5. Exit")
            
            choice = input("Choose an option (1-5): ").strip()
            
            if choice == '1':
                self.view_passwords()
            elif choice == '2':
                self.add_password()
            elif choice == '3':
                self.update_password()
            elif choice == '4':
                self.delete_password()
            elif choice == '5':
                print("Goodbye!")
                break
            else:
                print("Invalid option. Please try again.")
    
    def _hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()
    
    def _derive_key(self, password):
        key = hashlib.pbkdf2_hmac('sha256', password.encode(), b'salt', 100000)
        return base64.urlsafe_b64encode(key)
    
    def view_passwords(self):
        if not self.passwords:
            print("No passwords stored yet.")
            return
        
        print("\n--- Your Passwords ---")
        for service, data in self.passwords.items():
            print(f"Service: {service}")
            print(f"Username: {data['username']}")
            show_pass = input(f"Show password for {service}? (y/n): ").lower()
            if show_pass == 'y':
                print(f"Password: {data['password']}")
            print("-" * 30)
    
    def add_password(self):
        service = input("Service name (e.g., Gmail, Facebook): ").strip()
        username = input("Username/Email: ").strip()
        password = getpass("Password: ")
        
        if service in self.passwords:
            overwrite = input(f"Password for {service} already exists. Overwrite? (y/n): ")
            if overwrite.lower() != 'y':
                return
        
        self.passwords[service] = {
            'username': username,
            'password': password
        }
        
        self.save_data()
        print(f"Password for {service} saved successfully!")
    
    def update_password(self):
        if not self.passwords:
            print("No passwords to update.")
            return
        
        print("\nServices:")
        for service in self.passwords:
            print(f"- {service}")
        
        service = input("Which service to update: ").strip()
        if service not in self.passwords:
            print("Service not found.")
            return
        
        print(f"Current username: {self.passwords[service]['username']}")
        new_username = input("New username (press enter to keep current): ").strip()
        new_password = getpass("New password: ")
        
        if new_username:
            self.passwords[service]['username'] = new_username
        self.passwords[service]['password'] = new_password
        
        self.save_data()
        print(f"Password for {service} updated successfully!")
    
    def delete_password(self):
        if not self.passwords:
            print("No passwords to delete.")
            return
        
        print("\nServices:")
        for service in self.passwords:
            print(f"- {service}")
        
        service = input("Which service to delete: ").strip()
        if service not in self.passwords:
            print("Service not found.")
            return
        
        confirm = input(f"Are you sure you want to delete {service}? (y/n): ")
        if confirm.lower() == 'y':
            del self.passwords[service]
            self.save_data()
            print(f"Password for {service} deleted successfully!")
    
    def save_data(self):
        data = {
            'master_hash': self.master_password_hash,
            'passwords': {}
        }
        
        for service, creds in self.passwords.items():
            encrypted_username = self.cipher_suite.encrypt(creds['username'].encode()).decode()
            encrypted_password = self.cipher_suite.encrypt(creds['password'].encode()).decode()
            data['passwords'][service] = {
                'username': encrypted_username,
                'password': encrypted_password
            }
        
        with open(self.data_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def load_data(self):
        try:
            with open(self.data_file, 'r') as f:
                data = json.load(f)
                self.master_password_hash = data.get('master_hash')
                
                self.passwords = {}
                for service, creds in data.get('passwords', {}).items():
                    decrypted_username = self.cipher_suite.decrypt(creds['username'].encode()).decode()
                    decrypted_password = self.cipher_suite.decrypt(creds['password'].encode()).decode()
                    self.passwords[service] = {
                        'username': decrypted_username,
                        'password': decrypted_password
                    }
        except Exception as e:
            print(f"Error loading data: {e}")
            self.passwords = {}


if __name__ == "__main__":
    pm = PasswordManager()
    pm.start()