# routes.py
from flask import render_template
from app import app
# Importer andre nødvendige moduler og funksjoner

@app.route('/')
def index():
    # Din kode for ruten
    return render_template('index.html')
