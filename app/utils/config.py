import os
from dotenv import load_dotenv

load_dotenv() 

def get_env_variable(name):
    """Mendapatkan environment variable, atau raise error jika tidak ditemukan."""
    try:
        return os.environ[name]
    except KeyError:
        raise EnvironmentError(f"Gagal memuat variabel lingkungan wajib: {name}")

class Config:
    DB_USER = get_env_variable("DB_USER")
    DB_PASS = get_env_variable("DB_PASS")
    DB_HOST = get_env_variable("DB_HOST")
    DB_NAME = get_env_variable("DB_NAME")
    
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    SECRET_KEY = get_env_variable("SECRET_KEY") 
    
    MODEL_PATH = os.path.join(os.getcwd(), 'ml_models', 'model_waktu_tunggu_faskes.pkl')

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False
