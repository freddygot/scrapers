from app import db

# Many-to-many association tables
psychologist_method = db.Table('psychologist_method',
    db.Column('psychologist_id', db.Integer, db.ForeignKey('psychologist.id'), primary_key=True),
    db.Column('method_id', db.Integer, db.ForeignKey('method.id'), primary_key=True)
)

psychologist_work_form = db.Table('psychologist_work_form',
    db.Column('psychologist_id', db.Integer, db.ForeignKey('psychologist.id'), primary_key=True),
    db.Column('work_form_id', db.Integer, db.ForeignKey('work_form.id'), primary_key=True)
)

psychologist_problem_area = db.Table('psychologist_problem_area',
    db.Column('psychologist_id', db.Integer, db.ForeignKey('psychologist.id'), primary_key=True),
    db.Column('problem_area_id', db.Integer, db.ForeignKey('problem_area.id'), primary_key=True)
)

psychologist_services = db.Table('psychologist_services',
    db.Column('psychologist_id', db.Integer, db.ForeignKey('psychologist.id'), primary_key=True),
    db.Column('service_id', db.Integer, db.ForeignKey('service.id'), primary_key=True)
)

psychiatrist_method = db.Table('psychiatrist_method',
    db.Column('psychiatrist_id', db.Integer, db.ForeignKey('psychiatrist.id'), primary_key=True),
    db.Column('method_id', db.Integer, db.ForeignKey('method.id'), primary_key=True)
)

psychiatrist_work_form = db.Table('psychiatrist_work_form',
    db.Column('psychiatrist_id', db.Integer, db.ForeignKey('psychiatrist.id'), primary_key=True),
    db.Column('work_form_id', db.Integer, db.ForeignKey('work_form.id'), primary_key=True)
)

psychiatrist_problem_area = db.Table('psychiatrist_problem_area',
    db.Column('psychiatrist_id', db.Integer, db.ForeignKey('psychiatrist.id'), primary_key=True),
    db.Column('problem_area_id', db.Integer, db.ForeignKey('problem_area.id'), primary_key=True)
)

psychiatrist_services = db.Table('psychiatrist_services',
    db.Column('psychiatrist_id', db.Integer, db.ForeignKey('psychiatrist.id'), primary_key=True),
    db.Column('service_id', db.Integer, db.ForeignKey('service.id'), primary_key=True)
)

general_practitioner_method = db.Table('general_practitioner_method',
    db.Column('general_practitioner_id', db.Integer, db.ForeignKey('general_practitioner.id'), primary_key=True),
    db.Column('method_id', db.Integer, db.ForeignKey('method.id'), primary_key=True)
)

general_practitioner_work_form = db.Table('general_practitioner_work_form',
    db.Column('general_practitioner_id', db.Integer, db.ForeignKey('general_practitioner.id'), primary_key=True),
    db.Column('work_form_id', db.Integer, db.ForeignKey('work_form.id'), primary_key=True)
)

general_practitioner_problem_area = db.Table('general_practitioner_problem_area',
    db.Column('general_practitioner_id', db.Integer, db.ForeignKey('general_practitioner.id'), primary_key=True),
    db.Column('problem_area_id', db.Integer, db.ForeignKey('problem_area.id'), primary_key=True)
)

general_practitioner_services = db.Table('general_practitioner_services',
	db.Column('general_practitioner_id', db.Integer, db.ForeignKey('general_practitioner.id'), primary_key=True),
	db.Column('service_id', db.Integer, db.ForeignKey('service.id'), primary_key=True)
)

dps_subdepartment_method = db.Table('dps_subdepartment_method',
    db.Column('dps_subdepartment_id', db.Integer, db.ForeignKey('dps_subdepartment.id'), primary_key=True),
    db.Column('method_id', db.Integer, db.ForeignKey('method.id'), primary_key=True)
)

dps_subdepartment_problem_area = db.Table('dps_subdepartment_problem_area',
    db.Column('dps_subdepartment_id', db.Integer, db.ForeignKey('dps_subdepartment.id'), primary_key=True),
    db.Column('problem_area_id', db.Integer, db.ForeignKey('problem_area.id'), primary_key=True)
)
# Models
class Sector(db.Model):
    __tablename__ = 'sector'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    regional_health_trusts = db.relationship('RegionalHealthTrust', backref='sector', lazy=True)
    health_trusts = db.relationship('HealthTrust', backref='sector', lazy=True)
    private_clinics = db.relationship('PrivateClinic', backref='sector', lazy=True)
    general_practitioner_offices = db.relationship('GeneralPractitionerOffice', backref='sector', lazy=True)
    psychiatric_emergency_departments = db.relationship('PsychiatricEmergencyDepartment', backref='sector', lazy=True)
    voluntary_organizations = db.relationship('VoluntaryOrganization', backref='sector', lazy=True)

