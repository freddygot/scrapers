from app import db

# Definisjon av modeller for psykisk helsevern
class Sektor(db.Model):
    __tablename__ = 'sektor'
    id = db.Column(db.Integer, primary_key=True)
    navn = db.Column(db.String(100), nullable=False)
    helseforetak = db.relationship('Helseforetak', backref='sektor', lazy=True)
    private_klinikker = db.relationship('PrivatKlinikk', backref='sektor', lazy=True)
    fastlegekontor = db.relationship('Fastlegekontor', backref='sektor', lazy=True)
    psykiatrisk_legevakt = db.relationship('PsykiatriskLegevakt', backref='sektor', lazy=True)
    frivillige_organisasjoner = db.relationship('FrivilligOrganisasjon', backref='sektor', lazy=True)

class Helseforetak(db.Model):
    __tablename__ = 'helseforetak'
    id = db.Column(db.Integer, primary_key=True)
    navn = db.Column(db.String(100), nullable=False)
    sektor_id = db.Column(db.Integer, db.ForeignKey('sektor.id'), nullable=False)
    dps = db.relationship('DistriktspsykiatriskSenter', backref='helseforetak', lazy=True)

class DistriktspsykiatriskSenter(db.Model):
    __tablename__ = 'distriktspsykiatrisk_senter'
    id = db.Column(db.Integer, primary_key=True)
    navn = db.Column(db.String(100), nullable=False)
    helseforetak_id = db.Column(db.Integer, db.ForeignKey('helseforetak.id'), nullable=False)
    avdelinger = db.relationship('Avdeling', backref='dps', lazy=True)

class DPSAvdeling(db.Model):
    __tablename__ = 'dps_avdeling'
    id = db.Column(db.Integer, primary_key=True)
    navn = db.Column(db.String(100), nullable=False)
    ventetid = db.Column(db.String(100))
    dps_id = db.Column(db.Integer, db.ForeignKey('distriktspsykiatrisk_senter.id'), nullable=False)
    underavdelinger = db.relationship('Underavdeling', backref='avdeling', lazy=True)

class DPSUnderavdeling(db.Model):
    __tablename__ = 'dps_underavdeling'
    id = db.Column(db.Integer, primary_key=True)
    navn = db.Column(db.String(100), nullable=False)
    ventetid = db.Column(db.String(100))
    avdeling_id = db.Column(db.Integer, db.ForeignKey('avdeling.id'), nullable=False)

class PrivatKlinikk(db.Model):
    __tablename__ = 'privat_klinikk'
    id = db.Column(db.Integer, primary_key=True)
    navn = db.Column(db.String(100), nullable=False)
    ventetid = db.Column(db.String(100))
    sektor_id = db.Column(db.Integer, db.ForeignKey('sektor.id'), nullable=False)
    psykologer = db.relationship('Psykolog', backref='klinikk', lazy=True)
    psykiatere = db.relationship('Psykiater', backref='klinikk', lazy=True)

class Psykolog(db.Model):
    __tablename__ = 'psykolog'
    id = db.Column(db.Integer, primary_key=True)
    navn = db.Column(db.String(100), nullable=False)
    tittel = db.Column(db.String(100))
    fødselsår = db.Column(db.Integer)
    profilbilde = db.Column(db.LargeBinary)
    Selvrapport = db.Column(db.String(600))
    ventetid = db.Column(db.String(100))
    klinikk_id = db.Column(db.Integer, db.ForeignKey('privat_klinikk.id'), nullable=True)
    metoder = db.relationship('Metode', secondary='psykolog_metode', back_populates='psykologer')
    arbeidsformer = db.relationship('Arbeidsform', secondary='psykolog_arbeidsform', back_populates='psykologer')
    problemomrader = db.relationship('Problemomrade', secondary='psykolog_problemomrade', back_populates='psykologer')
    tjenester = db.relationship('Tjeneste', secondary=psykolog_tjenester, back_populates='psykologer')
    anmeldelser = db.relationship('Anmeldelse', backref='psykolog', lazy=True)


