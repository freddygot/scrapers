from flask import Flask, request, jsonify, render_template, redirect, url_for
import logging
from logging.handlers import RotatingFileHandler
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
# Logger setup
logging.basicConfig(level=logging.INFO)
handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=3)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(handler)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///psychologists.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)


#MODELLER


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

dps_level_2_method = db.Table('dps_level_2_method',
    db.Column('dps_level_2_id', db.Integer, db.ForeignKey('dps_level_2.id'), primary_key=True),
    db.Column('method_id', db.Integer, db.ForeignKey('method.id'), primary_key=True)
)

dps_level_3_method = db.Table('dps_level_3_method',
    db.Column('dps_level_2_id', db.Integer, db.ForeignKey('dps_level_2.id'), primary_key=True),
    db.Column('method_id', db.Integer, db.ForeignKey('method.id'), primary_key=True)
)


dps_level_2_problem_area = db.Table('dps_level_2_problem_area',
    db.Column('dps_level_2_id', db.Integer, db.ForeignKey('dps_level_2.id'), primary_key=True),
    db.Column('problem_area_id', db.Integer, db.ForeignKey('problem_area.id'), primary_key=True)
)

dps_level_3_problem_area = db.Table('dps_level_3_problem_area',
    db.Column('dps_level_3_id', db.Integer, db.ForeignKey('dps_level_3.id'), primary_key=True),
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
    healthtrusts_departments = db.relationship('HealthTrustsDepartment', backref='health_trust', lazy=True)


class HealthTrustsDepartment(db.Model):
    __tablename__ = 'healthtrusts_department'  # Tabellnavnet i databasen
    id = db.Column(db.Integer, primary_key=True)  # Primærnøkkel
    name = db.Column(db.String(100), nullable=False)
    visitor_address = db.Column(db.String(100), nullable=False)
    visitor_postal_code = db.Column(db.String(100), nullable=True)
    postal_address = db.Column(db.String(100), nullable=False)
    postal_postal_code = db.Column(db.String(100), nullable=True)
    city = db.Column(db.String(100), nullable=True)
    general_info = db.Column(db.Text)
    practical_info = db.Column(db.Text)
    phone_number = db.Column(db.Integer)
    email = db.Column(db.String(100))
    health_trust_id = db.Column(db.Integer, db.ForeignKey('health_trust.id'), nullable=False)

class DistrictPsychiatricCenter(db.Model):
    __tablename__ = 'district_psychiatric_center'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    visitor_address = db.Column(db.String(100), nullable=False)
    visitor_postal_code = db.Column(db.String(100), nullable=True)
    postal_address = db.Column(db.String(100), nullable=False)
    postal_postal_code = db.Column(db.String(100), nullable=True)
    city = db.Column(db.String(100), nullable=True)
    general_info = db.Column(db.Text)
    practical_info = db.Column(db.Text)
    phone_number = db.Column(db.Integer)
    email = db.Column(db.String(100))
    health_trust_id = db.Column(db.Integer, db.ForeignKey('health_trust.id'), nullable=False)
    departments = db.relationship('DPSLevel1', backref='dps', lazy=True)

class DPSLevel1(db.Model):
    __tablename__ = 'dps_level_1'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    by = db.Column(db.String(100), nullable=False)
    visitor_address = db.Column(db.String(100), nullable=False)
    postal_address = db.Column(db.String(100), nullable=False)
    general_info = db.Column(db.Text)
    practical_info = db.Column(db.Text)
    email = db.Column(db.String(100))
    phone_number = db.Column(db.Integer)
    treatment_description = db.Column(db.Text)
    dps_id = db.Column(db.Integer, db.ForeignKey('district_psychiatric_center.id'), nullable=False)
    subdepartments = db.relationship('DPSLevel2', backref='department', lazy=True)

class DPSLevel2(db.Model):
    __tablename__ = 'dps_level_2'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    about = db.Column(db.Text)
    visitor_address = db.Column(db.String(100), nullable=False)
    postal_address = db.Column(db.String(100), nullable=False)
    general_info = db.Column(db.Text)
    practical_info = db.Column(db.Text)
    phone_number = db.Column(db.Integer)
    email = db.Column(db.String(100))
    treatment_description = db.Column(db.Text)
    department_id = db.Column(db.Integer, db.ForeignKey('dps_level_1.id'), nullable=False)
    methods = db.relationship('Method', secondary=dps_level_2_method, back_populates='dps_level_2s')
    problem_areas = db.relationship('ProblemArea', secondary=dps_level_2_problem_area, back_populates='dps_level_2s')

class DPSLevel3(db.Model):
    __tablename__ = 'dps_level_3'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    about = db.Column(db.Text)
    visitor_address = db.Column(db.String(100), nullable=False)
    postal_address = db.Column(db.String(100), nullable=False)
    general_info = db.Column(db.Text)
    practical_info = db.Column(db.Text)
    treatment_description = db.Column(db.Text)
    department_id = db.Column(db.Integer, db.ForeignKey('dps_level_3.id'), nullable=False)




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
    dps_level_2s = db.relationship('DPSLevel2', secondary=dps_level_2_method, back_populates='methods')
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
    dps_level_2s = db.relationship('DPSLevel2', secondary=dps_level_2_problem_area, back_populates='problem_areas')
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

#RUTER
@app.route('/add_sector', methods=['GET', 'POST'])
def add_sector():
    if request.method == 'POST':
        name = request.form.get('name')
        if name:
            add_sector(name)
            return redirect(url_for('index'))
        else:
            return "Navn er påkrevd", 400
    return render_template('add_sector.html')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sector/<int:sector_id>', methods=['GET'])
def get_sector_route(sector_id):
    sector = get_sector_by_id(sector_id)
    if sector:
        return jsonify({
            'id': sector.id,
            'name': sector.name
        })
    else:
        return "Sektor ikke funnet", 404

@app.route('/sector/<int:sector_id>', methods=['PUT'])
def update_sector_route(sector_id):
    data = request.json
    name = data.get('name')
    if not name:
        return "Mangler nødvendig felt: 'name'", 400

    try:
        update_sector(sector_id, name)
        return f"Sektor med ID {sector_id} har blitt oppdatert."
    except Exception as e:
        return str(e), 500

@app.route('/sector/<int:sector_id>', methods=['DELETE'])
def delete_sector_route(sector_id):
    try:
        delete_sector(sector_id)
        return f"Sektor med ID {sector_id} har blitt slettet."
    except Exception as e:
        return str(e), 500


@app.route('/add_regional_health_trust', methods=['GET', 'POST'])
def add_regional_health_trust():
    if request.method == 'POST':
        name = request.form.get('name')
        sector_id = request.form.get('sector_id')
        if name and sector_id:
            add_regional_health_trust(name, sector_id)
            return redirect(url_for('index'))
        else:
            return "Navn og sektor er påkrevd", 400

    sectors = get_all_sectors()
    return render_template('add_regional_health_trust.html', sectors=sectors)

@app.route('/regional_health_trust/<int:rht_id>', methods=['GET'])
def get_regional_health_trust_route(rht_id):
    rht = get_regional_health_trust_by_id(rht_id)
    if rht:
        return jsonify({
            'id': rht.id,
            'name': rht.name,
            'sector_id': rht.sector_id
        })
    else:
        return "Regionalt helseforetak ikke funnet", 404

@app.route('/regional_health_trust/<int:rht_id>', methods=['PUT'])
def update_regional_health_trust_route(rht_id):
    data = request.json
    name = data.get('name')
    sector_id = data.get('sector_id')
    if not name or sector_id is None:
        return "Mangler nødvendig felt: 'name' eller 'sector_id'", 400

    try:
        update_regional_health_trust(rht_id, name, sector_id)
        return f"Regionalt helseforetak med ID {rht_id} har blitt oppdatert."
    except Exception as e:
        return str(e), 500

@app.route('/regional_health_trust/<int:rht_id>', methods=['DELETE'])
def delete_regional_health_trust_route(rht_id):
    try:
        delete_regional_health_trust(rht_id)
        return f"Regionalt helseforetak med ID {rht_id} har blitt slettet."
    except Exception as e:
        return str(e), 500

@app.route('/add_health_trust', methods=['GET', 'POST'])
def add_health_trust():
    if request.method == 'POST':
        name = request.form.get('name')
        sector_id = request.form.get('sector_id')
        regional_health_trust_id = request.form.get('regional_health_trust_id')
        if name and sector_id and regional_health_trust_id:
            add_health_trust(name, sector_id, regional_health_trust_id)
            return redirect(url_for('index'))
        else:
            return "Navn, sektor og regionalt helseforetak er påkrevd", 400

    sectors = get_all_sectors()
    regional_health_trusts = get_all_regional_health_trusts()
    return render_template('add_health_trust.html', sectors=sectors, regional_health_trusts=regional_health_trusts)

@app.route('/health_trust/<int:ht_id>', methods=['GET'])
def get_health_trust_route(ht_id):
    health_trust = get_health_trust_by_id(ht_id)
    if health_trust:
        return jsonify({
            'id': health_trust.id,
            'name': health_trust.name,
            'sector_id': health_trust.sector_id,
            'regional_health_trust_id': health_trust.regional_health_trust_id
        })
    else:
        return "Helseforetak ikke funnet", 404

@app.route('/health_trust/<int:ht_id>', methods=['PUT'])
def update_health_trust_route(ht_id):
    data = request.json
    name = data.get('name')
    sector_id = data.get('sector_id')
    regional_health_trust_id = data.get('regional_health_trust_id')

    if not all([name, sector_id, regional_health_trust_id]):
        return "Mangler nødvendig felt", 400

    try:
        update_health_trust(ht_id, name, sector_id, regional_health_trust_id)
        return f"Helseforetak med ID {ht_id} har blitt oppdatert."
    except Exception as e:
        return str(e), 500

@app.route('/health_trust/<int:ht_id>', methods=['DELETE'])
def delete_health_trust_route(ht_id):
    try:
        delete_health_trust(ht_id)
        return f"Helseforetak med ID {ht_id} har blitt slettet."
    except Exception as e:
        return str(e), 500


# ... eksisterende ruter ...

@app.route('/add_dps', methods=['GET', 'POST'])
def add_dps():
    if request.method == 'POST':
        # Hent verdiene fra skjemaet
        name = request.form.get('name')
        general_info = request.form.get('general_info')
        practical_info = request.form.get('practical_info')
        city = request.form.get('city')
        visitor_address = request.form.get('visitor_address')
        visitor_postal_code = request.form.get('visitor_postal_code')
        postal_address = request.form.get('postal_address')
        postal_postal_code = request.form.get('postal_postal_code')
        email = request.form.get('email')
        phone_number = request.form.get('phone_number')
        health_trust_id = request.form.get('health_trust_id')

        # Sjekk at alle feltene er fylt ut
        if not all([name, general_info, practical_info, city, visitor_address, visitor_postal_code, postal_address, postal_postal_code, email, phone_number, health_trust_id]):
            return "Alle felt er påkrevd", 400

        # Kall på CRUD-metoden for å legge til DPS
        add_dps(name, general_info, practical_info, city, visitor_address, visitor_postal_code, postal_address, postal_postal_code, email, phone_number, health_trust_id)
        return redirect(url_for('index'))

    health_trusts = get_all_health_trusts()  # Antatt metode for å hente alle helseforetak
    return render_template('add_dps.html', health_trusts=health_trusts)

    

@app.route('/dps/<int:dps_id>', methods=['GET'])
def get_dps_route(dps_id):
    dps = get_dps_by_id(dps_id)
    if dps:
        return jsonify({
            'id': dps.id,
            'name': dps.name,
            'visitor_address': dps.visitor_address,
            'postal_address': dps.postal_address,
            'health_trust_id': dps.health_trust_id
        })
    else:
        return "DPS ikke funnet", 404

@app.route('/dps/<int:dps_id>', methods=['PUT'])
def update_dps_route(dps_id):
    data = request.json
    name = data.get('name')
    visitor_address = data.get('visitor_address')
    postal_address = data.get('postal_address')
    health_trust_id = data.get('health_trust_id')

    if not all([name, visitor_address, postal_address, health_trust_id]):
        return "Mangler nødvendig felt", 400

    try:
        update_dps(dps_id, name, visitor_address, postal_address, health_trust_id)
        return f"DPS med ID {dps_id} har blitt oppdatert."
    except Exception as e:
        return str(e), 500

@app.route('/dps/<int:dps_id>', methods=['DELETE'])
def delete_dps_route(dps_id):
    try:
        delete_dps(dps_id)
        return f"DPS med ID {dps_id} har blitt slettet."
    except Exception as e:
        return str(e), 500


@app.route('/dps_level_1', methods=['GET', 'POST'])
def add_dps_level_1():
    if request.method == 'POST':
        name = request.form.get('name')
        by = request.form.get('by')
        visitor_address = request.form.get('visitor_address')
        postal_address = request.form.get('postal_address')
        general_info = request.form.get('general_info')
        practical_info = request.form.get('practical_info')
        email = request.form.get('email')
        phone_number = request.form.get('phone_number')
        dps_id = request.form.get('dps_id')

        if not all([name, by, visitor_address, postal_address, dps_id]):
            return "Alle nødvendige felt må fylles ut", 400

        add_dps_level_1(name, by, visitor_address, postal_address, general_info, practical_info, email, phone_number, dps_id)
        return redirect(url_for('index'))

    dps_list = get_all_dps()  # Antatt metode for å hente alle DPS
    return render_template('add_dps_level_1.html', dps_list=dps_list)

def get_all_dps():
    return DistrictPsychiatricCenter.query.all()


@app.route('/dps_level_1/<int:department_id>', methods=['GET'])
def get_dps_level_1_route(department_id):
    department = get_dps_level_1_by_id(department_id)
    if department:
        return jsonify({
            'id': department.id,
            'name': department.name,
            'about': department.about,
            'visitor_address': department.visitor_address,
            'postal_address': department.postal_address,
            'dps_id': department.dps_id
        })
    else:
        return "DPS-avdeling ikke funnet", 404

@app.route('/dps_level_1/<int:department_id>', methods=['PUT'])
def update_dps_level_1_route(department_id):
    data = request.json
    name = data.get('name')
    about = data.get('about')
    visitor_address = data.get('visitor_address')
    postal_address = data.get('postal_address')
    dps_id = data.get('dps_id')

    if not all([name, about, visitor_address, postal_address, dps_id]):
        return "Mangler nødvendig felt", 400

    try:
        update_dps_level_1(department_id, name, about, visitor_address, postal_address, dps_id)
        return f"DPS-avdeling med ID {department_id} har blitt oppdatert."
    except Exception as e:
        return str(e), 500

@app.route('/dps_level_1/<int:department_id>', methods=['DELETE'])
def delete_dps_level_1_route(department_id):
    try:
        delete_dps_level_1(department_id)
        return f"DPS-avdeling med ID {department_id} har blitt slettet."
    except Exception as e:
        return str(e), 500

@app.route('/add_dps_level_2', methods=['GET', 'POST'])
def add_dps_level_2_route():
    try:
        if request.method == 'POST':
            # Hent data fra formen
            name = request.form['name']
            about = request.form['about']
            visitor_address = request.form['visitor_address']
            postal_address = request.form['postal_address']
            general_info = request.form['general_info']
            practical_info = request.form['practical_info']
            treatment_description = request.form['treatment_description']
            email = request.form['email']
            phone_number = request.form['phone_number']
            department_id = request.form['department_id']
            method_ids = request.form.getlist('methods')
            problem_area_ids = request.form.getlist('problem_areas')
            new_methods = request.form.get('new_methods', '')
            new_problem_areas = request.form.get('new_problem_areas', '')

            # Kall funksjonen for å legge til DPS Nivå 2
            add_dps_level_2(name, about, visitor_address, postal_address, general_info, practical_info, treatment_description, email, phone_number, department_id, method_ids, problem_area_ids, new_methods, new_problem_areas)
            
            logger.info("DPS Nivå 2 underavdeling lagt til: %s", name)
            return redirect(url_for('index'))

        departments = DPSLevel1.query.all()
        methods = Method.query.all()
        problem_areas = ProblemArea.query.all()
        return render_template('add_dps_level_2.html', departments=departments, methods=methods, problem_areas=problem_areas)
    except Exception as e:
        logger.error("Feil under behandling av /add_dps_level_2: %s", str(e))
        return str(e), 500




@app.route('/dps_level_2/<int:subdepartment_id>', methods=['GET'])
def get_dps_level_2_route(subdepartment_id):
    subdepartment = get_dps_level_2_by_id(subdepartment_id)
    if subdepartment:
        return jsonify({
            'id': subdepartment.id,
            'name': subdepartment.name,
            'about': subdepartment.about,
            'visitor_address': subdepartment.visitor_address,
            'postal_address': subdepartment.postal_address,
            'department_id': subdepartment.department_id
        })
    else:
        return "DPS-underavdeling ikke funnet", 404

@app.route('/dps_level_2/<int:subdepartment_id>', methods=['PUT'])
def update_dps_level_2_route(subdepartment_id):
    data = request.json
    name = data.get('name')
    about = data.get('about')
    visitor_address = data.get('visitor_address')
    postal_address = data.get('postal_address')
    department_id = data.get('department_id')

    if not all([name, about, visitor_address, postal_address, department_id]):
        return "Mangler nødvendig felt", 400

    try:
        update_dps_level_2(subdepartment_id, name, about, visitor_address, postal_address, department_id)
        return f"DPS-underavdeling med ID {subdepartment_id} har blitt oppdatert."
    except Exception as e:
        return str(e), 500

@app.route('/dps_level_2/<int:subdepartment_id>', methods=['DELETE'])
def delete_dps_level_2_route(subdepartment_id):
    try:
        delete_dps_level_2(subdepartment_id)
        return f"DPS-underavdeling med ID {subdepartment_id} har blitt slettet."
    except Exception as e:
        return str(e), 500


@app.route('/add_private_clinic', methods=['POST'])
def add_private_clinic_route():
    # Hent og prosesser data fra request her
    return "Privat klinikk lagt til"

@app.route('/add_psychologist', methods=['POST'])
def add_psychologist_route():
    # Her vil du hente data fra request og kalle add_psychologist
    return "Psykolog lagt til"

# Definer andre ruter her...



#Legge til en ny sektor
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

def get_all_sectors():
    return Sector.query.all()

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

def get_all_regional_health_trusts():
    return RegionalHealthTrust.query.all()

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

def get_all_health_trusts():
    return HealthTrust.query.all()

# Legge til et nytt DPS
def add_dps(name, general_info, practical_info, city, visitor_address, visitor_postal_code, postal_address, postal_postal_code, email, phone_number, health_trust_id):
    new_dps = DistrictPsychiatricCenter(
        name=name,
        general_info=general_info,
        practical_info=practical_info,
        city=city,
        visitor_address=visitor_address,
        visitor_postal_code=visitor_postal_code,
        postal_address=postal_address,
        postal_postal_code=postal_postal_code,
        email=email,
        phone_number=phone_number,
        health_trust_id=health_trust_id
    )
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
def add_dps_level_2(name, about, visitor_address, postal_address, general_info, practical_info, treatment_description, email, phone_number, department_id, method_ids, problem_area_ids, new_methods, new_problem_areas):
    try:
        # Opprette ny DPS Nivå 2 underavdeling
        new_subdepartment = DPSLevel2(
            name=name, 
            about=about, 
            visitor_address=visitor_address, 
            postal_address=postal_address, 
            general_info=general_info,
            practical_info=practical_info,
            treatment_description=treatment_description,
            email=email, 
            phone_number=phone_number,
            department_id=department_id
        )
        db.session.add(new_subdepartment)
        db.session.flush()  # For å få generert ID for new_subdepartment

        # Behandle eksisterende metoder
        existing_methods = Method.query.filter(Method.id.in_(method_ids)).all()
        for method in existing_methods:
            if method not in new_subdepartment.methods:
                new_subdepartment.methods.append(method)

        # Behandle nye metoder
        if new_methods:
            for method_desc in new_methods.split(','):
                method_desc = method_desc.strip()
                method = Method.query.filter_by(description=method_desc).first()
                if not method:
                    method = Method(description=method_desc)
                    db.session.add(method)
                if method not in new_subdepartment.methods:
                    new_subdepartment.methods.append(method)

        # Behandle eksisterende problemområder
        existing_problem_areas = ProblemArea.query.filter(ProblemArea.id.in_(problem_area_ids)).all()
        for problem_area in existing_problem_areas:
            if problem_area not in new_subdepartment.problem_areas:
                new_subdepartment.problem_areas.append(problem_area)

        # Behandle nye problemområder
        if new_problem_areas:
            for problem_area_desc in new_problem_areas.split(','):
                problem_area_desc = problem_area_desc.strip()
                problem_area = ProblemArea.query.filter_by(description=problem_area_desc).first()
                if not problem_area:
                    problem_area = ProblemArea(description=problem_area_desc)
                    db.session.add(problem_area)
                if problem_area not in new_subdepartment.problem_areas:
                    new_subdepartment.problem_areas.append(problem_area)

        # Lagre endringene
        db.session.commit()
        logger.info(f"DPS Nivå 2 underavdeling lagt til: {name}")

    except Exception as e:
        logger.error(f"Feil ved tillegging av DPS Nivå 2 underavdeling: {e}")
        db.session.rollback()
        raise e  # Re-raise the exception to handle it in the calling context





# Hente en DPS-avdeling ved ID
def get_dps_level_1_by_id(department_id):
    return DPSLevel1.query.get(department_id)

# Oppdatere en DPS-avdeling
def update_dps_level_1(department_id, **kwargs):
    department = DPSLevel1.query.get(department_id)
    for key, value in kwargs.items():
        setattr(department, key, value)
    db.session.commit()

# Slette en DPS-avdeling
def delete_dps_level_1(department_id):
    department = DPSLevel1.query.get(department_id)
    db.session.delete(department)
    db.session.commit()

# Legge til en ny DPS-underavdeling
def add_dps_level_2(name, about, visitor_address, postal_address, general_info, practical_info, treatment_description, email, phone_number, department_id, method_ids, problem_area_ids, new_methods, new_problem_areas):
    # Opprette ny DPS Nivå 2 underavdeling
    new_subdepartment = DPSLevel2(
        name=name, 
        about=about, 
        visitor_address=visitor_address, 
        postal_address=postal_address, 
        general_info=general_info,
        practical_info=practical_info,
        treatment_description=treatment_description,
        email=email, 
        phone_number=phone_number,
        department_id=department_id
    )
    db.session.add(new_subdepartment)
    db.session.flush()  # For å få generert ID for new_subdepartment

    # Behandle eksisterende metoder
    for method_id in method_ids:
        # Sjekk om relasjonen allerede eksisterer
        existing_relation = db.session.query(dps_level_2_method).filter_by(
            dps_level_2_id=new_subdepartment.id, method_id=method_id).first()
        if not existing_relation:
            method = Method.query.get(method_id)
            if method:
                new_subdepartment.methods.append(method)

        # Behandle nye metoder
    if new_methods.strip():  # Sjekker om strengen ikke er tom
        for method_desc in new_methods.split(','):
            method_desc = method_desc.strip()
            if method_desc:  # Sjekker om hvert element i listen ikke er tom
                method = Method.query.filter_by(description=method_desc).first()
                if not method:
                    method = Method(description=method_desc)
                    db.session.add(method)
                if method not in new_subdepartment.methods:
                    new_subdepartment.methods.append(method)

    # Behandle eksisterende problemområder
    for problem_area_id in problem_area_ids:
        # Sjekk om relasjonen allerede eksisterer
        existing_relation = db.session.query(dps_level_2_problem_area).filter_by(
            dps_level_2_id=new_subdepartment.id, problem_area_id=problem_area_id).first()
        if not existing_relation:
            problem_area = ProblemArea.query.get(problem_area_id)
            if problem_area:
                new_subdepartment.problem_areas.append(problem_area)

        # Behandle nye problemområder
    if new_problem_areas.strip():  # Sjekker om strengen ikke er tom
        for problem_area_desc in new_problem_areas.split(','):
            problem_area_desc = problem_area_desc.strip()
            if problem_area_desc:  # Sjekker om hvert element i listen ikke er tom
                problem_area = ProblemArea.query.filter_by(description=problem_area_desc).first()
                if not problem_area:
                    problem_area = ProblemArea(description=problem_area_desc)
                    db.session.add(problem_area)
                if problem_area not in new_subdepartment.problem_areas:
                    new_subdepartment.problem_areas.append(problem_area)
        # Lagre endringene
        db.session.commit()



# Hente en DPS-underavdeling ved ID
def get_dps_level_2_by_id(subdepartment_id):
    return DPSLevel2.query.get(subdepartment_id)

# Oppdatere en DPS-underavdeling
def update_dps_level_2(subdepartment_id, **kwargs):
    subdepartment = DPSLevel2.query.get(subdepartment_id)
    if subdepartment:
        for key, value in kwargs.items():
            setattr(subdepartment, key, value)
        db.session.commit()

# Slette en DPS-underavdeling
def delete_dps_level_2(subdepartment_id):
    subdepartment = DPSLevel2.query.get(subdepartment_id)
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

def serialize_model(instance):
    """Konverterer SQLAlchemy-objekt til en ordbok."""
    return {c.name: getattr(instance, c.name) for c in instance.__table__.columns}

def get_database_data():
    """Henter data fra alle tabeller i databasen."""
    data = {}
    for mapper in db.Model.registry.mappers:
        cls = mapper.class_
        if hasattr(cls, '__tablename__'):
            records = cls.query.all()
            data[cls.__tablename__] = [serialize_model(record) for record in records]
    return data

@app.route('/export_database')
def export_database():
    data = get_database_data()
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)

if __name__ == "__main__":
    app.run(debug=True)
