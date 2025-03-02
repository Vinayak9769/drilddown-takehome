# Drilldown

This project is a Take home assignment for Drilldown. It processes and analyzes sales data, converting user queries into SQL statements and generating PDF reports.

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/Vinayak9769/drilddown-takehome
   cd drilddown-takehome
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Ensure the `data/` and `utils/` folders are present.

4. Run the project:
   ```bash
   python main.py --argument
   ```

## Project Structure

- **`main.py`**: Entry point that chains text-to-SQL conversion, SQL execution, and PDF generation.
- **`chains/`**: Contains logic for transforming user input into queries, executing those queries, and generating reports.
- **`utils/`**: Houses helper scripts for loading data, parsing JSON, etc.
- **`data/`**: Contains JSON and CSV files used for processing and analysis.

## Usage

1. Update the query string in `main.py` to change the search question.
2. The final PDF report is saved as `sales_report_landscape.pdf`.



