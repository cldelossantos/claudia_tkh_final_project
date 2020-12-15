from bs4 import BeautifulSoup
import requests
import sqlite3

conn = sqlite3.connect('happiness.db')
c = conn.cursor()

def create_or_update_database():
    url = 'https://en.wikipedia.org/wiki/World_Happiness_Report#2020_report'
    res = requests.get(url)
    soup = BeautifulSoup(res.text)
   
    table_rows = soup.findAll('tr')[11:164]

    for tr in table_rows:
        tds = tr.findAll('td')
        row = [string.text.strip() for string in tds]
       
        rank = int(row[0])
        country = row[1]
        life_expectancy = float(row[5])
        freedom = float(row[6])
        generosity = float(row[7])

        try:
            c.execute('''CREATE TABLE IF NOT EXISTS happiness 
            (rank INTEGER, country TEXT, life_expectancy REAL, freedom REAL, generosity REAL, UNIQUE(country))''')

            c.execute(f"INSERT INTO happiness VALUES ({rank}, '{country}', {life_expectancy}, {freedom}, {generosity})")
        except:
            continue
    
    # Save changes
    conn.commit()

    # Close connection
    conn.close()
    return "Successfully updated database!"
if __name__ == "__main__":
    create_or_update_database()