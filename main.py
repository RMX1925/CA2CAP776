import csv
import hashlib
import bcrypt
import requests
import re
import time
from tabulate import tabulate 

# NASA API URL and key
NASA_NEO_URL = "https://api.nasa.gov/neo/rest/v1/feed"
NASA_SSD_URL = "https://ssd-api.jpl.nasa.gov/"
API_KEY = "mhjOl1aQsiYEWCYAx4NfvjWh4uh8IKbxvDNkvdbn"

LOGIN_ATTEMPTS_LIMIT = 5

def load_users_from_csv():
    users = {}
    try:
        with open('regno.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                users[row['email']] = {
                    'hashed_password': row['hashed_password'],
                    'security_question': row['security_question'],
                    'security_answer': row['security_answer']
                }
    except FileNotFoundError:
        print("User data file not found.")
    return users

def save_user_to_csv(email, hashed_password, security_question, security_answer):
    with open('regno.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([email, hashed_password, security_question, security_answer])

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def validate_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def validate_password(password):
    return (len(password) >= 8 and re.search(r'[!@#$%^&*(),.?":{}|<>]', password))

def sign_up_user(users):
    email = input("Enter your email: ")
    if email in users:
        print("Email already registered. Please login.")
        return False

    if not validate_email(email):
        print("Invalid email format.")
        return False

    password = input("Enter your password: ")
    while not validate_password(password):
        print("Password must be at least 8 characters long and contain one special character.")
        password = input("Enter your password: ")

    security_question = input("Enter a security question: ")
    security_answer = input("Enter the answer to your security question: ")

    hashed_password = hash_password(password)
    save_user_to_csv(email, hashed_password, security_question, security_answer)
    users[email] = {
        'hashed_password': hashed_password,
        'security_question': security_question,
        'security_answer': security_answer
    }
    print("Sign-up successful!")
    return True

def login_user(users):
    attempts = 0
    while attempts < LOGIN_ATTEMPTS_LIMIT:
        email = input("Enter your email: ")
        if email not in users:
            print("Email not found. Try again.")
            attempts += 1
            continue
        
        password = input("Enter your password: ")
        hashed_password = users[email]['hashed_password']
        
        if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
            print("Login successful!")
            return email  # Return email after successful login
        else:
            print("Incorrect password. Try again.")
            attempts += 1
    
    print("Too many failed login attempts. Please try later.")
    return False

def reset_password(users):
    email = input("Enter your registered email for password reset: ")
    if email not in users:
        print("Email not found.")
        return

    security_question = users[email]['security_question']
    print(f"Security Question: {security_question}")
    security_answer = input("Answer: ")
    
    if security_answer == users[email]['security_answer']:
        new_password = input("Enter new password: ")
        while not validate_password(new_password):
            print("Password must be at least 8 characters long and contain one special character.")
            new_password = input("Enter new password: ")
        
        users[email]['hashed_password'] = hash_password(new_password)
        print("Password reset successfully!")
        return True
    else:
        print("Incorrect security answer.")
        return False

def fetch_nasa_neo_data():
    try:
        params = {
            'start_date': '2024-10-01',
            'end_date': '2024-10-01',
            'api_key': API_KEY
        }
        response = requests.get(NASA_NEO_URL, params=params)
        response.raise_for_status()
        data = response.json()

        # Prepare data for table
        table_data = []
        for date, objects in data['near_earth_objects'].items():
            for obj in objects:
                table_data.append([
                    obj['name'],
                    obj['close_approach_data'][0]['close_approach_date'],
                    obj['estimated_diameter']['meters']['estimated_diameter_max'],
                    obj['close_approach_data'][0]['relative_velocity']['kilometers_per_hour'],
                    obj['close_approach_data'][0]['miss_distance']['kilometers'],
                    obj['is_potentially_hazardous_asteroid']
                ])

        # Print data in table format
        print("\nNear-Earth Objects (NEO) Data:")
        headers = ["Name", "Close Approach Date", "Estimated Diameter (m)", "Velocity (km/h)", "Miss Distance (km)", "Hazardous"]
        print(tabulate(table_data, headers=headers, tablefmt="grid"))
    except requests.exceptions.RequestException as e:
        print(f"Error fetching NEO data: {e}")

def fetch_ssd_data():
    """Fetch Solar System Dynamics data from the NASA API."""
    url = "https://ssd-api.jpl.nasa.gov/sbdb.api"
    
    params = {
        "sstr": "Ceres",
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        # Prepare data for table
        table_data = [
            ["Name", data['object']['fullname']],
            ["Object Type", data['object']['spkid']],
            ["Discovery Date", data.get('object', {}).get('disc', 'N/A')],
            ["Semi-major Axis", f"{data['orbit']['elements'][0]['value']} AU"],
            ["Eccentricity", data['orbit']['elements'][1]['value']],
            ["Inclination", f"{data['orbit']['elements'][2]['value']} degrees"],
            ["Diameter", f"{data.get('phys_par', {}).get('diameter', 'Unknown')} km"]
        ]

        # Print data in table format
        print("\nSolar System Object Data (Ceres):")
        print(tabulate(table_data, tablefmt="grid"))
    except requests.exceptions.RequestException as e:
        print(f"Error fetching SSD data: {e}")

def logged_in_menu():
    while True:
        print("\nLogged In - Select an option:")
        print("1. Fetch NEO Data")
        print("2. Fetch SSD Data")
        print("3. Log out")
        choice = input("Choose an option: ")

        if choice == '1':
            fetch_nasa_neo_data()
        elif choice == '2':
            fetch_ssd_data()
        elif choice == '3':
            print("Logging out.")
            break
        else:
            print("Invalid option. Please try again.")

def main():
    users = load_users_from_csv()
    
    print("Welcome to the NASA Space Data App!")
    
    while True:
        print("\n1. Login")
        print("2. Sign Up")
        print("3. Forgot Password")
        print("4. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            user_email = login_user(users)
            if user_email:
                logged_in_menu()  # After login, show the logged-in menu
        elif choice == '2':
            sign_up_user(users)
        elif choice == '3':
            reset_password(users)
        elif choice == '4':
            print("Exiting application.")
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()