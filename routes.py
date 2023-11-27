# routes.py
from flask import render_template
from app import app
# Importer andre nødvendige moduler og funksjoner

@app.route('/')
def index():
    # Din kode for ruten
    return render_template('index.html')

@app.route('/add_sector', methods=['POST'])
def add_sector_route():
    # Behandle innkommende data og kall add_sector
    return "Sektor lagt til"

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


@app.route('/add_regional_health_trust', methods=['POST'])
def add_regional_health_trust_route():
    # Hent og prosesser data fra request her
    return "Regionalt helseforetak lagt til"

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

@app.route('/add_health_trust', methods=['POST'])
def add_health_trust_route():
    # Hent og prosesser data fra request her
    return "Helseforetak lagt til"

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


@app.route('/add_dps', methods=['POST'])
def add_dps_route():
    # Hent og prosesser data fra request her
    return "DPS lagt til"

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


@app.route('/add_dps_department', methods=['POST'])
def add_dps_department_route():
    # Hent og prosesser data fra request her
    return "DPS-avdeling lagt til"

@app.route('/dps_department/<int:department_id>', methods=['GET'])
def get_dps_department_route(department_id):
    department = get_dps_department_by_id(department_id)
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

@app.route('/dps_department/<int:department_id>', methods=['PUT'])
def update_dps_department_route(department_id):
    data = request.json
    name = data.get('name')
    about = data.get('about')
    visitor_address = data.get('visitor_address')
    postal_address = data.get('postal_address')
    dps_id = data.get('dps_id')

    if not all([name, about, visitor_address, postal_address, dps_id]):
        return "Mangler nødvendig felt", 400

    try:
        update_dps_department(department_id, name, about, visitor_address, postal_address, dps_id)
        return f"DPS-avdeling med ID {department_id} har blitt oppdatert."
    except Exception as e:
        return str(e), 500

@app.route('/dps_department/<int:department_id>', methods=['DELETE'])
def delete_dps_department_route(department_id):
    try:
        delete_dps_department(department_id)
        return f"DPS-avdeling med ID {department_id} har blitt slettet."
    except Exception as e:
        return str(e), 500

@app.route('/add_dps_subdepartment', methods=['POST'])
def add_dps_subdepartment_route():
    # Hent og prosesser data fra request her
    return "DPS-underavdeling lagt til"

@app.route('/dps_subdepartment/<int:subdepartment_id>', methods=['GET'])
def get_dps_subdepartment_route(subdepartment_id):
    subdepartment = get_dps_subdepartment_by_id(subdepartment_id)
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

@app.route('/dps_subdepartment/<int:subdepartment_id>', methods=['PUT'])
def update_dps_subdepartment_route(subdepartment_id):
    data = request.json
    name = data.get('name')
    about = data.get('about')
    visitor_address = data.get('visitor_address')
    postal_address = data.get('postal_address')
    department_id = data.get('department_id')

    if not all([name, about, visitor_address, postal_address, department_id]):
        return "Mangler nødvendig felt", 400

    try:
        update_dps_subdepartment(subdepartment_id, name, about, visitor_address, postal_address, department_id)
        return f"DPS-underavdeling med ID {subdepartment_id} har blitt oppdatert."
    except Exception as e:
        return str(e), 500

@app.route('/dps_subdepartment/<int:subdepartment_id>', methods=['DELETE'])
def delete_dps_subdepartment_route(subdepartment_id):
    try:
        delete_dps_subdepartment(subdepartment_id)
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

# Lignende ruter kan lages for GET, PUT, DELETE osv.



