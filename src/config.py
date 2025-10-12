import os
from dotenv import load_dotenv

load_dotenv()

# Configurações do Supabase
SUPABASE_URL = os.getenv('SUPABASE_URL', 'https://naawyjavknbewjgzcnxv.supabase.co')
SUPABASE_KEY = os.getenv('SUPABASE_KEY', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im5hYXd5amF2a25iZXdqZ3pjbnh2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3Mjc3MDY5NzIsImV4cCI6MjA0MzI4Mjk3Mn0.aDJGKhONKhCLLdGLZNjGhOJZKhONKhCLLdGLZNjGhOJ')

# Configurações do Flask
SECRET_KEY = os.getenv('SECRET_KEY', 'biblioteca-secret-key-2025')
DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
