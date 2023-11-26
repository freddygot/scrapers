import requests
from bs4 import BeautifulSoup
import re
from app import app, db
from models import Psychologist, ProblemArea, Method, PrivateClinic, Sector

with app.app_context():
    # Sørg for at sektoren "Privat sektor" eksisterer
    privat_sektor = Sector.query.filter_by(name="Privat sektor").first()
    if not privat_sektor:
        privat_sektor = Sector(name="Privat sektor")
        db.session.add(privat_sektor)
        db.session.commit()

    url = "https://dinpsykolog.no/?page=1&username=&village=oslo&gender=&age="
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    profile_links = soup.find_all("a", class_="link_btn")
    links = [link["href"] if "http" in link["href"] else "https://dinpsykolog.no" + link["href"] for link in profile_links]

    for link in links:
        profile_response = requests.get(link)
        profile_soup = BeautifulSoup(profile_response.content, "html.parser")
        psychologist_name = profile_soup.title.string

        # Hent adresse, by og postnummer
        address_label = profile_soup.find("label", class_="col-xs-4 control-label", string="Address")
        address = address_label.find_next_sibling("div").find("input", class_="textbox")["value"] if address_label else None

        city_label = profile_soup.find("label", class_="col-xs-4 control-label", string="By")
        city = city_label.find_next_sibling("div").find("input", class_="textbox")["value"].strip() if city_label else None

        postal_code_label = profile_soup.find("label", class_="col-xs-4 control-label", string="By")
        if postal_code_label:
            postal_code_input = postal_code_label.find_next_sibling("div").find("input", class_="textbox")
            if postal_code_input:
                postal_code_str = postal_code_input["value"]
                match = re.search(r'\d+', postal_code_str)
                postal_code = match.group() if match else None
                print(postal_code)
            else:
                postal_code = None
                print("No postal code input found")
        else:
            postal_code = None
            print("No postal code label found")
            

        # Finn eller opprett klinikk
        klinikk_navn = f"Psykolog {psychologist_name}"
        klinikk = PrivateClinic.query.filter_by(name=klinikk_navn).first()
        if not klinikk:
            klinikk = PrivateClinic(name=klinikk_navn, sector_id=privat_sektor.id, address=address, postal_code=postal_code, city=city,)
            db.session.add(klinikk)
            db.session.commit()

        # Opprett psykolog og tilknytt til klinikk
        psychologist = Psychologist(name=psychologist_name, clinic_id=klinikk.id)
        
        # Behandling av de ulike feltene...
        selected_option = profile_soup.find("select", {"id": "bornyear"}).find("option", selected=True)
        psychologist.birth_year = selected_option["value"] if selected_option and psychologist.birth_year is None else psychologist.birth_year

        gender_radio = profile_soup.find("input", {"name": "gender", "checked": True})
        psychologist.gender = gender_radio.parent.text.strip() if gender_radio and psychologist.gender is None else psychologist.gender

        profile_photo_div = profile_soup.find("div", class_="profile_img_section")
        profile_photo_img = profile_photo_div.find("img") if profile_photo_div else None
        profile_photo_url = profile_photo_img["src"] if profile_photo_img and profile_photo_img.has_attr("src") else None
        if profile_photo_url and not profile_photo_url.startswith("http"):
            profile_photo_url = "https://dinpsykolog.no" + profile_photo_url
        psychologist.profile_picture = profile_photo_url if psychologist.profile_picture is None else psychologist.profile_picture
        
        # Behandling av telefonnummer
        phone_number_input = profile_soup.find("input", {"name": "phonenumber"})
        psychologist.phone_number = phone_number_input["value"] if phone_number_input and psychologist.phone_number is None else psychologist.phone_number

        # Behandling av e-postadresse
        email_address_input = profile_soup.find("input", {"name": "emailaddress"})
        psychologist.email = email_address_input["value"] if email_address_input and psychologist.email is None else psychologist.email

        # Behandling av selvrapportering
        self_report_textarea = profile_soup.find("textarea", {"name": "bodycontent"})
        psychologist.self_report = self_report_textarea.get_text(strip=True) if self_report_textarea and psychologist.self_report is None else psychologist.self_report

        # Lagre psykologen i databasen
        db.session.add(psychologist)
        db.session.commit()

        # Skrap problemområder
        problem_areas = profile_soup.find_all("input", {"type": "checkbox", "checked": True})
        problem_areas_labels = [area.parent.text.strip() for area in problem_areas if area.parent.text.strip() in ["Angst", "Stress", "Utbrenthet", "Uro", "Depresjon", "Selvfølelse", "Avhengighet", "Spiseforstyrrelser", "Kroppslige plager", "Lærevansker", "ADHD", "Atferdsproblemer"]]


        # Lagre problemområdene i problem_area-tabellen og opprett assosiasjon mellom psykolog og problemområde
        for problem_area_label in problem_areas_labels:
            # Sjekk først om problemområdet allerede finnes i databasen
            problem_area = ProblemArea.query.filter_by(description=problem_area_label).first()

            # Hvis ikke, opprett et nytt problemområde og lagre det
            if not problem_area:
                problem_area = ProblemArea(description=problem_area_label)
                db.session.add(problem_area)
                db.session.commit()

            # Legg til problemområdet i psykologens liste over problemområder
            if problem_area not in psychologist.problem_areas:
                psychologist.problem_areas.append(problem_area)

        # Commit endringer etter å ha lagt til alle problemområder
        db.session.commit()
        
        # Skrap metoder
        metoder = profile_soup.find_all("input", {"type": "checkbox", "checked": True, "name": "methods"})
        metode_labels = [metode.parent.text.strip() for metode in metoder]

        # Lagre metodene i Method-tabellen og opprett assosiasjon mellom psykolog og metode
        for metode_label in metode_labels:
            metode = Method.query.filter_by(description=metode_label).first()

            # Hvis ikke, opprett en ny metode og lagre den
            if not metode:
                metode = Method(description=metode_label)
                db.session.add(metode)
                db.session.commit()

            # Legg til metoden i psykologens liste over metoder
            if metode not in psychologist.methods:
                psychologist.methods.append(metode)

        # Commit endringer etter å ha lagt til alle metoder
        db.session.commit()
