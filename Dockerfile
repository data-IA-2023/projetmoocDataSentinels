# Utiliser une image de base de Python
FROM python:3.9

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers de l'application dans le conteneur
COPY . .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Exposer le port sur lequel l'application fonctionne
EXPOSE 8501

# Commande pour lancer l'application
CMD ["streamlit", "run", "streamlitGrade.py", "--server.port=8501", "--server.address=0.0.0.0"]
