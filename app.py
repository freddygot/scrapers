from flask import Flask
import render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Importer andre nødvendige moduler og funksjoner

@app.route('/')
def index():
    return render_template('index.html')

# ...resten av dine ruter...


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///psychologists.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

import models

if __name__ == "__main__":
    import routes  # Importer ruter her
    app.run(debug=True)