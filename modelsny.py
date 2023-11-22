from app import db





class HelseInstitusjon(db.Model):
    __tablename__ = 'helse_institusjon'
    id = db.Column(db.Integer, primary_key=True)
    navn = db.Column(db.String(100), nullable=False)
    adresse = db.Column(db.String(200))
    postal_code = db.Column(db.Integer)
    by = db.Column(db.String(200))
    profilbilde = db.Column(db.String(200))
    telefonnummer = db.Column(db.String(20))
    epost = db.Column(db.String(100))
    hjemmeside = db.Column(db.String(100))
    tjenestekategori_id = db.Column(db.Integer, db.ForeignKey('tjeneste_kategori.id'), nullable=False)
    helse_personell = db.relationship('HelsePersonell', backref='helse_institusjon', lazy=True)

class HelsePersonell(db.Model):
    __tablename__ = 'helse_personell'
    institusjon_id = db.Column(db.Integer, db.ForeignKey('helse_institusjon.id'), nullable=False)
    tjeneste_tilbud = db.relationship('TjenesteTilbud', backref='helse_personell', lazy=True)
    anmeldelser = db.relationship('Anmeldelse', backref='helse_personell', lazy=True)
    

class Problemområde(db.Model):
    __tablename__ = 'problemområde'
    id = db.Column(db.Integer, primary_key=True)
    navn = db.Column(db.String(100), nullable=False)

class Behandlingsmetodikk(db.Model):
    __tablename__ = 'behandlingsmetodikk'
    id = db.Column(db.Integer, primary_key=True)
    navn = db.Column(db.String(100), nullable=False)

class Format(db.Model):
    __tablename__ = 'format'
    id = db.Column(db.Integer, primary_key=True)
    navn = db.Column(db.String(100), nullable=False)

class TjenesteTilbud(db.Model):
    __tablename__ = 'tjeneste_tilbud'
    id = db.Column(db.Integer, primary_key=True)
    pris = db.Column(db.Float)
    ventetid = db.Column(db.String(100))
    personell_id = db.Column(db.Integer, db.ForeignKey('helse_personell.id'), nullable=False)
    problemområder = db.relationship('Problemområde', secondary='tjenestetilbud_problemområde')
    behandlingsmetodikker = db.relationship('Behandlingsmetodikk', secondary='tjenestetilbud_behandlingsmetodikk')
    formater = db.relationship('Format', secondary='tjenestetilbud_format')

class TjenesteTilbudProblemområde(db.Model):
    __tablename__ = 'tjenestetilbud_problemområde'
    tjenestetilbud_id = db.Column(db.Integer, db.ForeignKey('tjeneste_tilbud.id'), primary_key=True)
    problemområde_id = db.Column(db.Integer, db.ForeignKey('problemområde.id'), primary_key=True)

class TjenesteTilbudBehandlingsmetodikk(db.Model):
    __tablename__ = 'tjenestetilbud_behandlingsmetodikk'
    tjenestetilbud_id = db.Column(db.Integer, db.ForeignKey('tjeneste_tilbud.id'), primary_key=True)
    behandlingsmetodikk_id = db.Column(db.Integer, db.ForeignKey('behandlingsmetodikk.id'), primary_key=True)

class TjenesteTilbudFormat(db.Model):
    __tablename__ = 'tjenestetilbud_format'
    tjenestetilbud_id = db.Column(db.Integer, db.ForeignKey('tjeneste_tilbud.id'), primary_key=True)
    format_id = db.Column(db.Integer, db.ForeignKey('format.id'), primary_key=True)
 --------------------------------------------

class Land(db.Model):
    __tablename__ = 'Land'
    id = db.Column(db.Integer, primary_key=True)
    navn = db.Column(db.String(100), nullable=False)

class Kommune(db.Model):
    __tablename__ = 'problemområde'
    id = db.Column(db.Integer, primary_key=True)
    navn = db.Column(db.String(100), nullable=False)

# Definisjon av modeller
class Sektor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    navn = db.Column(db.String(100), nullable=False)
    private_klinikker = db.relationship('PrivateKlinikk', backref='sektor', lazy=True)
    fastlegekontor = db.relationship('Fastlegekontor', backref='sektor', lazy=True)
    psykiatrisk_legevakt = db.relationship('PsykiatriskLegevakt', backref='sektor', lazy=True)
    frivillige_organisasjoner = db.relationship('FrivilligOrganisasjon', backref='sektor', lazy=True)

