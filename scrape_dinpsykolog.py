import requests
from bs4 import BeautifulSoup
from models import TjenesteTilbudProblemområde, TjenesteTilbudBehandlingsmetodikk, TjenesteTilbudFormat, Problemområde, Behandlingsmetodikk, Format, TjenesteTilbud, Anmeldelse, HelsePersonell, HelseInstitusjon, TjenesteKategori, Sektor, TjenesteNiva, db
from app import app

# Anta at antall_sider er kjent eller bestemt på forhånd
antall_sider = 29  # Eksempel, endre dette etter behov

def hent_psykologer_fra_dinpsykolog():
    psykologer = []
    base_url = "https://dinpsykolog.no/?page={}&username=&village=oslo&gender=&age="

    for side in range(1, antall_sider + 1):
        url = base_url.format(side)
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        for div in soup.find_all('div', class_='list_item'):
            navn = div.find('h4').get_text(strip=True)
            profilbilde_url = div.find('div', class_='list_img').find('img')['src']
            full_profilbilde_url = f"https://dinpsykolog.no{profilbilde_url}"
            profil_url = div.find('a', class_='link_btn')['href']
            full_profil_url = f"https://dinpsykolog.no{profil_url}"

            # Last ned bildet
            bilde_response = requests.get(full_profilbilde_url)
            profilbilde_data = bilde_response.content if bilde_response.status_code == 200 else None

            psykolog = {
                'navn': navn,
                'profilbilde_data': profilbilde_data,  # Lagrer det binære innholdet av bildet
                'dinpsykologlink': full_profil_url
            }
            psykologer.append(psykolog)

    return psykologer

def finn_eller_opprett_tjeneste_niva(navn):
    tjeneste_niva = TjenesteNiva.query.filter_by(navn=navn).first()
    if not tjeneste_niva:
        tjeneste_niva = TjenesteNiva(navn=navn)
        db.session.add(tjeneste_niva)
        db.session.commit()

    return tjeneste_niva.id

def finn_eller_opprett_sektor(navn, tjeneste_niva_id):
    sektor = Sektor.query.filter_by(navn=navn).first()
    if not sektor:
        sektor = Sektor(navn=navn, tjeneste_niva_id=tjeneste_niva_id)
        db.session.add(sektor)
        db.session.commit()

    return sektor.id

def finn_eller_opprett_tjeneste_kategori(navn, sektor_id):
    tjeneste_kategori = TjenesteKategori.query.filter_by(navn=navn).first()
    if not tjeneste_kategori:
        tjeneste_kategori = TjenesteKategori(navn=navn, sektor_id=sektor_id)
        db.session.add(tjeneste_kategori)
        db.session.commit()

    return tjeneste_kategori.id

def finn_eller_opprett_institusjon(psykolog_navn):
    institusjon_navn = f"Psykolog {psykolog_navn}"
    tjeneste_niva_id = finn_eller_opprett_tjeneste_niva("Førstelinjetjenesten")
    sektor_id = finn_eller_opprett_sektor("Privat sektor", tjeneste_niva_id)
    tjeneste_kategori_id = finn_eller_opprett_tjeneste_kategori("Privat virksomhet", sektor_id)

    institusjon = HelseInstitusjon.query.filter_by(navn=institusjon_navn).first()

    if not institusjon:
        institusjon = HelseInstitusjon(
            navn=institusjon_navn,
            tjenestekategori_id=tjeneste_kategori_id
        )
        db.session.add(institusjon)
        db.session.commit()

    return institusjon.id


