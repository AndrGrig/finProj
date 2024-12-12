import pymysql
import os

def get_db():
    return pymysql.connect(
        host=os.getenv('DB_HOST', 'db_address'),
        user=os.getenv('DB_USER', 'user'),
        password=os.getenv('DB_PASSWORD', 'password'),
        database=os.getenv('DB_NAME', 'db_name')
    )

def add_photo_record(photo_name):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("INSERT INTO photos (photo_name) VALUES (%s)", (photo_name,))
    db.commit()
    db.close()