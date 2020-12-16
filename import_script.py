from app import db, HappinessTable
from bs4 import BeautifulSoup
import requests

clean_suicide_data = []

def suicide_script():

    url = 'https://en.wikipedia.org/wiki/List_of_countries_by_suicide_rate'
    res = requests.get(url)
    soup = BeautifulSoup(res.text)

    table_rows = soup.findAll('tr')[27:210]

    for tr in table_rows:
        tds = tr.findAll('td')
        row = [string.text.strip() for string in tds]
        
        rank = int(row[0])
        country = row[1]
        if '(more info)' in country:
            country = country.replace('(more info)', "")
        if '[b]' in country:
            country = country.replace('[b]', '')

        clean_suicide_data.append([rank, country.strip()])
    
    return clean_suicide_data

suicide_script()


def happiness_script():

    url = 'https://en.wikipedia.org/wiki/World_Happiness_Report#2020_report'
    res = requests.get(url)
    soup = BeautifulSoup(res.text)

    clean_happiness_data = []

    table_rows = soup.findAll('tr')[11:164]

    for tr in table_rows:
        tds = tr.findAll('td')
        row = [string.text.strip() for string in tds]
        
        happiness_rank = int(row[0])
        country = row[1]

        suicide_rank = "N/A"
        for csd in clean_suicide_data:
            if csd[1] == country:
                suicide_rank = csd[0]

        gdp = float(row[3])
        life_expectancy = float(row[5])
        freedom = float(row[6])
        generosity = float(row[7])

        clean_happiness_data.append([suicide_rank, happiness_rank, country, gdp, life_expectancy, freedom, generosity])

    db.drop_all()
    db.create_all()

    for row in clean_happiness_data:
        new_row = HappinessTable(suicide_rank=row[0], happiness_rank=row[1], country=row[2], gdp=row[3], life_expectancy=row[4], freedom=row[5], generosity=row[6])
        db.session.add(new_row)
        db.session.commit()

if __name__ == "__main__":
    suicide_script()
    happiness_script()
