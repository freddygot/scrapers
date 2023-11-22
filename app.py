from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///psychologists.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialiser SQLAlchemy
db = SQLAlchemy(app)

# Importer alle modellene etter SQLAlchemy initialisering
import models

# Initialiser Flask-Migrate
migrate = Migrate(app, db)

# Importer ruter etter å ha initialisert alle utvidelser
import routes

# Denne blokken vil kjøre kun når filen kjøres direkte
if __name__ == "__main__":
    app.run(debug=True)