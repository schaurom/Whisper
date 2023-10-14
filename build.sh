#!/bin/bash

# Aktualisiere pip und installiere Abhängigkeiten
pip install --upgrade pip
pip install -r requirements.txt

# Führe Datenbankmigrationen durch (falls zutreffend)
# python manage.py db upgrade

# Führe Tests aus (falls zutreffend)
# pytest

# Sammle statische Dateien (falls deine App statische Dateien hat)
# python manage.py collectstatic

# Starte die Flask-Anwendung (verwende den richtigen Befehl für deine Anwendung)
# python meincode.py oder gunicorn meincode:app
# python app.py
gunicorn app:app

# Du kannst auch hier spezifische Umgebungsvariablen oder Konfigurationen setzen
# export FLASK_ENV=production
# export FLASK_APP=meincode.py

# Führe die Anwendung aus
# python app.py