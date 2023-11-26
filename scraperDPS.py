import requests
from bs4 import BeautifulSoup

def scrape_dps_data(url):
    # Hent siden
    response = requests.get(url)
    response.raise_for_status()  # Sjekk for HTTP-feil

    # Parse HTML-innholdet
    soup = BeautifulSoup(response.content, 'html.parser')

    # Finn alle DPS-oppføringer
    dps_list = soup.find_all('li')

    # Samle DPS-navn, URL-er og helseforetak
    dps_data = []
    for dps in dps_list:
        text = dps.get_text()
        if ':' in text:
            name = text.split(":")[1].strip()
            link = dps.find('a')['href']
            helseforetak = get_helseforetak(link)
            dps_data.append((name, link, helseforetak))

    return dps_data

def get_helseforetak(url):
    # Hent siden
    response = requests.get(url)
    response.raise_for_status()  # Sjekk for HTTP-feil

    # Parse HTML-innholdet
    soup = BeautifulSoup(response.content, 'html.parser')

    # Finn tittelen som inneholder helseforetaket
    title = soup.find('title').get_text()

    # Hent ut helseforetaket fra tittelen
    helseforetak = title.split('-')[1].strip()

    return helseforetak

# URL til siden med DPS-informasjon
url = 'https://www.oslo.kommune.no/helse-og-omsorg/helsetjenester/psykisk-helsehjelp/distriktspsykiatrisk-senter-dps/'

# Kall funksjonen og skriv ut resultatene
for name, link, helseforetak in scrape_dps_data(url):
    print(f"{name}: {link} - {helseforetak}")




