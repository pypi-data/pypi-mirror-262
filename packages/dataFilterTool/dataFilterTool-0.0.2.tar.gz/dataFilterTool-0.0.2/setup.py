# import setuptools
# from dataFilterTool.version import __version__

# with open("README.md", "r") as f:
#     description = f.read()
# setuptools.setup(
#     name="dataFilterTool",
#     version="0.0.2",
#     author="Lavanya",
#     author_email="lavanya.narang@dataverze.ai",
#     description="""
#         DataFilterTool is a Python package designed to 
#         facilitate filtering and analyzing employee data. It offers 
#         functionality to filter employees based on their date of joining 
#         and to calculate the average salary for a given designation. This 
#         package is suitable for use in various data analysis and human resources applications.
#     """,
#     packages=setuptools.find_packages(),
#     classifiers=[
#         "Programming Language :: Python :: 3",
#         "License :: OSI Approved :: MIT License",
#         "Operating System :: OS Independent",
#     ],
#     include_package_data=True,
#     package_data={"dataFilterTool": ["employee_data.xlsx"]},
#     install_requires=[
#         "pytest",
#         "pylance",
#         "pip",
#         "python",
#     ],
#     python_requires=">=3.7",
#     long_description=description,
#     long_description_content_type="text/markdown",
# )


import setuptools


with open("README.md", "r") as f:
    description = f.read()

setuptools.setup(
    name="dataFilterTool",
    version="0.0.2",
    author="Lavanya",
    author_email="lavanya.narang@dataverze.ai",
    description="""
        DataFilterTool is a Python package designed to 
        facilitate filtering and analyzing employee data. It offers 
        functionality to filter employees based on their date of joining 
        and to calculate the average salary for a given designation. This 
        package is suitable for use in various data analysis and human resources applications.
    """,
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
    package_data={"dataFilterTool": ["employee_data.xlsx"]},
    install_requires=[
        "pytest",
        "pylance",
    ],
    python_requires=">=3.7",
    long_description=description,
    long_description_content_type="text/markdown",
)