class Helseforetak(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    navn = db.Column(db.String(100), nullable=False)
    sektor_id = db.Column(db.Integer, db.ForeignKey('sektor.id'), nullable=False)
    dps = db.relationship('DistriktspsykiatriskSenter', backref='helseforetak', lazy=True)

class DistriktspsykiatriskSenter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    navn = db.Column(db.String(100), nullable=False)
    helseforetak_id = db.Column(db.Integer, db.ForeignKey('helseforetak.id'), nullable=False)
    avdelinger = db.relationship('Avdeling', backref='dps', lazy=True)
    helsepersonell = db.relationship('Helsepersonell', backref='dps', lazy=True)

class Avdeling(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    navn = db.Column(db.String(100), nullable=False)
    dps_id = db.Column(db.Integer, db.ForeignKey('distriktspsykiatrisk_senter.id'), nullable=False)
    underavdelinger = db.relationship('Underavdeling', backref='avdeling', lazy=True)

class Underavdeling(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    navn = db.Column(db.String(100), nullable=False)
    avdeling_id = db.Column(db.Integer, db.ForeignKey('avdeling.id'), nullable=False)

class Helsepersonell(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    navn = db.Column(db.String(100), nullable=False)
    yrke = db.Column(db.String(50), nullable=False)
    dps_id = db.Column(db.Integer, db.ForeignKey('distriktspsykiatrisk_senter.id'), nullable=True)

class PrivatKlinikk(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    navn = db.Column(db.String(100), nullable=False)
    sektor_id = db.Column(db.Integer, db.ForeignKey('sektor.id'), nullable=False)
    psykologer = db.relationship('Psykolog', backref='klinikk', lazy=True)
    psykiatere = db.relationship('Psykiater', backref='klinikk', lazy=True)

class Psykolog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    navn = db.Column(db.String(100), nullable=False)
    kjønn = db.Column(db.String(100))
    fødselsår = db.Column(db.Integer)
    Legelistelink = db.Column(db.String(100))
    Dinpsykologlink = db.Column(db.String(100))
    Selvrapport = db.Column(db.String(600))
    telefonnummer = db.Column(db.Integer)
    epost = db.Column(db.String(100))
    profilbilde = db.Column(db.LargeBinary)
    klinikk_id = db.Column(db.Integer, db.ForeignKey('privat_klinikk.id'), nullable=True)
    anmeldelser = db.relationship('Anmeldelse', backref='psykolog', lazy=True)
    problemomrader = db.relationship('PsykologProblemomrade', backref='psykolog', lazy='dynamic')
    formater = db.relationship('PsykologFormat', backref='psykolog', lazy='dynamic')
    arbeidsmetodikker = db.relationship('PsykologMetodikk', backref='psykolog', lazy='dynamic')


class Psykiater(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    navn = db.Column(db.String(100), nullable=False)
    kjønn = db.Column(db.String(100))
    fødselsår = db.Column(db.Integer)
    Legelistelink = db.Column(db.String(100))
    Dinpsykologlink = db.Column(db.String(100))
    Selvrapport = db.Column(db.String(600))
    telefonnummer = db.Column(db.Integer)
    epost = db.Column(db.String(100))
    profilbilde = db.Column(db.LargeBinary)
    klinikk_id = db.Column(db.Integer, db.ForeignKey('privat_klinikk.id'), nullable=True)
    anmeldelser = db.relationship('Anmeldelse', backref='psykiater', lazy=True)

class Fastlegekontor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    navn = db.Column(db.String(100), nullable=False)
    sektor_id = db.Column(db.Integer, db.ForeignKey('sektor.id'), nullable=False)
    fastleger = db.relationship('Fastlege', backref='fastlegekontor', lazy=True)

class Fastlege(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    navn = db.Column(db.String(100), nullable=False)
    kontor_id = db.Column(db.Integer, db.ForeignKey('fastlegekontor.id'), nullable=False)
    anmeldelser = db.relationship('Anmeldelse', backref='fastlege', lazy=True)

class PsykiatriskLegevakt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    navn = db.Column(db.String(100), nullable=False)
    sektor_id = db.Column(db.Integer, db.ForeignKey('sektor.id'), nullable=False)

class FrivilligOrganisasjon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    navn = db.Column(db.String(100), nullable=False)
    sektor_id = db.Column(db.Integer, db.ForeignKey('sektor.id'), nullable=False)

class Anmeldelse(db.Model):
    __tablename__ = 'anmeldelse'
    id = db.Column(db.Integer, primary_key=True)
    kommentar = db.Column(db.Text)
    rating = db.Column(db.Integer)
    psykolog_id = db.Column(db.Integer, db.ForeignKey('psykolog.id'), nullable=False)
    psykiater_id = db.Column(db.Integer, db.ForeignKey('psykiater.id'), nullable=False)
    fastlege_id = db.Column(db.Integer, db.ForeignKey('fastlege.id'), nullable=False)

class Problemomrade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    beskrivelse = db.Column(db.Text, nullable=False)
    psykologer = db.relationship('PsykologProblemomrade', backref='problemomrade', lazy='dynamic')
    psykiatere = db.relationship('PsykiaterProblemomrade', backref='problemomrade', lazy='dynamic')

class Format(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    beskrivelse = db.Column(db.Text, nullable=False)
    psykologer = db.relationship('PsykologFormat', backref='format', lazy='dynamic')
    psykiatere = db.relationship('PsykiaterFormat', backref='format', lazy='dynamic')

class Arbeidsmetodikk(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    beskrivelse = db.Column(db.Text, nullable=False)
    psykologer = db.relationship('PsykologMetodikk', backref='arbeidsmetodikk', lazy='dynamic')
    psykiatere = db.relationship('PsykiaterMetodikk', backref='arbeidsmetodikk', lazy='dynamic')






@app.before_first_request
def create_tables():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
