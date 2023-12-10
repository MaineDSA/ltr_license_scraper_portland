[![Pylint](https://github.com/MaineDSA/PortlandLTRData/actions/workflows/pylint.yml/badge.svg?branch=main)](https://github.com/MaineDSA/PortlandLTRData/actions/workflows/pylint.yml)

# Landlord License Data Downloader

This Python program allows you to download data about landlord licenses from the City of Portland website. It uses the `requests` library to send HTTP requests to the website's API and the `pandas` library to organize the data. It saves the results to a csv file.

## Data Downloaded

As written, the script downloads a list of all Long-Term Rental licenses issued since Jan 1 2022. It then looks up the details of each one, saving them as JSON data in the final column of the dataframe.

## Prerequisites

To run this code, you'll need to have Python 3.9, 3.10, or 3.11 installed on your machine. You'll also need to install the required packages by running the following command from inside the project folder:

```shell
python3 -m pip install -r requirements.txt
```

## Usage

1. Clone the repository and navigate to the project folder.
2. Open a terminal and run the following command to create a CSV of licenses:

```shell
python3 -m license_downloader
```

## Notes
The code contains two variables for easy testing and adjustment for usecase:

- `TESTMODE`: Set this to `True` if you want to test the program with small number of licenses (1 page of 20 licenses -- only iterating through Multi Family licenses). Set it to `False` if you want to download all Long Term Rental licenses.

- `PAGESIZE`: Set this to the desired number of licenses per page