class RegionalHealthTrust(db.Model):
    __tablename__ = 'regional_health_trust'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    sector_id = db.Column(db.Integer, db.ForeignKey('sector.id'), nullable=False)
    health_trusts = db.relationship('HealthTrust', backref='regional_health_trust', lazy=True)

class HealthTrust(db.Model):
    __tablename__ = 'health_trust'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    sector_id = db.Column(db.Integer, db.ForeignKey('sector.id'), nullable=False)
    regional_health_trust_id = db.Column(db.Integer, db.ForeignKey('regional_health_trust.id'), nullable=False)
    district_psychiatric_centers = db.relationship('DistrictPsychiatricCenter', backref='health_trust', lazy=True)

class DistrictPsychiatricCenter(db.Model):
    __tablename__ = 'district_psychiatric_center'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    visitor_address = db.Column(db.String(100), nullable=False)
    postal_address = db.Column(db.String(100), nullable=False)
    health_trust_id = db.Column(db.Integer, db.ForeignKey('health_trust.id'), nullable=False)
    departments = db.relationship('DPSDepartment', backref='dps', lazy=True)

class DPSDepartment(db.Model):
    __tablename__ = 'dps_department'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    about = db.Column(db.Text)
    visitor_address = db.Column(db.String(100), nullable=False)
    postal_address = db.Column(db.String(100), nullable=False)
    dps_id = db.Column(db.Integer, db.ForeignKey('district_psychiatric_center.id'), nullable=False)
    subdepartments = db.relationship('DPSSubdepartment', backref='department', lazy=True)

class DPSSubdepartment(db.Model):
    __tablename__ = 'dps_subdepartment'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    about = db.Column(db.Text)
    visitor_address = db.Column(db.String(100), nullable=False)
    postal_address = db.Column(db.String(100), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('dps_department.id'), nullable=False)

class PrivateClinic(db.Model):
    __tablename__ = 'private_clinic'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    postal_code = db.Column(db.String(100), nullable=True)
    city = db.Column(db.String(100), nullable=False)
    website = db.Column(db.String(100))
    sector_id = db.Column(db.Integer, db.ForeignKey('sector.id'), nullable=False)
    psychologists = db.relationship('Psychologist', backref='clinic', lazy=True)
    psychiatrists = db.relationship('Psychiatrist', backref='clinic', lazy=True)

class Psychologist(db.Model):
    __tablename__ = 'psychologist'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(100))
    birth_year = db.Column(db.Integer)
    gender = db.Column(db.String(100))
    profile_picture = db.Column(db.String(100))
    phone_number = db.Column(db.Integer)
    email = db.Column(db.String(100))
    self_report = db.Column(db.String(600))
    waiting_time = db.Column(db.String(100))
    clinic_id = db.Column(db.Integer, db.ForeignKey('private_clinic.id'), nullable=True)
    methods = db.relationship('Method', secondary=psychologist_method, back_populates='psychologists')
    work_forms = db.relationship('WorkForm', secondary=psychologist_work_form, back_populates='psychologists')
    problem_areas = db.relationship('ProblemArea', secondary=psychologist_problem_area, back_populates='psychologists')


class Psychiatrist(db.Model):
    __tablename__ = 'psychiatrist'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(100))
    birth_year = db.Column(db.Integer)
    gender = db.Column(db.String(100))
    profile_picture = db.Column(db.String(100))
    phone_number = db.Column(db.Integer)
    email = db.Column(db.String(100))
    self_report = db.Column(db.String(600))
    waiting_time = db.Column(db.String(100))
    clinic_id = db.Column(db.Integer, db.ForeignKey('private_clinic.id'), nullable=True)
    methods = db.relationship('Method', secondary=psychiatrist_method, back_populates='psychiatrists')
    work_forms = db.relationship('WorkForm', secondary=psychiatrist_work_form, back_populates='psychiatrists')
    problem_areas = db.relationship('ProblemArea', secondary=psychiatrist_problem_area, back_populates='psychiatrists')

