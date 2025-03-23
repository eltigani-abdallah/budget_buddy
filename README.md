# budget_buddy

The budget program that will make your finances Boom to riches!

# Boom_Budget

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/your-username/boom-budget.git
   ```
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Set up the MySQL database:
   - Create a new database named `boom_budget`.
   - Import the SQL schema from the `boom_budget.sql` file.
   - Update the database connection details in the `accounts.py` file.

## Usage

1. Run the login module:
   ```
   python accounts.py
   ```
2. The login window will appear. You can either sign up or log in.
3. After successful login, the main Finance Manager application will be launched.

## Contributing

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Implement your changes.
4. Test your changes.
5. Submit a pull request.

## Testing

The application does not have a dedicated testing suite. However, you can manually test the following scenarios:

1. User registration:
   - Verify that a new user can be registered with valid credentials.
   - Ensure that the password meets the security requirements.
   - Check that the user cannot register with an email that is already in use.
2. User login:
   - Verify that a registered user can log in with their correct credentials.
   - Ensure that the login fails with incorrect credentials.
3. Transactions:
   - Test the deposit, withdrawal, and transfer functionalities.
   - Verify that the transaction history is displayed correctly.
   - Check the search and filtering functionality.
4. Alerts and notifications:
   - Verify that the application correctly identifies and displays overdrawn accounts.
   - Test the "Check Alerts" functionality.
5. Language and theme switching:
   - Ensure that the application correctly updates the UI when changing the language or theme.
  
  ## Contributing

  Yuliia
  Eltigani
  Vanessa

  ## License

This project is licensed under the [MIT License](LICENSE).
