import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime
import sys
import os

# Function to read a CSV file and display its last 10 rows
def read_from_csv(filename):
    # Read the CSV file using pandas
    df = pd.read_csv(filename)
    # Display the last 10 rows of the dataframe
    print(df.tail(10))

# Function to save data to a CSV file, appending to the file if it already exists
def save_to_csv(data, filename):
    # Convert input data into a DataFrame
    new_df = pd.DataFrame(data)  # Assume `data` is a DataFrame or dictionary

    # Check if the file already exists
    if os.path.exists(filename):
        # Read the existing file
        existing_df = pd.read_csv(filename)
        # Concatenate the new data with the existing data
        combined_df = pd.concat([existing_df, new_df], ignore_index=False)
        # Save the updated DataFrame to the same file
        combined_df.to_csv(filename, index=False)
    else:
        # Save the new data as a new file
        new_df.to_csv(filename, index=False)

# Function to authenticate a user based on email and password
def authenticate_user(email, password):
    print("---- Login (enter '1' to register new account) ----\n")
    while True:
        # Prompt user for email
        print("Enter your email")
        email_in = input("Enter : ")
        if email_in == '1':  # Option to register
            print("To registration...")
            return False, None

        # Check if the entered email exists in the list of emails
        if email_in not in email:
            print("Email not found. Please check your email or register first.")
            continue

        # Prompt user for their password
        password_in = str(input("Please enter your password: "))
        e_password = str(password[email.index(email_in)])

        # Validate the entered password
        if e_password != password_in:
            print("Your password does not match your email. Please try again.")
            continue
        else:
            print("Login successful!")
            return True, email_in

# Function to validate email format
def validate_email(entry):
    # Check if the email contains "@" and ends with ".com"
    if "@" in entry and entry.endswith(".com"):
        return True
    return False

# Function to register a new user
def register_user(email):
    print("\n---- Register (enter 'exit' to quit) ----\n")
    while True:
        # Prompt user to enter their email
        email_in = input("Enter your email: ")
        if email_in == "exit":  # Exit option
            return False, None, None

        # Validate email format
        if not validate_email(email_in):
            print("Email in wrong format. Please try again.")
            continue 

        # Check if email already exists
        if email_in in email:
            print("Email already exists. Please choose a different email.")
            continue

        # Prompt user to enter their password
        password_in = str(input("Enter your password: "))
        if password_in == "exit":  # Exit option
            return False, None, None

        os.system('cls')  # Clear the console
        print("Enter again your password to check")
        password_check = str(input("Enter: "))
        if password_check == "exit":  # Exit option
            return False, None, None

        # Validate that both passwords match
        if password_in != password_check:
            print("The password is different, please enter again")
            continue
        else:
            os.system('cls')  # Clear the console
            print(f"\nUser '{email_in}' registered successfully!\n")
            return True, email_in, password_in

# Function to validate and parse a date entry
def check_date(date_entry):
    try:
        # Parse the date in the format "YYYYMMDD"
        date_object = datetime.strptime(date_entry, "%Y%m%d")
        return date_object
    except ValueError:  # Handle invalid date format
        return None

# Function to fetch and display closing stock prices
def get_closing_prices(ticker, start_date, end_date):
    stock_data = yf.Ticker(ticker)  # Fetch stock data
    stock_info = stock_data.info  # Retrieve stock information
    # Fetch historical stock data
    data = pd.DataFrame(stock_data.history(start=start_date, end=end_date))
    
    # Calculate the date range
    end_date = datetime.strptime(end_date, "%Y-%m-%d")
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    count_date = str(abs((end_date - start_date).days))

    os.system('cls')  # Clear the console
    print(f"\nDataset from {start_date} until {end_date}. Total is {count_date} days")
    print(f"Ticker name: {stock_info.get('shortName')} ({ticker})")
    print(f"Company name: {stock_info.get('longName')}\n")
    print(f"First 5 rows of the dataset for {stock_info.get('shortName')}:")
    print(data.head())  # Display the first 5 rows of the dataset
    return data

# Function to analyze closing stock prices
def analyze_closing_prices(data):
    df = pd.DataFrame(data)  # Convert data to DataFrame

    # Calculate the average closing price
    average_close = round(df["Close"].mean(), 3)

    # Calculate percentage change in closing prices
    df["Percentage change"] = df["Close"].pct_change() * 100
    percentage_change = round(df['Percentage change'].iloc[-1], 2)

    # Determine the highest and lowest closing prices
    highest_close = df["Close"].max()
    lowest_close = df["Close"].min()

    # Prepare the analysis results
    result = {
        'Average Closing Price': [average_close],
        'Percentage Change': [percentage_change],
        'Highest Closing Price': [highest_close],
        'Lowest Closing Price': [lowest_close]
    }

    result_df = pd.DataFrame(result)  # Convert results to DataFrame
    return result_df