class GeneralPractitionerOffice(db.Model):
    __tablename__ = 'general_practitioner_office'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    sector_id = db.Column(db.Integer, db.ForeignKey('sector.id'), nullable=False)
    general_practitioners = db.relationship('GeneralPractitioner', backref='general_practitioner_office', lazy=True)

class GeneralPractitioner(db.Model):
    __tablename__ = 'general_practitioner'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    office_id = db.Column(db.Integer, db.ForeignKey('general_practitioner_office.id'), nullable=False)
    methods = db.relationship('Method', secondary=general_practitioner_method, back_populates='general_practitioners')
    work_forms = db.relationship('WorkForm', secondary=general_practitioner_work_form, back_populates='general_practitioners')
    problem_areas = db.relationship('ProblemArea', secondary=general_practitioner_problem_area, back_populates='general_practitioners')

class PsychiatricEmergencyDepartment(db.Model):
    __tablename__ = 'psychiatric_emergency_department'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    sector_id = db.Column(db.Integer, db.ForeignKey('sector.id'), nullable=False)
    
class VoluntaryOrganization(db.Model):
    __tablename__ = 'voluntary_organization'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    sector_id = db.Column(db.Integer, db.ForeignKey('sector.id'), nullable=False)

class Method(db.Model):
    __tablename__ = 'method'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text, nullable=False)
    psychologists = db.relationship('Psychologist', secondary=psychologist_method, back_populates='methods')
    psychiatrists = db.relationship('Psychiatrist', secondary=psychiatrist_method, back_populates='methods')
    dps_subdepartment = db.relationship('DPSSubdepartment', secondary=dps_subdepartment_method, back_populates='methods')
    general_practitioners = db.relationship('GeneralPractitioner', secondary=general_practitioner_method, back_populates='methods')



class WorkForm(db.Model):
    __tablename__ = 'work_form'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text, nullable=False)
    psychologists = db.relationship('Psychologist', secondary=psychologist_work_form, back_populates='work_forms')
    psychiatrists = db.relationship('Psychiatrist', secondary=psychiatrist_work_form, back_populates='work_forms')
    general_practitioners = db.relationship('GeneralPractitioner', secondary=general_practitioner_work_form, back_populates='work_forms')

class ProblemArea(db.Model):
    __tablename__ = 'problem_area'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text, nullable=False)
    psychologists = db.relationship('Psychologist', secondary=psychologist_problem_area, back_populates='problem_areas')
    psychiatrists = db.relationship('Psychiatrist', secondary=psychiatrist_problem_area, back_populates='problem_areas')
    dps_subdepartment = db.relationship('DPSSubdepartment', secondary=dps_subdepartment_problem_area, back_populates='problem_areas')
    general_practitioners = db.relationship('GeneralPractitioner', secondary=general_practitioner_problem_area, back_populates='problem_areas')

class Service(db.Model):
	__tablename__ = 'service'
	id = db.Column(db.Integer, primary_key=True)
	description = db.Column(db.String(100), nullable=False)
	duration = db.Column(db.Integer, nullable=False)  # Duration in minutes
	price = db.Column(db.Float, nullable=False)  # Price in your currency
	psychologists = db.relationship('Psychologist', secondary=psychologist_services, backref=db.backref('services', lazy='dynamic'))
	psychiatrists = db.relationship('Psychiatrist', secondary=psychiatrist_services, backref=db.backref('services', lazy='dynamic'))
	general_practitioners = db.relationship('GeneralPractitioner', secondary=general_practitioner_services, backref=db.backref('services', lazy='dynamic'))

class Review(db.Model):
	__tablename__ = 'review'
	id = db.Column(db.Integer, primary_key=True)
	rating = db.Column(db.Float, nullable=False)  # Rating, for example a scale from 1 to 5
	comment = db.Column(db.Text, nullable=True)  # Review text
	# Foreign keys to healthcare professionals
	psychologist_id = db.Column(db.Integer, db.ForeignKey('psychologist.id'), nullable=True)
	psychiatrist_id = db.Column(db.Integer, db.ForeignKey('psychiatrist.id'), nullable=True)
	general_practitioner_id = db.Column(db.Integer, db.ForeignKey('general_practitioner.id'), nullable=True)
