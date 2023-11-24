import requests
from bs4 import BeautifulSoup
import re
from app import app, db  # Endret import her
from models import Psychologist  # Importerer Psychologist fra models.py

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

    print(psychologist_name)
    selected_option = profile_soup.find("select", {"id": "bornyear"}).find("option", selected=True)
    if selected_option is not None:
        birth_year = selected_option["value"]
        print(birth_year)
    else:
        print("No birth year found")
    gender_radio = profile_soup.find("input", {"name": "gender", "checked": True})
    if gender_radio is not None:
        gender = gender_radio.parent.text.strip()
        print(gender)
    else:
        print("No gender found")
    profile_photo = profile_soup.find("img", {"height": "200"})
    if profile_photo is not None:
        profile_photo_url = profile_photo["src"]
        print(profile_photo_url)
    else:
        print("No profile photo found")
    phone_number_input = profile_soup.find("input", {"name": "phonenumber"})
    if phone_number_input is not None:
        phone_number = phone_number_input["value"]
        print(phone_number)
    else:
        print("No phone number found")
    email_address_input = profile_soup.find("input", {"name": "emailaddress"})
    if email_address_input is not None:
        email_address = email_address_input["value"]
        print(email_address)
    else:
        print("No email address found")

    self_report_textarea = profile_soup.find("textarea", {"name": "bodycontent"})
    if self_report_textarea is not None:
        self_report_content = self_report_textarea.get_text(strip=True)
        if self_report_content:
            print(self_report_content)
        else:
            print("No self-report content found")
    else:
        print("No self-report textarea found")

    problem_areas = profile_soup.find_all("input", {"type": "checkbox", "checked": True})
    problem_areas_labels = [area.parent.text.strip() for area in problem_areas if area.parent.text.strip() in ["Angst", "Stress", "Utbrenthet", "Uro", "Depresjon", "Selvfølelse", "Avhengighet", "Spiseforstyrrelser", "Kroppslige plager", "Lærevasker", "ADHD", "Atferdsproblemer"]]
    print(problem_areas_labels)
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
