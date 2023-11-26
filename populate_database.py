from app import app, db
from models import Sector, RegionalHealthTrust, HealthTrust, DistrictPsychiatricCenter, DPSDepartment, DPSSubdepartment

def get_or_create_sector():
    sector_name = "Statlig sektor"
    sector = Sector.query.filter_by(name=sector_name).first()
    if not sector:
        sector = Sector(name=sector_name)
        db.session.add(sector)
        db.session.commit()
    return sector

def get_or_create_regional_health_trust(sector):
    rht_name = "Helse Sør-Øst RHF"
    rht = RegionalHealthTrust.query.filter_by(name=rht_name, sector_id=sector.id).first()
    if not rht:
        rht = RegionalHealthTrust(name=rht_name, sector_id=sector.id)
        db.session.add(rht)
        db.session.commit()
    return rht

def get_or_create_health_trust(rht, sector):
    ht_name = input("Skriv inn navnet på helseforetaket: ")
    ht = HealthTrust.query.filter_by(name=ht_name, regional_health_trust_id=rht.id).first()
    if not ht:
        ht = HealthTrust(name=ht_name, sector_id=sector.id, regional_health_trust_id=rht.id)
        db.session.add(ht)
        db.session.commit()
    return ht

def get_or_create_dps(health_trust):
    dps_name = input("Skriv inn navnet på DPS: ")
    dps = DistrictPsychiatricCenter.query.filter_by(name=dps_name, health_trust_id=health_trust.id).first()
    if not dps:
        dps = DistrictPsychiatricCenter(name=dps_name, health_trust_id=health_trust.id)
        db.session.add(dps)
        db.session.commit()
    return dps

def get_or_create_department(dps):
    dept_name = input("Skriv inn navnet på avdelingen: ")
    full_dept_name = f"{dept_name} ({dps.name})"
    department = DPSDepartment.query.filter_by(name=full_dept_name, dps_id=dps.id).first()
    if not department:
        department = DPSDepartment(name=full_dept_name, dps_id=dps.id)
        db.session.add(department)
        db.session.commit()
    return department

def get_or_create_subdepartment(department):
    subdept_name = input("Skriv inn navnet på underavdelingen: ")
    
    # Anta at department.dps gir tilgang til tilknyttet DPS-objekt
    dps_name = department.dps.name
    full_subdept_name = f"{subdept_name} ({dps_name})"

    subdepartment = DPSSubdepartment.query.filter_by(name=full_subdept_name, department_id=department.id).first()
    if not subdepartment:
        subdepartment = DPSSubdepartment(name=full_subdept_name, department_id=department.id)
        db.session.add(subdepartment)
        db.session.commit()
    return subdepartment


if __name__ == "__main__":
    with app.app_context():
        sector = get_or_create_sector()
        rht = get_or_create_regional_health_trust(sector)
        ht = get_or_create_health_trust(rht, sector)
        dps = get_or_create_dps(ht)
        department = get_or_create_department(dps)
        get_or_create_subdepartment(department)
