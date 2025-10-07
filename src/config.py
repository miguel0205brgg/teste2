import os

# Configurações do Flask
SECRET_KEY = os.getenv("SECRET_KEY", "biblioteca-secret-key-2025")
DEBUG = os.getenv("DEBUG", "True").lower() == "true"

