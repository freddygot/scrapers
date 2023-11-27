# Legge til en ny sektor
def add_sector(name):
    new_sector = Sector(name=name)
    db.session.add(new_sector)
    db.session.commit()

# Hente en sektor ved ID
def get_sector_by_id(sector_id):
    return Sector.query.get(sector_id)

# Oppdatere en sektor
def update_sector(sector_id, name):
    sector = Sector.query.get(sector_id)
    sector.name = name
    db.session.commit()

# Slette en sektor
def delete_sector(sector_id):
    sector = Sector.query.get(sector_id)
    db.session.delete(sector)
    db.session.commit()

# Legge til et nytt regionalt helseforetak
def add_regional_health_trust(name, sector_id):
    new_rht = RegionalHealthTrust(name=name, sector_id=sector_id)
    db.session.add(new_rht)
    db.session.commit()

# Hente et regionalt helseforetak ved ID
def get_regional_health_trust_by_id(rht_id):
    return RegionalHealthTrust.query.get(rht_id)

# Oppdatere et regionalt helseforetak
def update_regional_health_trust(rht_id, name, sector_id):
    rht = RegionalHealthTrust.query.get(rht_id)
    rht.name = name
    rht.sector_id = sector_id
    db.session.commit()

# Slette et regionalt helseforetak
def delete_regional_health_trust(rht_id):
    rht = RegionalHealthTrust.query.get(rht_id)
    db.session.delete(rht)
    db.session.commit()

# Legge til et nytt helseforetak
def add_health_trust(name, sector_id, regional_health_trust_id):
    new_ht = HealthTrust(name=name, sector_id=sector_id, regional_health_trust_id=regional_health_trust_id)
    db.session.add(new_ht)
    db.session.commit()

# Hente et helseforetak ved ID
def get_health_trust_by_id(ht_id):
    return HealthTrust.query.get(ht_id)

# Oppdatere et helseforetak
def update_health_trust(ht_id, **kwargs):
    ht = HealthTrust.query.get(ht_id)
    for key, value in kwargs.items():
        setattr(ht, key, value)
    db.session.commit()

# Slette et helseforetak
def delete_health_trust(ht_id):
    ht = HealthTrust.query.get(ht_id)
    db.session.delete(ht)
    db.session.commit()

# Legge til et nytt DPS
def add_dps(name, visitor_address, postal_address, health_trust_id):
    new_dps = DistrictPsychiatricCenter(name=name, visitor_address=visitor_address, postal_address=postal_address, health_trust_id=health_trust_id)
    db.session.add(new_dps)
    db.session.commit()

# Hente et DPS ved ID
def get_dps_by_id(dps_id):
    return DistrictPsychiatricCenter.query.get(dps_id)

# Oppdatere et DPS
def update_dps(dps_id, **kwargs):
    dps = DistrictPsychiatricCenter.query.get(dps_id)
    for key, value in kwargs.items():
        setattr(dps, key, value)
    db.session.commit()

# Slette et DPS
def delete_dps(dps_id):
    dps = DistrictPsychiatricCenter.query.get(dps_id)
    db.session.delete(dps)
    db.session.commit()

# Legge til en ny DPS-avdeling
def add_dps_department(name, about, visitor_address, postal_address, dps_id):
    new_department = DPSDepartment(name=name, about=about, visitor_address=visitor_address, postal_address=postal_address, dps_id=dps_id)
    db.session.add(new_department)
    db.session.commit()

# Hente en DPS-avdeling ved ID
def get_dps_department_by_id(department_id):
    return DPSDepartment.query.get(department_id)

# Oppdatere en DPS-avdeling
def update_dps_department(department_id, **kwargs):
    department = DPSDepartment.query.get(department_id)
    for key, value in kwargs.items():
        setattr(department, key, value)
    db.session.commit()

# Slette en DPS-avdeling
def delete_dps_department(department_id):
    department = DPSDepartment.query.get(department_id)
    db.session.delete(department)
    db.session.commit()

# Legge til en ny DPS-underavdeling
def add_dps_subdepartment(name, about, visitor_address, postal_address, department_id):
    new_subdepartment = DPSSubdepartment(name=name, about=about, visitor_address=visitor_address, postal_address=postal_address, department_id=department_id)
    db.session.add(new_subdepartment)
    db.session.commit()

# Hente en DPS-underavdeling ved ID
def get_dps_subdepartment_by_id(subdepartment_id):
    return DPSSubdepartment.query.get(subdepartment_id)

# Oppdatere en DPS-underavdeling
def update_dps_subdepartment(subdepartment_id, **kwargs):
    subdepartment = DPSSubdepartment.query.get(subdepartment_id)
    for key, value in kwargs.items():
        setattr(subdepartment, key, value)
    db.session.commit()

# Slette en DPS-underavdeling
def delete_dps_subdepartment(subdepartment_id):
    subdepartment = DPSSubdepartment.query.get(subdepartment_id)
    db.session.delete(subdepartment)
    db.session.commit()

# Legge til en ny privat klinikk
def add_private_clinic(name, address, postal_code, city, website, sector_id):
    new_clinic = PrivateClinic(name=name, address=address, postal_code=postal_code, city=city, website=website, sector_id=sector_id)
    db.session.add(new_clinic)
    db.session.commit()

# Hente en privat klinikk ved ID
def get_private_clinic_by_id(clinic_id):
    return PrivateClinic.query.get(clinic_id)

# Oppdatere en privat klinikk
def update_private_clinic(clinic_id, **kwargs):
    clinic = PrivateClinic.query.get(clinic_id)
    for key, value in kwargs.items():
        setattr(clinic, key, value)
    db.session.commit()

# Slette en privat klinikk
def delete_private_clinic(clinic_id):
    clinic = PrivateClinic.query.get(clinic_id)
    db.session.delete(clinic)
    db.session.commit()

# Legg til en ny psykolog
def add_psychologist(name, title, birth_year, gender, clinic_id):
    new_psychologist = Psychologist(name=name, title=title, birth_year=birth_year, gender=gender, clinic_id=clinic_id)
    db.session.add(new_psychologist)
    db.session.commit()

# Hente en psykolog ved ID
def get_psychologist_by_id(psychologist_id):
    return Psychologist.query.get(psychologist_id)

# Oppdatere en psykolog
def update_psychologist(psychologist_id, **kwargs):
    psychologist = Psychologist.query.get(psychologist_id)
    for key, value in kwargs.items():
        setattr(psychologist, key, value)
    db.session.commit()

# Slette en psykolog
def delete_psychologist(psychologist_id):
    psychologist = Psychologist.query.get(psychologist_id)
    db.session.delete(psychologist)
    db.session.commit()
