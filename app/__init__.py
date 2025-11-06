from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import atexit
from apscheduler.schedulers.background import BackgroundScheduler

from app.utils.config import Config
# from app.routes import blueprint as routes_blueprint 
from app.extension import db, migrate 
from flask_migrate import Migrate

# db = SQLAlchemy() 

def create_app(config_class=Config):
    app = Flask(__name__)
    
    app.config.from_object(config_class)

    db.init_app(app)
    Migrate(app, db) 

    from app.routes import blueprint
    app.register_blueprint(blueprint)

    from app.services.ml_service import train_and_save_model 
    
    scheduler = BackgroundScheduler()
    
    scheduler.add_job(
        func=train_and_save_model, 
        trigger="cron", 
        day_of_week='sun', 
        hour=2, 
        minute=0, 
        id='ml_retrain',
        name='ML Model Retraining Job'
    )
    
    scheduler.start()
    
    atexit.register(lambda: scheduler.shutdown())
    

    return app
