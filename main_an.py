import pandas as pd
import numpy as np
from datetime import datetime
import sys
import os
from function_an import read_from_csv, save_to_csv, authenticate_user, register_user, get_closing_prices, analyze_closing_prices, check_date

# Clear the console
os.system('cls')

# File paths for user data and record data
user_file = r"C:\Users\ASUS VivoBook\OneDrive\Desktop\UUM\SEM 7 A241\SQIT 3073\Data\user_data.csv"
record_file = r"C:\Users\ASUS VivoBook\OneDrive\Desktop\UUM\SEM 7 A241\SQIT 3073\Data\record_data.csv"

# Load user and record data into DataFrames
df_user = pd.read_csv(user_file)
df_record = pd.read_csv(record_file)

# Extract email and password lists from user DataFrame, if columns exist
email = df_user['Email'].tolist() if 'Email' in df_user.columns else []
password = df_user['Password'].tolist() if 'Password' in df_user.columns else []

print("\n---- Stock Selection ----")
while True:
    # Loop to handle login attempts and menu navigation
    authenticate_user_result = authenticate_user(email, password)
    if authenticate_user_result[0]:  # If login is successful
        os.system('cls')
        email_in = authenticate_user_result[1]
        print(f"\nWelcome {email_in}!")
        current_time = datetime.now()  # Store current time for record

        while True:
            print("\n---- Check record or searching stock?(Please enter the number provided) ----")
            print("1. Check")  # Option to check records
            print("2. Search")  # Option to search stock data
            purpose_choice = input("Select the function:")
            if purpose_choice == "1":
                os.system('cls')
                print("\n---- Record ----\n")
                read_from_csv(record_file)  # Display the last 10 rows of record data
                continue
            if purpose_choice == "logout":
                sys.exit()  # Exit program if user logs out
            if purpose_choice == "2":
                os.system('cls')
                print("\n---- Stock data search (enter 'exit' to quit) ----")
                while True:
                    ticker = input("\nPlease enter the stock you want to search (In format nnnn): ")
                    if ticker == "logout":
                        sys.exit()  # Exit program if user logs out
                    if ticker == "exit":
                        break  # Exit stock search functionality
                    if len(ticker) == 4 and ticker.isdigit():  # Validate ticker format
                        ticker = ticker + ".KL"  # Append ".KL" for Malaysian stocks

                        # Get start date
                        while True:
                            os.system('cls')
                            print("\n---- Set the date range ----\n")
                            start_date = input("Please enter the start date (In format yyyymmdd): ")
                            if start_date == "logout":
                                sys.exit()
                            if start_date == "exit":
                                break
                            if check_date(start_date):  # Validate start date
                                start_date = datetime.strptime(start_date, "%Y%m%d")
                                start_date = start_date.strftime("%Y-%m-%d")
                                break
                            else:
                                print("The date format you entered in start date does not follow the format. Please enter the date in the correct format.")
                                continue

                        # Get end date
                        while True:
                            end_date = input("Please enter the end date (In format yyyymmdd): ")
                            if end_date == "logout":
                                sys.exit()
                            if end_date == "exit":
                                break
                            if check_date(end_date):  # Validate end date
                                end_date = datetime.strptime(end_date, "%Y%m%d")
                                end_date = end_date.strftime("%Y-%m-%d")
                                break
                            else:
                                print("The date format you entered in end date does not follow the format. Please enter the date in the correct format.")
                                continue

                        # Validate date range
                        while True:
                            if start_date >= end_date:
                                os.system('cls')
                                print("\nThe end date should be later than the start date")
                                break
                            else:
                                # Fetch and display stock data
                                data_to_analyze = get_closing_prices(ticker, start_date, end_date)
                                data_to_record = analyze_closing_prices(data_to_analyze)
                                print("\n")
                                print(data_to_record)

                                # Prepare data for saving
                                dict_result = {
                                    "Email": [email_in],
                                    "Time": [current_time]
                                }
                                # Convert dict_result to a DataFrame
                                df_result = pd.DataFrame(dict_result)

                                # Concatenate user and analysis data
                                final_data = pd.concat([df_result, data_to_record], axis=1)

                                # Save the data to the record file
                                save_to_csv(final_data, record_file)
                                
                                print("\nEnter 'logout' to logout")
                                print("Enter 'exit' to exit the function")
                                
                                break
                    else:
                        print("\nPlease enter the correct ticker. Ticker should have 4 characters.")
                        continue
            else:
                os.system('cls')
                print("Please enter a valid option")

    if not authenticate_user_result[0]:  # If login fails
        os.system('cls')
        print("Type '1' to register or '2' to try logging in again")
        register_choice = input("Select next step: ")
        if register_choice == '1':  # Register a new user
            register_result = register_user(email)
            if register_result[0]:
                email_in = register_result[1]
                password_in = register_result[2]

                # Append the new user to the lists
                email.append(email_in)
                password.append(password_in)

                # Save updated data to CSV after registration
                data_dict = {'Email': email, 'Password': password}
                df_new = pd.DataFrame(data_dict)
                df_new.insert(0, 'id', range(1, len(df_new) + 1))  # Add user ID column
                df_new.to_csv(user_file, index=False)
            else:
                os.system('cls')
                continue
        else:
            print("Retrying login...")
