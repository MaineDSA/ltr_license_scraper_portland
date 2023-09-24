# Landlord License Data Downloader

This Python program allows you to download data about landlord licenses from the City of Portland website. It uses the `requests` library to send HTTP requests to the website's API and the `pandas` library to organize the data. It saves the results to a csv file.

## Prerequisites

To run this program, you need to have Python 3 installed on your computer. You can download and install Python 3 from the official Python website: [https://www.python.org](https://www.python.org)

You also need to install the following Python libraries:

- `requests`
- `pandas`

You can install these libraries using `pip` by running the following command in your terminal or command prompt:

```
pip install requests pandas
```

## Usage

1. Download the Python script provided and save it to a directory on your computer.

2. Open the script in a text editor and modify the following variables if needed:

   - `TESTMODE`: Set this to `True` if you want to test the program with a smaller number of licenses (20 licenses per license type) and only iterating through a Multi Family licenses. Set it to `False` if you want to download all licenses (200 licenses per license type).

   - `PAGESIZE`: Set this to the desired number of licenses per page
