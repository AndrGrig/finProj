from flask import Flask
import os

# def create_app():
#     app = Flask(__name__)
#     app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
#         'DATABASE_URL', 'mysql+pymysql://user:mysecurepassword@db_address/photoDB'
#     )
#     app.config['S3_BUCKET'] = os.getenv('S3_BUCKET', 'djans-photo-bucket')
#     # app.secret_key = os.getenv('FLASK_SECRET_KEY', 'your-dev-secret-key123456')
#     app.config['SECRET_KEY'] = os.urandom(24)

#     from .routes import main
#     app.register_blueprint(main)

#     return app


def create_app(testing=False):
    app = Flask(__name__)
    
    if testing:
        app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
            'DATABASE_URL', 'mysql+pymysql://root:mysecurepassword@localhost/photoDB_test'
        )
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
            'DATABASE_URL', 'mysql+pymysql://root:mysecurepassword@mysql/photoDB'
        )
    
    app.config['S3_BUCKET'] = os.getenv('S3_BUCKET', 'djans-photo-bucket')
    app.config['TESTING'] = testing
    app.config['SECRET_KEY'] = os.urandom(24)

    from .routes import main
    app.register_blueprint(main)

    return app