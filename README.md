# Vendor Assignment Automation

## Overview

This software is designed to automate the monitoring and updating of vendor assignments for product units within a corporate SQL database. The program performs the following key functions:

1.  **Monitoring**: Continuously monitors an internal SQL database for flags indicating units with new vendor assignments.
2.  **Data Retrieval**: Extracts the "parent case ID" for the unit and communicates with a third-party API using the SOAP protocol to retrieve the corresponding "child case ID" for the newly assigned vendor.
3.  **Data Processing and Updating**: Processes the XML data received from the third-party API and updates the SQL database accordingly.

This system ensures that the database remains up-to-date with the latest vendor assignments, streamlining the data management process and enhancing operational efficiency.

## Technologies Used

- **Python**: The primary programming language used for this project.
- **Object-Oriented Programming (OOP)**: Emphasizes the use of classes and objects to create modular and reusable code.
- **Asynchronous Programming**: Utilized for handling I/O-bound operations efficiently.
- **Data Classes**: Used for creating classes that primarily store data with minimal boilerplate code.
- **Exception Handling**: Implemented to manage errors and ensure the robustness of the application.
- **Logging**: For tracking and debugging the process.
- **SQL**: For database interactions and queries.
- **SOAP**: For communication with the third-party API.
- **XML Parsing**: For processing the data format received from the API.
- **Dependency Management**: Managed using `pip` and `requirements.txt`.

## Features

- Automated monitoring of vendor assignments.
- Integration with third-party APIs using SOAP.
- XML data processing and conversion.
- Asynchronous operations for efficient data handling.
- Robust error handling and logging.

## Project Structure

The project is organized into the following files:

- `config.py`: Configuration settings and constants.
- `connect_sql.py`: Functions for connecting to the SQL database.
- `defusedexpat.py`: A defused version of the `pyexpat` and `_elementtree` modules.
- `exceptions.py`: Custom exception classes.
- `handlers.py`: Handlers for SQL and XML operations.
- `holders.py`: Data holder classes using `dataclasses`.
- `interfaces.py`: Abstract base classes for various operations.
- `interval_timer.py`: Utility for setting intervals.
- `loggers.py`: Logging classes.
- `main.py`: Main script to run the project.
- `notify.py`: Functions for sending notifications via email.
- `operations.py`: Classes for executing SQL and SOAP operations.
- `processors.py`: Data processing classes.
- `traceback_logger.py`: Utility for logging tracebacks.
- `utilities.py`: Utility functions.
- `xmltodict.py`: Module for converting XML to dictionary.
- `__init__.py`: Initialization file for the package.

## Prerequisites

- Python 3.7 or higher
- Access to a corporate SQL database
- SendGrid API key for email notifications

## Getting Started

1.  Clone the repository:
    
        git clone https://github.com/ryanlevee/vendor-assignment-automation.git
    
2.  Navigate to the project directory:
    
        cd vendor-assignment-automation
    
3.  Install the dependencies:
    
        pip install -r requirements.txt

## Usage

To run the main script, use:

    python src/main.py

## Usage Example

Here's a brief example of how the software works:

1.  The program monitors the SQL database for units with new vendor assignments.
2.  When a new assignment is detected, it retrieves the parent case ID tied to the unit.
3.  The parent case ID is sent to the third-party API to get the corresponding child case ID tied to the newly assigned vendor.
4.  The XML data received from the API is processed and the SQL database is updated.

## Modules

#### `config.py`

Contains configuration settings and constants used throughout the project.

#### `connect_sql.py`

Provides functions to connect to the SQL database and execute queries.

#### `defusedexpat.py`

A defused version of the `pyexpat` and `_elementtree` modules to prevent XML vulnerabilities.

#### `exceptions.py`

Defines custom exceptions used in the project.

#### `handlers.py`

Contains handler classes for SQL and XML operations.

#### `holders.py`

Defines data holder classes using `dataclasses` to store and manage data.

#### `interfaces.py`

Abstract base classes for various operations, ensuring a consistent interface.

#### `interval_timer.py`

Utility for setting intervals to repeatedly execute functions.

#### `loggers.py`

Logging classes to log debug, info, and error messages.

#### `main.py`

The main script that orchestrates the execution of the project.

#### `notify.py`

Functions for sending email notifications using SendGrid.

#### `operations.py`

Classes for executing SQL and SOAP operations.

#### `processors.py`

Data processing classes to normalize and process XML and SQL data.

#### `traceback_logger.py`

Utility for logging tracebacks and sending notifications on errors.

#### `utilities.py`

Utility functions for various tasks such as list manipulation and SQL string creation.

#### `xmltodict.py`

Module for converting XML data to a dictionary format.

Contributing
------------

Contributions are welcome! Please open an issue or submit a pull request.

Credits
-------

This project includes code from the following repositories:

*   `xmltodict.py`: xmltodict by Martin Blech, licensed under the MIT License.
*   `defusedexpat.py`: defusedexpat by Christian Heimes, licensed under the PSF License.

Author
------

Ryan Levee

License
-------

This project is licensed under the MIT License. See the `LICENSE` file for details.

