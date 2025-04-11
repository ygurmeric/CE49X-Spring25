
def parse_construction_date(date_str):

    day, month, year = map(int, date_str.split('/'))
    is_leap = False
    if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
        is_leap = True
    return ((day, month, year), is_leap)

# Test data
test_dates = ["15/06/2024", "28/02/2023", "01/01/2020"]

# Test solution
for date in test_dates:
    result = parse_construction_date(date)
    print(f"Date: {date}")
    print(f"Parsed: {result[0]}")
    print(f"Is leap year: {result[1]}\n")