class Psykiater(db.Model):
    __tablename__ = 'psykiater'
    id = db.Column(db.Integer, primary_key=True)
    navn = db.Column(db.String(100), nullable=False)
    tittel = db.Column(db.String(100))
    fødselsår = db.Column(db.Integer)
    profilbilde = db.Column(db.LargeBinary)
    Selvrapport = db.Column(db.String(600))
    ventetid = db.Column(db.String(100))
    klinikk_id = db.Column(db.Integer, db.ForeignKey('privat_klinikk.id'), nullable=True)
    metoder = db.relationship('Metode', secondary='psykiater_metode', back_populates='psykiatere')
    arbeidsformer = db.relationship('Arbeidsform', secondary='psykiater_arbeidsform', back_populates='psykiatere')
    problemomrader = db.relationship('Problemomrade', secondary='psykiater_problemomrade', back_populates='psykiatere')
    tjenester = db.relationship('Tjeneste', secondary=psykiater_tjenester, back_populates='psykiatere')
    anmeldelser = db.relationship('Anmeldelse', backref='psykiater', lazy=True)


class Fastlegekontor(db.Model):
    __tablename__ = 'fastlegekontor'
    id = db.Column(db.Integer, primary_key=True)
    navn = db.Column(db.String(100), nullable=False)
    ventetid = db.Column(db.String(100))
    sektor_id = db.Column(db.Integer, db.ForeignKey('sektor.id'), nullable=False)
    fastleger = db.relationship('Fastlege', backref='fastlegekontor', lazy=True)

class Fastlege(db.Model):
    __tablename__ = 'fastlege'
    id = db.Column(db.Integer, primary_key=True)
    navn = db.Column(db.String(100), nullable=False)
    tittel = db.Column(db.String(100))
    fødselsår = db.Column(db.Integer)
    profilbilde = db.Column(db.LargeBinary)
    Selvrapport = db.Column(db.String(600))
    ventetid = db.Column(db.String(100))
    kontor_id = db.Column(db.Integer, db.ForeignKey('fastlegekontor.id'), nullable=False)
    metoder = db.relationship('Metode', secondary='fastlege_metode', back_populates='fastleger')
    arbeidsformer = db.relationship('Arbeidsform', secondary='fastlege_arbeidsform', back_populates='fastleger')
    problemomrader = db.relationship('Problemomrade', secondary='fastlege_problemomrade', back_populates='fastleger')
    tjenester = db.relationship('Tjeneste', secondary=fastlege_tjenester, back_populates='fastleger')
    anmeldelser = db.relationship('Anmeldelse', backref='fastlege', lazy=True)


class PsykiatriskLegevakt(db.Model):
    __tablename__ = 'psykiatrisk_legevakt'
    id = db.Column(db.Integer, primary_key=True)
    navn = db.Column(db.String(100), nullable=False)
    sektor_id = db.Column(db.Integer, db.ForeignKey('sektor.id'), nullable=False)

class FrivilligOrganisasjon(db.Model):
    __tablename__ = 'frivillig_organisasjon'
    id = db.Column(db.Integer, primary_key=True)
    navn = db.Column(db.String(100), nullable=False)
    sektor_id = db.Column(db.Integer, db.ForeignKey('sektor.id'), nullable=False)


class Metode(db.Model):
    __tablename__ = 'metode'
    id = db.Column(db.Integer, primary_key=True)
    beskrivelse = db.Column(db.Text, nullable=False)
    psykologer = db.relationship('Psykolog', secondary='psykolog_metode', back_populates='metoder')
    psykiatere = db.relationship('Psykiater', secondary='psykiater_metode', back_populates='metoder')

class Arbeidsform(db.Model):
    __tablename__ = 'arbeidsform'
    id = db.Column(db.Integer, primary_key=True)
    beskrivelse = db.Column(db.Text, nullable=False)
    psykologer = db.relationship('Psykolog', secondary='psykolog_arbeidsform', back_populates='arbeidsformer')
    psykiatere = db.relationship('Psykiater', secondary='psykiater_arbeidsform', back_populates='arbeidsformer')

class Problemomrade(db.Model):
    __tablename__ = 'problemomrade'
    id = db.Column(db.Integer, primary_key=True)
    beskrivelse = db.Column(db.Text, nullable=False)
    psykologer = db.relationship('Psykolog', secondary='psykolog_problemomrade', back_populates='problemomrader')
    psykiatere = db.relationship('Psykiater', secondary='psykiater_problemomrade', back_populates='problemomrader')

class Tjeneste(db.Model):
    __tablename__ = 'tjeneste'
    id = db.Column(db.Integer, primary_key=True)
    beskrivelse = db.Column(db.String(100), nullable=False)
    varighet = db.Column(db.Integer, nullable=False)  # Varighet i minutter
    pris = db.Column(db.Float, nullable=False)  # Pris i din valuta

