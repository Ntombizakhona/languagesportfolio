# backend/config.py
import os

class Config:
    """Application configuration from environment variables."""
    
    # Database configuration
    DATABASE_HOST = os.getenv('DATABASE_HOST', 'localhost')
    DATABASE_PORT = int(os.getenv('DATABASE_PORT', 3306))
    DATABASE_NAME = os.getenv('DATABASE_NAME', 'portfolio_db')
    DATABASE_USER = os.getenv('DATABASE_USER', 'portfolio_user')
    DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD', '')
    
    # Flask configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'