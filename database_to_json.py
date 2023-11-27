from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from app import db  # Erstatt 'your_model_file' med navnet på filen der 'db' er definert

app = Flask(__name__)
# Konfigurer og initialiser appen og databasen her, hvis det ikke allerede er gjort

def serialize_model(instance):
    """Konverterer SQLAlchemy-objekt til en ordbok."""
    return {c.name: getattr(instance, c.name) for c in instance.__table__.columns}

def get_database_data():
    """Henter data fra alle tabeller i databasen."""
    data = {}
    for cls in db.Model._decl_class_registry.values():
        if isinstance(cls, type) and issubclass(cls, db.Model) and hasattr(cls, '__tablename__'):
            records = cls.query.all()
            data[cls.__tablename__] = [serialize_model(record) for record in records]
    return data

@app.route('/export_database')
def export_database():
    data = get_database_data()
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