class Anmeldelse(db.Model):
    __tablename__ = 'anmeldelse'
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Float, nullable=False)  # Rating, for eksempel en skala fra 1 til 5
    kommentar = db.Column(db.Text, nullable=True)  # Anmeldelsestekst
    # Fremmednøkler til helsepersonell
    psykolog_id = db.Column(db.Integer, db.ForeignKey('psykolog.id'), nullable=True)
    psykiater_id = db.Column(db.Integer, db.ForeignKey('psykiater.id'), nullable=True)
    fastlege_id = db.Column(db.Integer, db.ForeignKey('fastlege.id'), nullable=True)

# Mange-til-mange assosiasjonstabeller
psykolog_metode = db.Table('psykolog_metode',
    db.Column('psykolog_id', db.Integer, db.ForeignKey('psykolog.id'), primary_key=True),
    db.Column('metode_id', db.Integer, db.ForeignKey('metode.id'), primary_key=True)
)

psykolog_arbeidsform = db.Table('psykolog_arbeidsform',
    db.Column('psykolog_id', db.Integer, db.ForeignKey('psykolog.id'), primary_key=True),
    db.Column('arbeidsform_id', db.Integer, db.ForeignKey('arbeidsform.id'), primary_key=True)
)

psykolog_problemomrade = db.Table('psykolog_problemomrade',
    db.Column('psykolog_id', db.Integer, db.ForeignKey('psykolog.id'), primary_key=True),
    db.Column('problemomrade_id', db.Integer, db.ForeignKey('problemomrade.id'), primary_key=True)
)

psykiater_metode = db.Table('psykiater_metode',
    db.Column('psykiater_id', db.Integer, db.ForeignKey('psykiater.id'), primary_key=True),
    db.Column('metode_id', db.Integer, db.ForeignKey('metode.id'), primary_key=True)
)

psykiater_arbeidsform = db.Table('psykiater_arbeidsform',
    db.Column('psykiater_id', db.Integer, db.ForeignKey('psykiater.id'), primary_key=True),
    db.Column('arbeidsform_id', db.Integer, db.ForeignKey('arbeidsform.id'), primary_key=True)
)

psykiater_problemomrade = db.Table('psykiater_problemomrade',
    db.Column('psykiater_id', db.Integer, db.ForeignKey('psykiater.id'), primary_key=True),
    db.Column('problemomrade_id', db.Integer, db.ForeignKey('problemomrade.id'), primary_key=True)
)

fastlege_metode = db.Table('fastlege_metode',
    db.Column('fastlege_id', db.Integer, db.ForeignKey('fastlege.id'), primary_key=True),
    db.Column('metode_id', db.Integer, db.ForeignKey('metode.id'), primary_key=True)
)

fastlege_arbeidsform = db.Table('fastlege_arbeidsform',
    db.Column('fastlege_id', db.Integer, db.ForeignKey('fastlege.id'), primary_key=True),
    db.Column('arbeidsform_id', db.Integer, db.ForeignKey('arbeidsform.id'), primary_key=True)
)

fastlege_problemomrade = db.Table('fastlege_problemomrade',
    db.Column('fastlege_id', db.Integer, db.ForeignKey('fastlege.id'), primary_key=True),
    db.Column('problemomrade_id', db.Integer, db.ForeignKey('problemomrade.id'), primary_key=True)
)

psykolog_tjenester = db.Table('psykolog_tjenester',
    db.Column('psykolog_id', db.Integer, db.ForeignKey('psykolog.id'), primary_key=True),
    db.Column('tjeneste_id', db.Integer, db.ForeignKey('tjeneste.id'), primary_key=True)
)

psykiater_tjenester = db.Table('psykiater_tjenester',
    db.Column('psykiater_id', db.Integer, db.ForeignKey('psykiater.id'), primary_key=True),
    db.Column('tjeneste_id', db.Integer, db.ForeignKey('tjeneste.id'), primary_key=True)
)

fastlege_tjenester = db.Table('fastlege_tjenester',
    db.Column('fastlege_id', db.Integer, db.ForeignKey('fastlege.id'), primary_key=True),
    db.Column('tjeneste_id', db.Integer, db.ForeignKey('tjeneste.id'), primary_key=True)
)



# Husk å inkludere alle nødvendige felt og relasjoner for de andre modellene