def hent_detaljer_fra_profil(url, navn, profilbilde_data):
    with app.app_context():
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Fødselsår
        bornyear_select = soup.find('select', id='bornyear')
        fødselsår_option = bornyear_select.find('option', selected=True) if bornyear_select else None
        fødselsår = fødselsår_option['value'] if fødselsår_option else None

        # Telefonnummer
        telefonnummer_input = soup.find('input', attrs={'name': 'phonenumber'})
        telefonnummer = telefonnummer_input['value'] if telefonnummer_input else None

        # E-post
        email_input = soup.find('input', attrs={'name': 'emailaddress'})
        epost = email_input['value'] if email_input else None

        # Klinikkadresse
        address_input = soup.find('input', attrs={'name': 'address'})
        adresse = address_input['value'] if address_input else None

        # Postnummer på klinikk
        by_input = soup.find('input', attrs={'name': 'by'})
        by_value = by_input['value'] if by_input and by_input.get('value') else ""
        postal_code = by_value.split()[0] if by_value.split() else None

        # Informasjon om psykologen
        content_textarea = soup.find('textarea', attrs={'name': 'bodycontent'})
        selvrapport = content_textarea.get_text() if content_textarea else None

        # Hent problemområder
        problemområde_labels = {
            '1101': 'Angst',
            '1102': 'Stress',
            '1103': 'Utbrenthet',
            '1104': 'Uro',
            '1105': 'Depresjon',
            '1106': 'Selvfølelse',
            '1107': 'Avhengighet',
            '1108': 'Spiseforstyrrelser',
            '1109': 'Kroppslige plager',
            '1115': 'Lærevansker',
            '1116': 'Emosjonelle problemer',
            '1117': 'ADHD',
            '1118': 'Atferdsproblemer'
        }
        problemområder = []
        for value, label in problemområde_labels.items():
            if soup.find('input', {'type': 'checkbox', 'value': value, 'checked': True}):
                problemområder.append(label)
        # Logge identifiserte problemområder
        if problemområder:
            print(f"Identifiserte problemområder for {navn}: {', '.join(problemområder)}")
        else:
            print(f"Ingen problemområder funnet for {navn}")

        eksisterende_psykolog = HelsePersonell.query.filter_by(navn=navn).first()
        if eksisterende_psykolog:
            # Oppdater kun tomme felt for den eksisterende psykologen
            if not eksisterende_psykolog.fødselsår and fødselsår:
                eksisterende_psykolog.fødselsår = fødselsår
            if not eksisterende_psykolog.profilbilde:
                eksisterende_psykolog.profilbilde = profilbilde_data  
            if not eksisterende_psykolog.telefonnummer and telefonnummer:
                eksisterende_psykolog.telefonnummer = telefonnummer
            if not eksisterende_psykolog.epost and epost:
                eksisterende_psykolog.epost = epost
            if not eksisterende_psykolog.Selvrapport and selvrapport:
                eksisterende_psykolog.Selvrapport = selvrapport
            # ... [Gjenta for andre felt etter behov]

            db.session.commit()
            helse_personell_id = eksisterende_psykolog.id
        else:
            # Finn eller opprett en institusjon for psykologen
            institusjon_id = finn_eller_opprett_institusjon(navn)
            # Oppretter ny HelsePersonell-instans
            ny_helse_personell = HelsePersonell(
                navn=navn,
                profilbilde=profilbilde_data,
                fødselsår=fødselsår,
                telefonnummer=telefonnummer,
                epost=epost,
                Selvrapport=selvrapport,
                institusjon_id=institusjon_id
            )
            db.session.add(ny_helse_personell)
            db.session.commit()
            helse_personell_id = ny_helse_personell.id

        # Koble problemområder til HelsePersonell
        for problem in problemområder:
            problemområde = Problemområde.query.filter_by(navn=problem).first()
            if not problemområde:
                problemområde = Problemområde(navn=problem)
                db.session.add(problemområde)
                db.session.flush()  # For å få ID til et nytt problemområde

            # Sjekk om koblingen allerede eksisterer
            eksisterende_kobling = TjenesteTilbudProblemområde.query.filter_by(tjenestetilbud_id=helse_personell_id, problemområde_id=problemområde.id).first()
            if not eksisterende_kobling:
                ny_kobling = TjenesteTilbudProblemområde(tjenestetilbud_id=helse_personell_id, problemområde_id=problemområde.id)
                db.session.add(ny_kobling)

        db.session.commit()

        return helse_personell_id

        




def main():
    psykologer = hent_psykologer_fra_dinpsykolog()
    for psykolog in psykologer:
        detaljer_id = hent_detaljer_fra_profil(psykolog['dinpsykologlink'], psykolog['navn'], psykolog['profilbilde_data'])
        print(f"Hentet detaljer for psykolog med ID: {detaljer_id}")

if __name__ == "__main__":
    main()

