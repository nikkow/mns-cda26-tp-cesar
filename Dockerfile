# Image de base à utiliser 
FROM python:3.14-slim

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier mon app à l'intérieur du conteneur
COPY . .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir gunicorn

# Exposer le port 8000
EXPOSE 8000

# Commande pour lancer l'application avec Gunicorn
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:8000", "app:app"]