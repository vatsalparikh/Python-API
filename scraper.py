from bs4 import BeautifulSoup
import csv
import urllib
import pandas as pd

def holidays(holidayType=None, number=10):

    holidays_page = "https://www.timeanddate.com/holidays/us/"
    page = urllib.request.urlopen(holidays_page)
    soup = BeautifulSoup(page, "html.parser")
    table = soup.find("table", {"id": "holidays-table"})

    # parse current year for which data is displayed
    new_soup = soup.find("select", {"id": "year"})
    year = new_soup.find("option", selected=True)

    output_rows = []
    for table_row in table.find_all('tr'):
        columns = table_row.find_all(['td', 'th'])
        output_row = []
        for column in columns:
            output_row.append(column.text)
        output_rows.append(output_row)

    with open('holidays.csv', 'w', encoding='utf-8-sig') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(output_rows)

    df = pd.read_csv('holidays.csv')
    df = df.rename(columns={'\xa0': 'Day'})
    # convert 'Date' column string to datetime format
    df['Date'] = pd.to_datetime(df['Date'] + year.text, format='%b %d%Y', errors='coerce')
    # get today's date
    curr = pd.to_datetime('today')
    # filter rows by date and holiday type
    df = df.loc[df['Date'] > curr]
    if holidayType != None:
        df = df.loc[df['Type'] == holidayType]
    # convert 'Date' column back to string
    df['Date'] = df['Date'].dt.strftime('%A, %B %d, %Y')
    # drop day column from dataframe
    df = df.drop(columns='Day')
    # reorder columns in the order of expected output
    df = df.reindex(columns=['Name', 'Date', 'Type', 'Details'])
    return df[:number].to_dict('records')