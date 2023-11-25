import requests
from bs4 import BeautifulSoup
import re
from app import app, db
from models import Psychologist, ProblemArea, psychologist_problem_area, Method, psychologist_method

with app.app_context():
    url = "https://dinpsykolog.no/?page=1&username=&village=oslo&gender=&age="
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    profile_links = soup.find_all("a", class_="link_btn")
    links = [link["href"] if "http" in link["href"] else "https://dinpsykolog.no" + link["href"] for link in profile_links]

    for link in links:
        profile_response = requests.get(link)
        profile_soup = BeautifulSoup(profile_response.content, "html.parser")
        psychologist_name = profile_soup.title.string

        # Opprett og legg til ny Psychologist-instans i databasen
        psychologist = Psychologist(name=psychologist_name)
        db.session.add(psychologist)
        db.session.commit()
        
        selected_option = profile_soup.find("select", {"id": "bornyear"}).find("option", selected=True)
        if selected_option is not None:
            birth_year = selected_option["value"]
            psychologist.birth_year = birth_year
            print(birth_year)
            db.session.add(psychologist)
            db.session.commit()
        else:
            print("No birth year found")
    
        gender_radio = profile_soup.find("input", {"name": "gender", "checked": True})
        if gender_radio is not None:
            gender = gender_radio.parent.text.strip()
            psychologist.gender = gender
            print(gender)
            db.session.add(psychologist)
            db.session.commit()
        else:
            print("No gender found")
        
        profile_photo_div = profile_soup.find("div", class_="profile_img_section")
        if profile_photo_div:
            profile_photo_img = profile_photo_div.find("img")
            if profile_photo_img and profile_photo_img.has_attr("src"):
                profile_photo_url = profile_photo_img["src"]
            # Sjekk om URL-en trenger å bli fullstendig (noen ganger kan den være relativ)
            if not profile_photo_url.startswith("http"):
                profile_photo_url = "https://dinpsykolog.no" + profile_photo_url
            print(profile_photo_url)
            psychologist.profile_picture = profile_photo_url  # Lagrer URL-en til profilbilde
        else:
            print("Profile photo not found")
            psychologist.profile_picture = None
            db.session.add(psychologist)
            db.session.commit()

        phone_number_input = profile_soup.find("input", {"name": "phonenumber"})
        if phone_number_input is not None:
            phone_number = phone_number_input["value"]
            print(phone_number)
            psychologist.phone_number = phone_number
            db.session.add(psychologist)
            db.session.commit()
        else:
            print("No phone number found")

        email_address_input = profile_soup.find("input", {"name": "emailaddress"})
        if email_address_input is not None:
            email_address = email_address_input["value"]
            print(email_address)
            psychologist.email = email_address
            db.session.add(psychologist)
            db.session.commit()       
        else:
            print("No email address found")

        self_report_textarea = profile_soup.find("textarea", {"name": "bodycontent"})
        if self_report_textarea is not None:
            self_report_content = self_report_textarea.get_text(strip=True)
            psychologist.self_report = self_report_content
            db.session.add(psychologist)
            db.session.commit()
            print(self_report_content)
        else:
            print("No self-report textarea found")

        # Skrap problemområder
        problem_areas = profile_soup.find_all("input", {"type": "checkbox", "checked": True})
        problem_areas_labels = [area.parent.text.strip() for area in problem_areas if area.parent.text.strip() in ["Angst", "Stress", "Utbrenthet", "Uro", "Depresjon", "Selvfølelse", "Avhengighet", "Spiseforstyrrelser", "Kroppslige plager", "Lærevansker", "ADHD", "Atferdsproblemer"]]
        print(problem_areas_labels)

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
            psychologist.methods.append(metode)

        # Commit endringer etter å ha lagt til alle metoder
        db.session.commit()


       
    methodologies = profile_soup.find_all("input", {"type": "checkbox", "checked": True, "name": "methods"})
    methodologies_labels = [method.parent.text.strip() for method in methodologies if method.parent.text.strip() in ["Kognitiv atferdsterapi", "Metakognitiv terapi", "Motiverende intervju", "Multisystemisk terapi", "Kognitiv trening", "EMDR", "Mindfulness", "Aksept og forpliktelsesterapi", "Dynamisk terapi"]]
    print(methodologies_labels)
    address_label = profile_soup.find("label", class_="col-xs-4 control-label", string="Address")
    if address_label is not None:
        address = address_label.find_next_sibling("div").find("input", class_="textbox")["value"]
        print(address)
    else:
        print("No address found")

    city_label = profile_soup.find("label", class_="col-xs-4 control-label", string="By")
    if city_label is not None:
        city_input = city_label.find_next_sibling("div").find("input", class_="textbox")
        city = re.sub(r'\d+', '', city_input["value"]).strip()
        print(city)
    else:
        print("No city found")

    postal_code_label = profile_soup.find("label", class_="col-xs-4 control-label", string="By")
    if postal_code_label is not None:
        postal_code_input = postal_code_label.find_next_sibling("div").find("input", class_="textbox")
        postal_code = re.findall(r'\d+', postal_code_input["value"])
        if postal_code:
            print(postal_code[0])
        else:
            print("No postal code found")
    else:
        print("No postal code found")
