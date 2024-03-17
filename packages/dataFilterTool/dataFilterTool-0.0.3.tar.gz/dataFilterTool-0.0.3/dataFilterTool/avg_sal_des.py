# import os
# import pandas as pd
# from dataFilterTool.config import get_output_path, get_logs_path
# from datetime import datetime
# import configparser


# def read_config():
#     config = configparser.ConfigParser()
#     config.read("config.ini")
#     return config

#  designation = input("Enter the designation: ")
# def is_designation_in_data(designation, employees):
#     """
#     Check if the entered designation exists in the employee data (case-insensitive).

#     Parameters:
#     - designation (str): The designation to check.
#     - employees (pd.DataFrame): DataFrame containing employee data.

#     Returns:
#     - bool: True if the designation is found, False otherwise.
#     """
#     # Convert both the user input and the data to lowercase for case-insensitive comparison
#     designation = designation.lower()
#     return not employees[employees["Designation"].str.lower() == designation].empty


# def average_salary_by_designation(designation):
#     # input_file = "/home/user1/Desktop/dataFilterTool/input/employee_data.xlsx"
#     directory = "/home/user1/Desktop/dataFilterTool/input/"
#     filename = "employee_data.xlsx"

#     # Combine the directory and filename to create a file path
#     input_file = os.path.join(directory, filename)

#     # Ensure that the output directory exists, if not create it
#     # if not os.path.exists(output_directory):
#     #     os.makedirs(output_directory)
#     output_directory = "/home/user1/Desktop/dataFilterTool/output"
#     op_filename = "average_salary_output.txt"
#     # Define the path for the output file
#     output_file = os.path.join(output_directory, op_filename)

#     # output_file = get_output_path("average_salary_output.txt")
#     log_file = get_logs_path("average_salary_logs.txt")
#     # log_file = get_logs_path("average_salary_logs.txt", logs_directory="/home/user1/Desktop/external_logs")
#     # Read the Excel file or query the database
#     employees = pd.read_excel(input_file, parse_dates=["Date_of_joining"])

#     # Prompt user for designation input
#     #designation = input("Enter the designation: ")

#     # Check if the entered designation is in the data (case-insensitive)
#     if not is_designation_in_data(designation, employees):
#         print(f"No employees found with the designation: {designation}")
#         return

#     # Convert the user input to lowercase for consistent formatting
#     designation = designation.lower()

#     # Filter employees based on the designation (case-insensitive)
#     filtered_employees = employees[employees["Designation"].str.lower() == designation]

#     # Calculate the average salary and round to 2 decimal places
#     average_salary = round(filtered_employees["Salary"].mean(), 2)

#     # Print and save the result to an output file
#     result = f"{datetime.now()}: Average Salary for {designation} is {average_salary}\n"
#     print(result)

#     with open(output_file, "a") as file:
#         file.write(result)

#     # Log the action
#     with open(log_file, "a") as log:
#         log.write(f"{datetime.now()}: Calculated average salary for {designation}\n")


# # Call the function to calculate average salary for the input designation
# # average_salary_by_designation()


# import os
# import pandas as pd
# from dataFilterTool.config import get_output_path, get_logs_path
# from datetime import datetime
# import configparser


# def read_config():
#     config = configparser.ConfigParser()
#     config.read("config.ini")
#     return config


# def is_designation_in_data(designation, employees):
#     """
#     Check if the entered designation exists in the employee data (case-insensitive).

#     Parameters:
#     - designation (str): The designation to check.
#     - employees (pd.DataFrame): DataFrame containing employee data.

#     Returns:
#     - bool: True if the designation is found, False otherwise.
#     """
#     # Convert both the user input and the data to lowercase for case-insensitive comparison
#     designation = designation.lower()
#     return not employees[employees["Designation"].str.lower() == designation].empty


# def average_salary_by_designation(designation):
#     # input_file = "/home/user1/Desktop/dataFilterTool/input/employee_data.xlsx"
#     directory = "/home/user1/Desktop/dataFilterTool/input/"
#     filename = "employee_data.xlsx"

