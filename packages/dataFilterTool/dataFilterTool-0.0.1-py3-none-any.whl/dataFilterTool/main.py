# Importing the necessary functions from the scripts
# from join_date_filter import filter_by_date
# from avg_sal_des import average_salary_by_designation

# if __name__ == "__main__":
#     # Call the filter_by_date function
#     date_join_str = input("Enter the date (in the format YYYY-MM-DD) to filter employees: ")
#     generated_excel_file = filter_by_date(date_join_str)
#     if generated_excel_file:
#         print(f"Excel file generated: {generated_excel_file}")
#     else:
#         print("Failed to generate Excel file.")

#     # Call the average_salary_by_designation function
#     average_salary_by_designation()
# from dataFilterTool.filter_by_date import filter_by_date
# from dataFilterTool.avg_sal_by_des import average_salary_by_designation

# if __name__ == "__main__":
#     # Call the filter_by_date function
#     date_join_str = input("Enter the date (in the format YYYY-MM-DD) to filter employees: ")
#     generated_excel_file = filter_by_date(date_join_str)
#     if generated_excel_file:
#         print(f"Excel file generated: {generated_excel_file}")
#     else:
#         print("Failed to generate Excel file.")

#     # Call the average_salary_by_designation function
#     average_salary_by_designation()

# import os
# import sys

# # Add the parent directory to sys.path
# current_dir = os.path.dirname(os.path.abspath(__file__))
# parent_dir = os.path.abspath(os.path.join(current_dir, ".."))
# sys.path.insert(0, parent_dir)

# from dataFilterTool.join_date_filter import filter_by_date
# from dataFilterTool.avg_sal_des import average_salary_by_designation

# if __name__ == "__main__":
#     # Call the filter_by_date function
#     date_join_str = input(
#         "Enter the date (in the format YYYY-MM-DD) to filter employees: "
#     )
#     generated_excel_file = filter_by_date(date_join_str)
#     if generated_excel_file:
#         print(f"Excel file generated: {generated_excel_file}")
#     else:
#         print("Failed to generate Excel file.")

#     # Call the average_salary_by_designation function
#     average_salary_by_designation()

import os
import sys

# Add the parent directory to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.insert(0, parent_dir)

from dataFilterTool.join_date_filter import filter_by_date
from dataFilterTool.avg_sal_des import average_salary_by_designation


def main():
    # Call the filter_by_date function
    date_join_str = input(
        "Enter the date (in the format YYYY-MM-DD) to filter employees: "
    )
    generated_excel_file = filter_by_date(date_join_str)
    if generated_excel_file:
        print(f"Excel file generated: {generated_excel_file}")
    else:
        print("Failed to generate Excel file.")

    # Call the average_salary_by_designation function
    designation = input("Enter the designation:")
    average_salary_by_designation(designation)


if __name__ == "__main__":
    main()
