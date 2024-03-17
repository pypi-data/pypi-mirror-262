import os
import pandas as pd
from dataFilterTool.config import get_output_path, get_logs_path, get_timestamp
from datetime import datetime
import configparser
import xlsxwriter


def read_config():
    config = configparser.ConfigParser()
    config.read("config.ini")
    return config
    # Initializes a ConfigParser object and reads the configuration file config.ini.
    # Returns the ConfigParser object.

def filter_by_date(date_str):
    try:
        # Convert the user input date to a Pandas datetime object
        user_date = pd.to_datetime(date_str)

        # Get today's date
        today_date = pd.to_datetime(datetime.now().strftime("%Y-%m-%d"))

        # Check if the user date is between "2022-07-13" and today's date
        if pd.to_datetime("2022-07-13") <= user_date <= today_date:
            print(f"The date {date_str} is within the desired range.")
        else:
            print(f"The date {date_str} is outside the desired range.")
            return None  # Exit the function if the date is outside the desired range

        # Convert user_date to datetime for further processing
        date_join = pd.to_datetime(date_str)

        # Assuming 'scripts/generate_sample_data.py' is in the same directory as the script
        directory = "/home/user1/Desktop/dataFilterTool/input/"
        filename = "employee_data.xlsx"

        # Combine the directory and filename to create a file path
        input_file = os.path.join(directory, filename)

        # Read data from Excel file and parse 'Date_of_joining' column as datetime
        employees = pd.read_excel(input_file, parse_dates=["Date_of_joining"])

        # Filter employees based on date
        filtered_employees = employees[employees["Date_of_joining"] > date_join].copy()

        # Include the formatted date in the output filename
        output_filename = f"filtered_output_{get_timestamp(date_join)}.xlsx"
        output_path = get_output_path(output_filename)

        log_filename = f"filtered_logs_{get_timestamp(date_join)}.txt"
        log_path = get_logs_path(log_filename)

        # Create ExcelWriter object with xlsxwriter engine and set date format
        with pd.ExcelWriter(output_path, engine="xlsxwriter") as writer:
            filtered_employees.to_excel(writer, index=False, sheet_name="Filtered Data")

            # Get the xlsxwriter workbook and worksheet objects
            workbook = writer.book
            worksheet = writer.sheets["Filtered Data"]

            # Add date format to the cells containing dates
            date_format = workbook.add_format({"num_format": "yyyy-mm-dd"})
            worksheet.set_column("A:A", None, date_format)

        # Write log
        with open(log_path, "w") as log:
            log.write(
                f"{get_timestamp(date_join)}: filtered employees after {date_join}\n"
            )

        return output_path  # Return the path of the generated Excel file

    except ValueError:
        print(
            "Invalid date format. Please enter a valid date in the format YYYY-MM-DD."
        )
    except FileNotFoundError:
        print(f"Input file not found: {input_file}")
        return None
