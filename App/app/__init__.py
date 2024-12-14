from flask import Flask
import os

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
        'DATABASE_URL', 'mysql+pymysql://user:mysecurepassword@db_address/photoDB'
    )
    app.config['S3_BUCKET'] = os.getenv('S3_BUCKET', 'djans-photos-bucket')

    from .routes import main
    app.register_blueprint(main)

    return app