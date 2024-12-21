import pymysql
import os

# def get_db():
#     return pymysql.connect(
#         host=os.getenv('DB_HOST', 'db_address'),
#         user=os.getenv('DB_USER', 'user'),
#         password=os.getenv('DB_PASSWORD', 'mysecurepassword'),
#         database=os.getenv('DB_NAME', 'photoDB')
#     )

def get_db():
    host = 'localhost' if os.getenv('FLASK_ENV') == 'testing' else os.getenv('DB_HOST', 'db_address')
    return pymysql.connect(
        host=host,
        user=os.getenv('DB_USER', 'root'),
        password=os.getenv('DB_PASSWORD', 'mysecurepassword'),
        database=os.getenv('DB_NAME', 'photoDB_test' if os.getenv('FLASK_ENV') == 'testing' else 'photoDB')
    )

def add_photo_record(photo_name):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("INSERT INTO photos (photo_name) VALUES (%s)", (photo_name,))
    db.commit()
    db.close()