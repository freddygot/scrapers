import requests
from datetime import datetime
from bs4 import BeautifulSoup
from flask import Flask
from app import app, db  # Importer 'app' og 'db' fra din Flask-applikasjonsmodul
from app import PrivateClinic, Psychologist, Review # Importer modellene
import locale
locale.setlocale(locale.LC_TIME, 'no_NO')

def get_profile_info(soup):
    profile_info = soup.find("div", class_="profile-image profile-image-mobile person").find_next_sibling("div")
    if profile_info:
        # Anta at teksten etter <br> er i formatet "Kjønn, Alder år"
        profile_text = profile_info.get_text(separator="|").split("|")[1].split(", ")
        if len(profile_text) == 2:
            gender = profile_text[0]
            age = profile_text[1].split()[0]
        else:
            gender = "Ukjent"
            age = "Ukjent"
    else:
        gender = "Ukjent"
        age = "Ukjent"
    return gender, age


def parse_date(date_str):
    # Fjerner overflødige hvite tegn
    date_str = date_str.strip()
    return datetime.strptime(date_str, "%d. %B %Y")  # Juster formatet etter behov




def scrape_reviews(soup, psychologist_id):
    reviews = soup.find_all("section", itemprop="review")
    for review in reviews:
        review_title = review.find("h3").text
        review_date_str = review.find("time", itemprop="dateCreated").text
        review_rating = float(review.find("span", class_="rating").text)
        review_body = review.find("div", itemprop="reviewBody").text

        review_date = parse_date(review_date_str)

        # Sjekk om anmeldelsen allerede er lagret
        existing_review = Review.query.filter_by(
            psychologist_id=psychologist_id,
            title=review_title,
            review_date=review_date
        ).first()

        if not existing_review:
            review_instance = Review(
                title=review_title,
                review_date=review_date,
                rating=review_rating,
                comment=review_body,
                psychologist_id=psychologist_id
            )

            db.session.add(review_instance)

    db.session.commit()

     

def scrape_clinic_info(clinic_url):
    response = requests.get(clinic_url)
    soup = BeautifulSoup(response.content, "html.parser")
    
    clinic_name = soup.find("title").text
    address = soup.find(itemprop="address")
    street_address = address.find(itemprop="streetAddress").text if address else "Ukjent adresse"
    postal_code = address.find(itemprop="postalCode").text if address else "Ukjent postnummer"
    locality = address.find(itemprop="addressLocality").text if address else "Ukjent kommune"
    phone_element = soup.find("a", itemprop="telephone")
    phone = phone_element.text.strip() if phone_element else "Ukjent telefonnummer"


    clinic_info = {
        "clinic_name": clinic_name,
        "address": street_address,
        "postal_code": postal_code,
        "locality": locality,
        "phone": phone
    }
    return clinic_info


def save_clinic(clinic_data):
    clinic = PrivateClinic.query.filter_by(name=clinic_data['clinic_name']).first()
    if not clinic:
        clinic = PrivateClinic(
            name=clinic_data['clinic_name'],
            address=clinic_data['address'],
            postal_code=clinic_data['postal_code'],
            city=clinic_data['locality'],
            sector_id=2
        )
        db.session.add(clinic)
    else:
        # Oppdater bare hvis den nye informasjonen er tilgjengelig og forskjellig fra "Ukjent"
        if clinic_data['address'] != "Ukjent adresse" and clinic.address == "Ukjent adresse":
            clinic.address = clinic_data['address']
        if clinic_data['postal_code'] != "Ukjent postnummer" and clinic.postal_code == "Ukjent postnummer":
            clinic.postal_code = clinic_data['postal_code']
        if clinic_data['locality'] != "Ukjent kommune" and clinic.city == "Ukjent kommune":
            clinic.city = clinic_data['locality']
        # Anta at sector_id alltid skal oppdateres
        clinic.sector_id = 2

    db.session.commit()
    return clinic


def save_psychologist(soup, name, gender, age, clinic):
    psychologist = Psychologist.query.filter_by(name=name).first()
    psychologist_id = None

    if psychologist:
        # Oppdater eksisterende psykolog med ny informasjon, hvis tilgjengelig
        update_needed = False
        if gender != "Ukjent" and (psychologist.gender is None or psychologist.gender != gender):
            psychologist.gender = gender
            update_needed = True
        if age.isdigit() and (psychologist.birth_year is None or psychologist.birth_year != int(age)):
            psychologist.birth_year = int(age)
            update_needed = True
        if clinic and (psychologist.clinic_id is None or psychologist.clinic_id != clinic.id):
            psychologist.clinic_id = clinic.id
            update_needed = True
        if psychologist.title is None or psychologist.title == "":
            psychologist.title = "Psykolog"  # Setter tittelen til "Psykolog"
            update_needed = True

        if update_needed:
            db.session.commit()

        psychologist_id = psychologist.id

    else:
        # Opprett en ny psykolog hvis den ikke finnes
        new_psychologist = Psychologist(
            name=name,
            title="Psykolog",  # Setter tittelen til "Psykolog" for nye psykologer
            gender=gender if gender != "Ukjent" else None,
            birth_year=int(age) if age.isdigit() else None,
            clinic_id=clinic.id if clinic else None,
        )
        db.session.add(new_psychologist)
        db.session.commit()

        psychologist_id = new_psychologist.id

    if psychologist_id:
        scrape_reviews(soup, psychologist_id)




def scrape_psychologist(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    name = soup.find("h1", itemprop="name").text
    gender, age = get_profile_info(soup)

    # Henter klinikkens URL og informasjon
    clinic_info = soup.find("div", class_="practice-location")
    clinic = None
    if clinic_info and clinic_info.find("a", class_="org-profile-link"):
        clinic_url = "https://www.legelisten.no" + clinic_info.find("a", class_="org-profile-link")["href"]
        clinic_data = scrape_clinic_info(clinic_url)
        clinic = save_clinic(clinic_data)

    # Sørg for å sende alle nødvendige argumenter, inkludert 'clinic'
    save_psychologist(soup, name, gender, age, clinic)  # scrape_reviews kalles inne i denne funksjonen


def scrape_page(base_url, max_pages=100):
    with app.app_context():  # Forsikre at vi er innenfor applikasjonskonteksten
        for page in range(1, max_pages + 1):
            current_url = f"{base_url}?side={page}"
            response = requests.get(current_url)
            if response.status_code != 200:
                break  # Avslutter hvis siden ikke eksisterer eller en annen feil oppstår
            soup = BeautifulSoup(response.content, "html.parser")
            psychologists = soup.find_all("td", class_="name")
            if not psychologists:
                break  # Avslutter hvis det ikke finnes flere psykologer å skrape
            for psychologist in psychologists:
                link = psychologist.find("a")
                if link:
                    psychologist_url = "https://www.legelisten.no" + link["href"]
                    scrape_psychologist(psychologist_url)

# Kaller funksjonen for å skrape opp til 100 sider
scrape_page("https://www.legelisten.no/psykologer/Oslo", 100)
