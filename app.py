from flask import Flask, jsonify, request, render_template, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event
from sqlalchemy.engine import Engine
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import base64
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:demauye0911@localhost:5432/dep'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'
db = SQLAlchemy(app)

class Mahasiswa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(255))
    deskripsi = db.Column(db.String(255))
    password = db.Column(db.LargeBinary)
    salt = db.Column(db.LargeBinary)

class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_type = db.Column(db.String(50))
    event_description = db.Column(db.Text)
    event_timestamp = db.Column(db.TIMESTAMP, server_default=db.func.now())

def create_connection():
    conn = psycopg2.connect(**db_config)
    return conn, conn.cursor()

def close_connection(conn, cur):
    if cur is not None:
        cur.close()
    if conn is not None:
        conn.close()

def encrypt_password(password, salt):
    kdf = PBKDF2HMAC(
        algorithm=algorithms.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    cipher = Cipher(algorithms.AES(key), modes.CFB(os.urandom(16)), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted_password = encryptor.update(password.encode()) + encryptor.finalize()
    return encrypted_password

def decrypt_password(encrypted_password, salt):
    kdf = PBKDF2HMAC(
        algorithm=algorithms.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(user[1].encode()))
    cipher = Cipher(algorithms.AES(key), modes.CFB(os.urandom(16)), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_password = decryptor.update(encrypted_password) + decryptor.finalize()
    return decrypted_password.decode()

def log_event(mapper, connection, target):
    if not target.id:
        event_type = 'INSERT'
        event_description = f"{target.__tablename__} row inserted"
    else:
        event_type = 'UPDATE' if target in connection.dirty else 'DELETE'
        event_description = f"{target.__tablename__} row {event_type.lower()}"

    log_entry = Log(event_type=event_type, event_description=event_description)
    db.session.add(log_entry)
    db.session.commit()

event.listen(Mahasiswa, 'after_insert', log_event)
event.listen(Mahasiswa, 'after_update', log_event)
event.listen(Mahasiswa, 'after_delete', log_event)

@app.route('/login', methods=['POST'])
def login():
    # ...

@app.route('/login', methods=['GET'])
def login_page():
    return render_template('login.html')

@app.route('/info', methods=['POST'])
def create_info():
    # ...

@app.route('/info', methods=['GET'])
def get_info():
    try:
        mahasiswa = Mahasiswa.query.first()
        if mahasiswa:
            data = {
                'id': mahasiswa.id,
                'nama': mahasiswa.nama,
                'deskripsi': mahasiswa.deskripsi,
                'password': decrypt_password(mahasiswa.password, mahasiswa.salt)
            }
            return jsonify(data)
        else:
            return jsonify({'message': 'Data not found'})
    finally:
        close_connection(conn, cur)

@app.route('/info', methods=['PUT'])
def update_info():
    # ...

@app.route('/info', methods=['DELETE'])
def delete_info():
    # ...

@app.route('/log', methods=['GET'])
def get_logs():
    logs = Log.query.all()
    log_list = [{'event_type': log.event_type,
                 'event_description': log.event_description,
                 'event_timestamp': log.event_timestamp} for log in logs]
    return jsonify({'logs': log_list})

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)