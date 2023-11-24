import requests
from bs4 import BeautifulSoup
from app import app
import models 


def hent_psykologer_fra_liste():
    psykologer = []
    base_url = "https://www.legelisten.no/psykologer/Oslo?side="

    for side in range(1,93):  # Iterer fra side 1 til 93
        url = f"{base_url}{side}"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        for tr in soup.find_all('tr', class_='search-result-row'):
            # Flyttet psykolog-objektet inn i loopen
            navn_element = tr.find('td', class_='name').find('span', class_='primary').find('a')
            navn = navn_element.get_text(strip=True)
            profil_url = navn_element['href']
            full_profil_url = f"https://www.legelisten.no{profil_url}"
            kjønn = tr.find('td', class_='name').find('span', class_='secondary').get_text(strip=True).split(',')[0]
            institusjonsnavn = tr.find('td', class_='practice').find('a').get_text(strip=True)
            adresse = tr.find('td', class_='practice').find('span', itemprop='streetAddress').get_text(strip=True)
            postal_code = tr.find('td', class_='area').find('span', itemprop='postalCode').get_text(strip=True)
            rating_element = tr.find('div', class_='stars-svg')['aria-label']
            rating = float(rating_element.split(' ')[0].replace(',', '.'))

            psykolog = {
                'navn': navn,
                'tittel': 'Psykolog',
                'kjønn': kjønn,
                'institusjonsnavn': institusjonsnavn,
                'adresse': adresse,
                'postal_code': postal_code,
                'by': 'Oslo',
                'legelistelink': full_profil_url,
                'rating': rating
            }

            if psykolog not in psykologer:
                psykologer.append(psykolog)

    return psykologer

def finn_eller_opprett_tjeneste_enheter():
    tjeneste_niva = TjenesteNiva.query.filter_by(navn="Førstelinjetjenesten").first()
    if not tjeneste_niva:
        tjeneste_niva = TjenesteNiva(navn="Førstelinjetjenesten")
        db.session.add(tjeneste_niva)
        db.session.commit()

    sektor = Sektor.query.filter_by(navn="Privat sektor").first()
    if not sektor:
        sektor = Sektor(navn="Privat sektor", tjeneste_niva_id=tjeneste_niva.id)
        db.session.add(sektor)
        db.session.commit()

    tjeneste_kategori = TjenesteKategori.query.filter_by(navn="Privat virksomhet").first()
    if not tjeneste_kategori:
        tjeneste_kategori = TjenesteKategori(navn="Privat virksomhet", sektor_id=sektor.id)
        db.session.add(tjeneste_kategori)
        db.session.commit()

    return tjeneste_kategori, sektor, tjeneste_niva

def hent_detaljer_fra_profil(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    telefonnummer = soup.find(itemprop="telephone").get_text(strip=True) if soup.find(itemprop="telephone") else None
    hjemmeside_elem = soup.find('span', itemprop="url")
    hjemmeside_link = hjemmeside_elem.find('a')['href'] if hjemmeside_elem and hjemmeside_elem.find('a') else None

    return telefonnummer, hjemmeside_link


def lagre_til_database(psykolog, tjeneste_kategori):
    with app.app_context():
        # Finn eller opprett HelseInstitusjon
        institusjon = HelseInstitusjon.query.filter_by(navn=psykolog['institusjonsnavn']).first()
        if not institusjon:
            institusjon = HelseInstitusjon(
                navn=psykolog['institusjonsnavn'],
                adresse=psykolog['adresse'],
                postal_code=psykolog['postal_code'],
                by=psykolog['by'],
                tjenestekategori_id=tjeneste_kategori.id
                # Merk: Telefonnummer og hjemmeside legges ikke her fordi det hører til HelsePersonell
            )
            db.session.add(institusjon)
        else:
            # Oppdater kun tomme felt for den eksisterende institusjonen
            if not institusjon.adresse and psykolog['adresse']:
                institusjon.adresse = psykolog['adresse']
            if not institusjon.postal_code and psykolog['postal_code']:
                institusjon.postal_code = psykolog['postal_code']
            if not institusjon.by and psykolog['by']:
                institusjon.by = psykolog['by']
            # Ikke oppdater tjenestekategori_id, antar at den forblir konstant

        db.session.commit()

        # Opprett eller oppdater HelsePersonell
        personell = HelsePersonell.query.filter_by(navn=psykolog['navn'], institusjon_id=institusjon.id).first()
        if not personell:
            personell = HelsePersonell(
                navn=psykolog['navn'],
                tittel='Psykolog',
                kjønn=psykolog['kjønn'],
                Legelistelink=psykolog['legelistelink'],
                institusjon_id=institusjon.id,
                telefonnummer=psykolog['telefonnummer'],
            
            )
            db.session.add(personell)
        else:
            # Oppdater kun tomme felt for den eksisterende personellen
            if not personell.telefonnummer and psykolog['telefonnummer']:
                personell.telefonnummer = psykolog['telefonnummer']
            # Ikke endre tittel og kjønn da disse sannsynligvis forblir konstante

        db.session.commit()

        # Opprett Anmeldelse og knytt den til HelsePersonell
        anmeldelse = Anmeldelse.query.filter_by(personell_id=personell.id).first()
        if not anmeldelse:
            anmeldelse = Anmeldelse(
                rating=psykolog['rating'],
                personell_id=personell.id
            )
            db.session.add(anmeldelse)
            db.session.commit()


if __name__ == "__main__":
    with app.app_context():
        tjeneste_kategori, sektor, tjeneste_niva = finn_eller_opprett_tjeneste_enheter()
        psykologer = hent_psykologer_fra_liste()
        for psykolog in psykologer:
            telefonnummer, hjemmeside = hent_detaljer_fra_profil(psykolog['legelistelink'])
            psykolog['telefonnummer'] = telefonnummer
            psykolog['hjemmeside'] = hjemmeside
            lagre_til_database(psykolog, tjeneste_kategori)