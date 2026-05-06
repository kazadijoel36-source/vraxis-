import os

class Config:
    # 1. Database Logic
    # Allows buyer to switch to PostgreSQL or change the SQLite filename easily
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///instance/vraxis.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 2. Expiration Logic (The "Ember" Timer)
    # Defaulting to 24 hours, but easily changeable
    DEFAULT_EXPIRY_HOURS = 24
    
    # 3. Security
    # Essential for AdSense and session security
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'potch-node-secret-key-2026'

    # 4. Global Branding
    NODE_NAME = "ZA-01 POTCHEFSTROOM NODE"
    VERSION = "1.0.4"