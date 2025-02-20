import os
import requests
import time
import json
import logging
import hashlib
from twilio.rest import Client
import socket

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Constants for security
MAX_LOGIN_ATTEMPTS = 3
RESET_THRESHOLD = 3  # Number of failed attempts before account reset
BLOCK_TIME = 24 * 3600  # 24 hours in seconds

# Load credentials from environment variables
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID', 'your_sid_here')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN', 'your_token_here')
TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER', '+15156196481')
YOUR_PHONE_NUMBER = os.getenv('YOUR_PHONE_NUMBER', '+919630021121')

# File paths for storing failed login attempts and blocked IP addresses
failed_attempts_file = "failed_attempts.json"
blocked_ips_file = "blocked_ips.json"
reset_accounts_file = "reset_accounts.json"

# Function to load data from a JSON file
def load_data(file_path):
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

# Function to save data to a JSON file
def save_data(data, file_path):
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)

# Function to block an IP address for 24 hours
def block_ip(ip_address):
    current_time = time.time()
    blocked_ips[ip_address] = current_time + BLOCK_TIME
    save_data(blocked_ips, blocked_ips_file)
    logging.info(f"Blocked IP {ip_address} for 24 hours.")

# Function to get the local IP address of the device
def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception as e:
        logging.error(f"Unable to retrieve local IP address: {e}")
        return None

# Initialize blocked IPs, failed login attempts, and reset accounts
blocked_ips = load_data(blocked_ips_file)
failed_attempts = load_data(failed_attempts_file)
reset_accounts = load_data(reset_accounts_file)

# Function to reset an account's password
def reset_account(username):
    logging.info(f"Resetting account for {username}...")
    reset_accounts[username] = 0
    save_data(reset_accounts, reset_accounts_file)

# Function to hash a password (for security)
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Predefined user credentials (hashed passwords)
stored_users = {
    "user123": hash_password("password")  # Replace with actual user database
}

# Function to handle login attempts
def login(username, password):
    local_ip = get_local_ip()
    
    if not local_ip:
        logging.error("Login failed due to IP retrieval issue.")
        return False

    if local_ip in blocked_ips and time.time() < blocked_ips[local_ip]:
        logging.warning("Access denied: IP address is blocked.")
        return False

    if username in reset_accounts and reset_accounts[username] >= RESET_THRESHOLD:
        logging.warning(f"Account {username} requires a password reset.")
        return False

    if username in stored_users and stored_users[username] == hash_password(password):
        reset_accounts.pop(username, None)
        return True
    
    failed_attempts[local_ip] = failed_attempts.get(local_ip, 0) + 1
    save_data(failed_attempts, failed_attempts_file)

    reset_accounts[username] = reset_accounts.get(username, 0) + 1
    save_data(reset_accounts, reset_accounts_file)

    if reset_accounts[username] >= RESET_THRESHOLD:
        logging.warning(f"Account {username} reached reset threshold.")
        reset_account(username)
        return False
    
    return False

# Main authentication loop
for attempt in range(MAX_LOGIN_ATTEMPTS):
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    if login(username, password):
        print("Login successful!")
        break
    else:
        print("Login failed. Please try again.")
        if attempt < MAX_LOGIN_ATTEMPTS - 1:
            print(f"You have {MAX_LOGIN_ATTEMPTS - attempt - 1} attempts left.")
        else:
            print("Too many failed attempts. Blocking IP and sending notification...")
            block_ip(get_local_ip())
            client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
            client.messages.create(
                body="Multiple login attempts detected. Your IP has been blocked for 24 hours.",
                from_=TWILIO_PHONE_NUMBER,
                to=YOUR_PHONE_NUMBER
            )
            print("Notification sent. IP blocked for 24 hours.")