#     # Combine the directory and filename to create a file path
#     input_file = os.path.join(directory, filename)

#     # Ensure that the output directory exists, if not create it
#     # if not os.path.exists(output_directory):
#     #     os.makedirs(output_directory)
#     output_directory = "/home/user1/Desktop/dataFilterTool/output"
#     op_filename = "average_salary_output.txt"
#     # Define the path for the output file
#     output_file = os.path.join(output_directory, op_filename)

#     # output_file = get_output_path("average_salary_output.txt")
#     log_file = get_logs_path("average_salary_logs.txt")
#     # log_file = get_logs_path("average_salary_logs.txt", logs_directory="/home/user1/Desktop/external_logs")
#     # Read the Excel file or query the database
#     employees = pd.read_excel(input_file, parse_dates=["Date_of_joining"])

#     # Prompt user for designation input
#     #designation = input("Enter the designation: ")

#     # Check if the entered designation is in the data (case-insensitive)
#     if not is_designation_in_data(designation, employees):
#         print(f"No employees found with the designation: {designation}")
#         return

#     # Convert the user input to lowercase for consistent formatting
#     designation = designation.lower()

#     # Filter employees based on the designation (case-insensitive)
#     filtered_employees = employees[employees["Designation"].str.lower() == designation]

#     # Calculate the average salary and round to 2 decimal places
#     average_salary = round(filtered_employees["Salary"].mean(), 2)

#     # Print and save the result to an output file
#     result = f"{datetime.now()}: Average Salary for {designation} is {average_salary}\n"
#     print(result)

#     with open(output_file, "a") as file:
#         file.write(result)

#     # Log the action
#     with open(log_file, "a") as log:
#         log.write(f"{datetime.now()}: Calculated average salary for {designation}\n")


import os
import pandas as pd
from dataFilterTool.config import get_output_path, get_logs_path
from datetime import datetime
import configparser

def read_config():
    config = configparser.ConfigParser()
    config.read("config.ini")
    return config

def is_designation_in_data(designation, employees):
    """
    Check if the entered designation exists in the employee data (case-insensitive).

    Parameters:
    - designation (str): The designation to check.
    - employees (pd.DataFrame): DataFrame containing employee data.

    Returns:
    - bool: True if the designation is found, False otherwise.
    """
    # Convert both the user input and the data to lowercase for case-insensitive comparison
    designation = designation.lower()
    return not employees[employees["Designation"].str.lower() == designation].empty

def average_salary_by_designation(designation):
    # input_file = "/home/user1/Desktop/dataFilterTool/input/employee_data.xlsx"
    directory = "/home/user1/Desktop/dataFilterTool/input/"
    filename = "employee_data.xlsx"

    # Combine the directory and filename to create a file path
    input_file = os.path.join(directory, filename)

    # Ensure that the output directory exists, if not create it
    output_directory = "/home/user1/Desktop/dataFilterTool/output"
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    op_filename = "average_salary_output.txt"
    # Define the path for the output file
    output_file = os.path.join(output_directory, op_filename)

    # Read the Excel file or query the database
    employees = pd.read_excel(input_file, parse_dates=["Date_of_joining"])

    # Check if the entered designation is in the data (case-insensitive)
    if not is_designation_in_data(designation, employees):
        print(f"No employees found with the designation: {designation}")
        return

    # Convert the user input to lowercase for consistent formatting
    designation = designation.lower()

    # Filter employees based on the designation (case-insensitive)
    filtered_employees = employees[employees["Designation"].str.lower() == designation]

    # Calculate the average salary and round to 2 decimal places
    average_salary = round(filtered_employees["Salary"].mean(), 2)

    # Print and save the result to an output file
    result = f"{datetime.now()}: Average Salary for {designation} is {average_salary}\n"
    print(result)

    with open(output_file, "a") as file:
        file.write(result)

    # Log the action
    log_file = get_logs_path("average_salary_logs.txt")
    with open(log_file, "a") as log:
        log.write(f"{datetime.now()}: Calculated average salary for {designation}\n")

    return average_salary
