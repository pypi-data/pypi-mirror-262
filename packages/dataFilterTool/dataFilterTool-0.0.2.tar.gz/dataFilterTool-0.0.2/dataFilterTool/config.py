import os #This module provides functions for interacting with the operating system, such as file operations and directory manipulation.
from datetime import datetime #provides classes for manipulating dates and times.
from configparser import ConfigParser #This module allows reading and writing configuration files in a standard format.

config = ConfigParser()
# instance of ConfigParser; read and write from ini file

def get_output_path(filename):
    output_directory = os.path.join(os.getcwd(), "output")
    output_path = os.path.join(output_directory, filename) #3
    return output_path

#input: filename output: returns a path to output directory with the filename argument
# os.path.join(): constructs path to the output directory by joining it the current working directory
#3 create a full path by joining output directory with filename


# def get_logs_path(filename, logs_directory=None):
#     if logs_directory is None:
#         #logs_directory = os.path.join(os.getcwd(), "logs")
#         logs_directory = os.path.join(os.path.expanduser("~"), "Desktop", "logs")
#     logs_path = os.path.join(logs_directory, filename)
#     return logs_path
def get_logs_path(filename, logs_directory=None):
    if logs_directory is None:
        # Read the logs directory path from config.ini in the dataFilterTool_config directory
        config_file_path = os.path.join(
            os.getcwd(), "dataFilterTool_config", "config.ini"
        )
        config.read(config_file_path)
        logs_directory = config.get(
            "Paths", "logs_directory", fallback="/home/user1/Desktop/external_logs"
        )
    logs_path = os.path.join(logs_directory, filename)
    return logs_path
# takes filename and logs_directory (optional) as parameter and returns log path
# reads the log directory path from ini file with cwd
#get() gets the log directory path from ini paths section
# if file not found then fall back is also provided
#
def get_timestamp(date_time):
    return date_time.strftime("%Y-%m-%d-%H-%M")
# returns a formatted string by taking date_time(object of datetime class) as parameter