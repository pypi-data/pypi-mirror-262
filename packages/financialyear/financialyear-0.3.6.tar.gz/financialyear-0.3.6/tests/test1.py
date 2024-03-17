from src

 # Example usage:
def test_fiancial_data():
    financial_year = Calculation("2023-24")
    print(financial_year.start_month(1))  # Output: 01-04-2023
    print(financial_year.end_month(1))    # Output: 30-04-2023
    print(financial_year.previous_month_dates(month=1))
    print(financial_year.month_list())    # Output: ['04-2023', '05-2023', '06-2023', ..., '03-2024']

if __name__ == '__main__':
    test_fiancial_data()