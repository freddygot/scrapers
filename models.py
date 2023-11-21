from app import db

#Førstlinje, andrelinje og tredjelinje
class TjenesteNiva(db.Model):
    __tablename__ = 'tjeneste_niva'
    id = db.Column(db.Integer, primary_key=True)
    navn = db.Column(db.String(50), nullable=False)
    sektorer = db.relationship('Sektor', backref='tjeneste_niva', lazy=True)

#Privat, statlig og kommunal sektor
class Sektor(db.Model):
    __tablename__ = 'sektor'
    id = db.Column(db.Integer, primary_key=True)
    navn = db.Column(db.String(50), nullable=False)
    tjeneste_niva_id = db.Column(db.Integer, db.ForeignKey('tjeneste_niva.id'), nullable=False)
    tjeneste_kategorier = db.relationship('TjenesteKategori', backref='sektor', lazy=True)

#Privat virksomhet, Distriktspsykiatrisk sykehus (DPS), Fastlegene, Generelle kommunale helsetjenester, 
class TjenesteKategori(db.Model):
    __tablename__ = 'tjeneste_kategori'
    id = db.Column(db.Integer, primary_key=True)
    navn = db.Column(db.String(100), nullable=False)
    sektor_id = db.Column(db.Integer, db.ForeignKey('sektor.id'), nullable=False)
    helse_institusjoner = db.relationship('HelseInstitusjon', backref='tjeneste_kategori', lazy=True)


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
    id = db.Column(db.Integer, primary_key=True)
    navn = db.Column(db.String(100), nullable=False)
    tittel = db.Column(db.String(100))
    kjønn = db.Column(db.String(100))
    fødselsår = db.Column(db.Integer)
    Legelistelink = db.Column(db.String(100))
    Dinpsykologlink = db.Column(db.String(100))
    Selvrapport = db.Column(db.String(600))
    telefonnummer = db.Column(db.Integer)
    epost = db.Column(db.String(100))
    profilbilde = db.Column(db.LargeBinary)
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


class Anmeldelse(db.Model):
    __tablename__ = 'anmeldelse'
    id = db.Column(db.Integer, primary_key=True)
    kommentar = db.Column(db.Text)
    rating = db.Column(db.Integer)
    personell_id = db.Column(db.Integer, db.ForeignKey('helse_personell.id'), nullable=False)