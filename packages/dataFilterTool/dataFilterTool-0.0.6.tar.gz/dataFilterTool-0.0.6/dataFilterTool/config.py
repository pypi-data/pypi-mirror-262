# import os  # This module provides functions for interacting with the operating system, such as file operations and directory manipulation.
# from datetime import datetime  # provides classes for manipulating dates and times.
# from configparser import (
#     ConfigParser,
# )  # This module allows reading and writing configuration files in a standard format.

# config = ConfigParser()
# # instance of ConfigParser; read and write from ini file

# def get_output_path(filename):
#     config_file_path = os.path.join(os.getcwd(), "dataFilterTool_config", "config.ini")
#     config.read(config_file_path)
#     output_directory = config.get("Paths", "output_directory", fallback="/home/user1/Desktop/external_output")
#     output_path = os.path.join(output_directory, filename)
#     return output_path

# # input: filename output: returns a path to output directory with the filename argument
# # os.path.join(): constructs path to the output directory by joining it the current working directory


# # def get_logs_path(filename, logs_directory=None):
# #     if logs_directory is None:
# #         #logs_directory = os.path.join(os.getcwd(), "logs")
# #         logs_directory = os.path.join(os.path.expanduser("~"), "Desktop", "logs")
# #     logs_path = os.path.join(logs_directory, filename)
# #     return logs_path
# def get_logs_path(filename, logs_directory=None):
#     if logs_directory is None:
#         # Read the logs directory path from config.ini in the dataFilterTool_config directory
#         config_file_path = os.path.join(
#             os.getcwd(), "dataFilterTool_config", "config.ini"
#         )
#         config.read(config_file_path)
#         logs_directory = config.get(
#             "Paths", "logs_directory", fallback="/home/user1/Desktop/external_logs"
#         )
#     logs_path = os.path.join(logs_directory, filename)
#     return logs_path


# # takes filename and logs_directory (optional) as parameter and returns log path
# # reads the log directory path from ini file with cwd
# # get() gets the log directory path from ini paths section
# # if file not found then fall back is also provided
# #
# def get_timestamp(date_time):
#     return date_time.strftime("%Y-%m-%d-%H-%M")


# returns a formatted string by taking date_time(object of datetime class) as parameter
import os
from configparser import ConfigParser

config = ConfigParser()

def get_output_path(filename):
    config_file_path = os.path.join(os.getcwd(), "dataFilterTool_config", "config.ini")
    config.read(config_file_path)
    output_directory = config.get("Paths", "output_directory", fallback="/home/user1/output")
    output_path = os.path.join(output_directory, filename)
    ensure_directory(output_directory)  # Create the output directory if it doesn't exist
    return output_path

def ensure_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def get_logs_path(filename, logs_directory=None):
    if logs_directory is None:
        config_file_path = os.path.join(os.getcwd(), "dataFilterTool_config", "config.ini")
        config.read(config_file_path)
        logs_directory = config.get("Paths", "logs_directory", fallback="/home/user1/Desktop/external_logs")
    logs_path = os.path.join(logs_directory, filename)
    return logs_path

def get_timestamp(date_time):
    return date_time.strftime("%Y-%m-%d-%H-%M")
