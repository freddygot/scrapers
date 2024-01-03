import requests
from bs4 import BeautifulSoup
import re
from app import app, db
from app import Psychologist, PrivateClinic, Sector, ProblemArea, Method

with app.app_context():
    privat_sektor = Sector.query.filter_by(name="Privat sektor").first()
    if not privat_sektor:
        privat_sektor = Sector(name="Privat sektor")
        db.session.add(privat_sektor)
        db.session.commit()

    for page in range(1, 30):
        url = f"https://dinpsykolog.no/?page={page}&username=&village=oslo&gender=&age="
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")

        profile_links = soup.find_all("a", class_="link_btn")
        links = [link["href"] if "http" in link["href"] else "https://dinpsykolog.no" + link["href"] for link in profile_links]

        for link in links:
            profile_response = requests.get(link)
            profile_soup = BeautifulSoup(profile_response.content, "html.parser")
            psychologist_name = profile_soup.title.string.split(" - ")[0].strip()

            existing_psychologist = Psychologist.query.filter_by(name=psychologist_name).first()

            if existing_psychologist:
                psychologist = existing_psychologist

                if not psychologist.title:
                    psychologist.title = "Psykolog"

                if not psychologist.birth_year:
                    selected_option = profile_soup.find("select", {"id": "bornyear"}).find("option", selected=True)
                    psychologist.birth_year = selected_option["value"] if selected_option else None

                if not psychologist.gender:
                    gender_radio = profile_soup.find("input", {"name": "gender", "checked": True})
                    psychologist.gender = gender_radio.parent.text.strip() if gender_radio else None

                if not psychologist.profile_picture:
                    profile_photo_div = profile_soup.find("div", class_="profile_img_section")
                    profile_photo_img = profile_photo_div.find("img") if profile_photo_div else None
                    profile_photo_url = "https://dinpsykolog.no" + profile_photo_img["src"] if profile_photo_img and profile_photo_img.has_attr("src") and not profile_photo_img["src"].startswith("http") else None
                    psychologist.profile_picture = profile_photo_url if profile_photo_url else None

                if not psychologist.phone_number:
                    phone_number_input = profile_soup.find("input", {"name": "phonenumber"})
                    psychologist.phone_number = phone_number_input["value"] if phone_number_input else None

                if not psychologist.email:
                    email_address_input = profile_soup.find("input", {"name": "emailaddress"})
                    psychologist.email = email_address_input["value"] if email_address_input else None

                if not psychologist.self_report:
                    self_report_textarea = profile_soup.find("textarea", {"name": "bodycontent"})
                    psychologist.self_report = self_report_textarea.get_text(strip=True) if self_report_textarea else None

                if not psychologist.problem_areas:
                    psychologist.problem_areas = []

                db.session.commit()
            else:
                new_psychologist = Psychologist(name=psychologist_name)
                db.session.add(new_psychologist)

                new_psychologist.title = "Psykolog"

                selected_option = profile_soup.find("select", {"id": "bornyear"}).find("option", selected=True)
                new_psychologist.birth_year = selected_option["value"] if selected_option else None

                gender_radio = profile_soup.find("input", {"name": "gender", "checked": True})
                new_psychologist.gender = gender_radio.parent.text.strip() if gender_radio else None

                profile_photo_div = profile_soup.find("div", class_="profile_img_section")
                profile_photo_img = profile_photo_div.find("img") if profile_photo_div else None
                profile_photo_url = "https://dinpsykolog.no" + profile_photo_img["src"] if profile_photo_img and profile_photo_img.has_attr("src") and not profile_photo_img["src"].startswith("http") else None
                new_psychologist.profile_picture = profile_photo_url if profile_photo_url else None

                phone_number_input = profile_soup.find("input", {"name": "phonenumber"})
                new_psychologist.phone_number = phone_number_input["value"] if phone_number_input else None

                email_address_input = profile_soup.find("input", {"name": "emailaddress"})
                new_psychologist.email = email_address_input["value"] if email_address_input else None

                self_report_textarea = profile_soup.find("textarea", {"name": "bodycontent"})
                new_psychologist.self_report = self_report_textarea.get_text(strip=True) if self_report_textarea else None

                new_psychologist.problem_areas = []

                # Behandling av adresse, by og postnummer for klinikken
                address_label = profile_soup.find("label", class_="col-xs-4 control-label", string="Address")
                address = address_label.find_next_sibling("div").find("input", class_="textbox")["value"] if address_label else None

                city_label = profile_soup.find("label", class_="col-xs-4 control-label", string="By")
                city_input = city_label.find_next_sibling("div").find("input", class_="textbox") if city_label else None
                city = " ".join(re.findall(r'[A-Za-zæøåÆØÅ]+', city_input["value"])) if city_input else None

                postal_code_label = profile_soup.find("label", class_="col-xs-4 control-label", string="By")
                if postal_code_label:
                    postal_code_input = postal_code_label.find_next_sibling("div").find("input", class_="textbox")
                    if postal_code_input:
                        postal_code_str = postal_code_input["value"]
                        match = re.search(r'\d+', postal_code_str)
                        postal_code = match.group() if match else None
                    else:
                        postal_code = None
                else:
                    postal_code = None

                problem_areas = profile_soup.find_all("input", {"type": "checkbox", "checked": True})
                for area in problem_areas:
                    problem_area_label = area.parent.text.strip()
                    problem_area = ProblemArea.query.filter_by(description=problem_area_label).first()
                    if not problem_area:
                        problem_area = ProblemArea(description=problem_area_label)
                        db.session.add(problem_area)

                    if problem_area not in new_psychologist.problem_areas:
                        new_psychologist.problem_areas.append(problem_area)

                # Skrap og lagre metoder
                methods = profile_soup.find_all("input", {"type": "checkbox", "checked": True, "name": "methods"})
                for method_input in methods:
                    method_label = method_input.parent.text.strip()
                    method = Method.query.filter_by(description=method_label).first()
                    if not method:
                        method = Method(description=method_label)
                        db.session.add(method)

                    if method not in new_psychologist.methods:
                        new_psychologist.methods.append(method)

                klinikk_navn = f"Psykolog {psychologist_name} Klinikk"
                klinikk = PrivateClinic(name=klinikk_navn, sector_id=privat_sektor.id, address=address, postal_code=postal_code, city=city)
                db.session.add(klinikk)
                new_psychologist.clinic = klinikk

                db.session.commit()
