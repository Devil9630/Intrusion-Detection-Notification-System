import requests
import time
import json
from twilio.rest import Client
import socket

# Constants for security
MAX_LOGIN_ATTEMPTS = 3
RESET_THRESHOLD = 3  # Number of failed attempts before account reset
BLOCK_TIME = 24 * 3600  # 24 hours in seconds

# Load credentials from environment variables
TWILIO_ACCOUNT_SID = 'AC2e80da7e1b6396f5b2b77dee6e52f84f'
TWILIO_AUTH_TOKEN = '844dabdf3c38df041b240e00dcaf6749'
TWILIO_PHONE_NUMBER = '+15156196481'
YOUR_PHONE_NUMBER = '+919630021121'

# File paths for storing failed login attempts and blocked IP addresses
failed_attempts_file = "failed_attempts.json"
blocked_ips_file = "blocked_ips.json"
reset_accounts_file = "reset_accounts.json"

# Function to load data from a JSON file
def load_data(file_path):
    try:
        with open(file_path, "r") as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        return {}

# Function to save data to a JSON file
def save_data(data, file_path):
    with open(file_path, "w") as file:
        json.dump(data, file)

# Function to block an IP address for 24 hours
def block_ip(ip_address):
    current_time = time.time()
    block_time = current_time + BLOCK_TIME  # 24 hours in seconds
    blocked_ips[ip_address] = block_time
    save_data(blocked_ips, blocked_ips_file)

# Function to get the local IP address of the device
def get_local_ip():
    try:
        # Create a socket connection to an external server
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))  # Google's DNS server
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception as e:
        print(f"Unable to retrieve local IP address: {e}")
        return None

# Initialize blocked IPs, failed login attempts, and reset accounts
blocked_ips = load_data(blocked_ips_file)
failed_attempts = load_data(failed_attempts_file)
reset_accounts = load_data(reset_accounts_file)

# Function to reset an account's password
def reset_account(username):
    # In a real-world scenario, you would implement a secure account reset mechanism here.
    print(f"Resetting account for {username}...")

# Function to handle login attempts
def login(username, password):
    local_ip = get_local_ip()
    
    if local_ip is None:
        print("Unable to retrieve your local IP address. Login failed.")
        return False

    if local_ip in blocked_ips and time.time() < blocked_ips[local_ip]:
        return False  # IP address is blocked

    if username in reset_accounts:
        if reset_accounts[username] >= RESET_THRESHOLD:
            print(f"Account {username} has been reset. Please reset your password.")
            return False

    # Replace with database lookup for user's plain password
    stored_password = "password"  # Replace with actual plain password

    if username == "user123" and password == stored_password:
        if username in reset_accounts:
            del reset_accounts[username]  # Reset successful, remove from reset list
        return True
    else:
        if local_ip in failed_attempts:
            failed_attempts[local_ip] += 1
        else:
            failed_attempts[local_ip] = 1
        save_data(failed_attempts, failed_attempts_file)

        if username in reset_accounts:
            reset_accounts[username] += 1
        else:
            reset_accounts[username] = 1
            save_data(reset_accounts, reset_accounts_file)

        if reset_accounts[username] >= RESET_THRESHOLD:
            print(f"Account {username} has reached the reset threshold.")
            reset_account(username)  # Reset the account
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
            print("You have no more login attempts. Sending notification and blocking IP address...")

            # Block the IP address for 24 hours
            block_ip(get_local_ip())

            # Initialize the Twilio client
            client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

            # Send a notification
            message = client.messages.create(
                body="Multiple login attempts detected. Your IP address has been blocked for 24 hours. Please try again later or reset your account.",
                from_=TWILIO_PHONE_NUMBER,
                to=YOUR_PHONE_NUMBER
            )
            print("Notification sent to your phone number and IP address blocked for 24 hours.")
