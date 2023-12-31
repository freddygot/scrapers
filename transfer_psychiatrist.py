from app import app, db
from app import Psychologist, Psychiatrist, PrivateClinic

def transfer_psychiatrists():
    # Hent alle psykologer som faktisk er psykiatere basert på self_report
    psykiatere = Psychologist.query.filter(Psychologist.self_report.contains("Psykiater med")).all()

    for psykolog in psykiatere:
        # Finn klinikken som er knyttet til psykologen
        klinikk = PrivateClinic.query.get(psykolog.clinic_id)
        print(klinikk)

        # Endre navnet på klinikken hvis den eksisterer
        if klinikk:
            klinikk.name = f"Psykiater {psykolog.name}"
            db.session.add(klinikk)
            db.session.commit()  # Lagre endringen av klinikknavnet i databasen

        # Opprett en ny psykiaterinstans med tilsvarende data
        psykiater = Psychiatrist(
            name=psykolog.name,
            title=psykolog.title,
            birth_year=psykolog.birth_year,
            gender=psykolog.gender,
            profile_picture=psykolog.profile_picture,
            phone_number=psykolog.phone_number,
            email=psykolog.email,
            self_report=psykolog.self_report,
            waiting_time=psykolog.waiting_time,
            clinic_id=psykolog.clinic_id
        )

        # Flytt relasjoner (methods, work_forms, problem_areas) hvis nødvendig
        # Merk: Dette avhenger av din spesifikke database- og relasjonstruktur.
        # psykiater.methods = psykolog.methods
        # psykiater.work_forms = psykolog.work_forms
        # psykiater.problem_areas = psykolog.problem_areas

        # Legg til den nye psykiateren i databasen og slett den gamle psykologen
        db.session.add(psykiater)
        db.session.delete(psykolog)
        db.session.commit()  # Commit endringene til databasen

if __name__ == "__main__":
    with app.app_context():
        transfer_psychiatrists()