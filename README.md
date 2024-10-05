
# NASA Data Console Application

## Overview
The **NASA Data Console** is a Python-based console application that allows users to access NASA's space-related data. The application provides a secure login system, user registration, and password reset functionality. Once logged in, users can fetch data from two NASA APIs:
- **Near Earth Object (NEO) Feed**: Fetch data on asteroids and near-Earth objects.
- **Solar System Dynamics (SSD)**: Retrieve information about solar system objects like planets, moons, comets, and asteroids.

## Features
- **Login System**: Users need to log in to access the data. Credentials are stored securely in a CSV file with password hashing.
- **User Registration**: New users can sign up by entering their email, password, and a security question.
- **Password Reset**: Users can reset their password by answering a security question.
- **NASA API Integration**: Retrieve and display NEO and SSD data from NASA APIs in a table format.
- **Error Handling**: Gracefully handles invalid credentials, API issues, and connection errors.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/nasa-data-console.git
    cd nasa-data-console
    ```

2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Run the application:
    ```bash
    python main.py
    ```

## Demo

### 1. **Login, Sign-up, and Password Reset**
When the application starts, the user is prompted with options to **Login**, **Sign-up**, or **Reset Password**.

#### **Sign-up:**
```bash
Enter your email: user@example.com
Enter your password: *********
Enter a security question: What is your favorite planet?
Enter the answer to your security question: Mars
Sign-up successful!
```

#### **Login:**
```bash
Enter your email: user@example.com
Enter your password: *********
Login successful!
```

### 2. **Fetching Near Earth Object (NEO) Data**
After a successful login, users can fetch NEO data from NASA’s API. The data is displayed in a neatly formatted table.

#### **Example NEO Data:**
```bash
Logged In - Select an option:
1. Fetch NEO Data
2. Fetch SSD Data
3. Exit
Choose an option: 1

Near-Earth Objects (NEO) Data:
+------------------+----------------------+------------------------+------------------+------------------+-------------+
| Name             | Close Approach Date   | Estimated Diameter (m)  | Velocity (km/h)  | Miss Distance (km) | Hazardous   |
+------------------+----------------------+------------------------+------------------+------------------+-------------+
| 2021 SM3         | 2024-10-01            | 160.23                 | 37000            | 7840000           | False       |
| 2010 NY65        | 2024-10-01            | 134.87                 | 45432            | 5840000           | True        |
+------------------+----------------------+------------------------+------------------+------------------+-------------+
```

### 3. **Fetching Solar System Dynamics (SSD) Data**
The application also retrieves data about solar system objects (e.g., planets, asteroids, comets).

#### **Example SSD Data:**
```bash
Logged In - Select an option:
1. Fetch NEO Data
2. Fetch SSD Data
3. Exit
Choose an option: 2

Solar System Object Data (Ceres):
+------------------+----------------------------------+
| Parameter        | Value                            |
+------------------+----------------------------------+
| Name             | 1 Ceres                          |
| Object Type      | 2000001                          |
| Discovery Date   | 1801-01-01                       |
| Semi-major Axis  | 2.77 AU                          |
| Eccentricity     | 0.079                            |
| Inclination      | 10.6 degrees                     |
| Diameter         | 939.4 km                         |
+------------------+----------------------------------+
```

### 4. **Password Reset**
If a user forgets their password, they can reset it by providing the correct answer to their security question.

#### **Password Reset:**
```bash
Enter your registered email for password reset: user@example.com
Security Question: What is your favorite planet?
Answer: Mars
Enter new password: *********
Password reset successfully!
```

## Error Handling
The app includes various error-handling mechanisms:
- Invalid credentials trigger error messages.
- Failed API requests (due to network issues or invalid API keys) are caught and reported.
  
```bash
Error fetching NEO data: RequestException: 401 Unauthorized (Invalid API Key)
```

## Technologies Used
- **Python**
- **CSV for user data storage**
- **bcrypt for password hashing**
- **tabulate for table formatting**
- **NASA NEO & SSD APIs**

## Contributing
If you'd like to contribute to this project, feel free to submit a pull request or open an issue.

## License
This project is licensed under the MIT License.
