# Utiliser une image de base de Python
FROM python:3.10.5-slim


# Définir le répertoire de travail
WORKDIR /app

# Copy requirements.txt and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy the rest of the application code
COPY . .

ENV MONGO_URL='51.11.209.4:27017'
ENV POSTGRES_USER='sentinelsdata'
ENV POSTGRES_PASSWORD='Sentinelsdata37'
ENV POSTGRES_HOST='51.11.209.4'
ENV POSTGRES_PORT='5432'
ENV POSTGRES_DB='postgres'

# Exposer le port sur lequel l'application fonctionne
EXPOSE 8501

# Commande pour lancer l'application
CMD ["streamlit", "run", "main.py", "--server.port", "8501", "--server.address", "0.0.0.0"]
