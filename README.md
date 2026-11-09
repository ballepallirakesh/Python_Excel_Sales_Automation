                                    Excel Sales Data Automation
About the Project:
        Managing sales data from multiple branches can become time-consuming, especially when each branch maintains its own Excel file. Combining the files, fixing inconsistent data, checking for errors, and preparing sales reports manually takes effort and can lead to mistakes.

        I built this Python automation project to simplify that process.

        It reads sales data from multiple Excel files, cleans and validates the records, separates invalid entries, calculates sales performance, and generates formatted Excel reports automatically.

        The goal was to create something practical that could help a small business reduce repetitive Excel work and get useful sales insights faster.

Features:
    Read multiple Excel files: Automatically finds and combines Excel files from the input folder.

    Clean sales data: Removes unnecessary spaces and standardizes text values such as product names, categories, and regions.

    Validate records: Checks for duplicate order IDs, missing customer names, invalid quantities, missing prices, and invalid dates.

    Separate rejected records: Keeps invalid records in a separate Excel file and records the reasons for rejection.

    Analyze sales: Calculates revenue and prepares category-wise, region-wise, product-wise, and monthly sales summaries.

    Generate Excel reports: Creates clean, organized Excel workbooks with formatted headers, filters, column widths, and frozen header rows.

    Logging and error handling: Records important steps and errors to help identify problems during execution.

    Automated testing: Uses pytest to check the main functionality and error-handling scenarios. 

Technologies Used:
            Python
            Pandas
            OpenPyXL
            pathlib
            Logging
            pytest

Project Structure: 
        python_automation_excel/
        │
        ├── input/
        │   ├── sales_january.xlsx
        │   ├── sales_february.xlsx
        │   └── sales_march.xlsx
        │
        ├── output/
        │   ├── cleaned_sales.xlsx
        │   ├── reject_records.xlsx
        │   └── sales_report.xlsx
        │
        ├── logs/
        │   └── automation.log
        │
        ├── src/
        │   ├── logger_config.py
        │   ├── excel_reader.py
        │   ├── data_cleaner.py
        │   ├── data_validator.py
        │   ├── sales_analyzer.py
        │   ├── report_generator.py
        │   └── main.py
        │
        ├── tests/
        │   ├── test_excel_reader.py
        │   ├── test_data_cleaner.py
        │   ├── test_data_validator.py
        │   ├── test_sales_analyzer.py
        │   └── test_report_generator.py
        │
        ├── create_sample_data.py
        ├── requirements.txt
        └── README.md   

Installation

1. Clone the repository
        git clone <your-github-repository-url>
        cd python_automation_excel

2. Create a virtual environment
        python -m venv venv

3. Activate the virtual environment
Windows:
        venv\Scripts\activate

4. Install the required packages
        pip install -r requirements.txt

Generate Sample Data:
The project includes a script to generate sample sales Excel files for testing.
 python create_sample_data.py
This creates three sample files inside the input/ folder, representing January, February, and March sales.
The sample data also includes a few intentional data-quality issues so that the cleaning and validation features can be tested.

Run the Automation:
From the project root directory, run:
python -m src.main
The automation reads the Excel files, processes the records, performs sales analysis, and generates the output reports.

Generated Reports:
After successful execution, three Excel files are created inside the output/ folder.
File                               Purpose
cleaned_sales.xlsx        Contains validated sales records
reject_records.xlsx       Contains rejected records and their rejection reasons
sales_report.xlsx         Contains category, region, product, and monthly sales summaries

Sample Results
Using the included sample data, the automation processed 30 sales records.
Metric                                       Result
Total records processed                       30
Valid records                                 25
Rejected records                               5
Total sales revenue                           ₹8,91,400

The sales analysis also showed that electronics contributed the largest share of revenue, while laptops were the highest-revenue product in the sample data.
These figures are based on the sample Excel files included with the project.

Run Automated Tests

I used pytest to test the individual modules and verify that the application handles both successful operations and common failure scenarios.

Run all tests using:
        pytest -v

Current test results:
        28 passed

The tests cover Excel file reading, data cleaning, validation, sales calculations, report generation, Excel formatting, and error handling.

Logging:
The application records execution details, warnings, and errors in:

logs/automation.log

This makes it easier to understand what happened during execution and troubleshoot issues.

What I Learned

While building this project, I got practical experience working with multiple Excel files, handling inconsistent data, using Pandas for data processing, generating formatted Excel reports, implementing logging and error handling, and writing automated tests with pytest.

Future Improvements:

Some features I would like to add in future versions include:

        Support for CSV files.
        Configurable validation rules.
        Custom date-range reports.
        Interactive sales dashboards.
        Scheduling automatic report generation.

Project focus: 
Python Automation | Excel Data Processing | Data Validation | Sales Reporting



