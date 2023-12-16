from flask import Flask, jsonify, request, render_template, redirect, url_for, session, flash
import psycopg2
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import base64
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Konfigurasi koneksi database
db_config = {
    'dbname': 'dep',
    'user': 'postgres',
    'password': 'demauye0911',
    'host': 'localhost',
    'port': '5432'
}

def create_connection():
    conn = psycopg2.connect(**db_config)
    return conn, conn.cursor()

def close_connection(conn, cur):
    if cur is not None:
        cur.close()
    if conn is not None:
        conn.close()

# Fungsi untuk mengenkripsi password
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

# Fungsi untuk mendekripsi password
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

# (POST) Login
@app.route('/login', methods=['POST'])
def login():
    conn = None
    cur = None
    try:
        conn, cur = create_connection()

        username = request.form.get('username')
        password = request.form.get('password')

        cur.execute("SELECT * FROM pengguna WHERE username = %s", (username,))
        user = cur.fetchone()

        if user and decrypt_password(user[2], user[3]) == password:
            session['user_id'] = user[0]
            flash('Login berhasil!', 'success')
            return redirect(url_for('get_info'))
        else:
            flash('Login gagal. Periksa kembali username dan password Anda.', 'error')
            return redirect(url_for('login_page'))
    finally:
        close_connection(conn, cur)

#GET Login
@app.route('/login', methods=['GET'])
def login_page():
    return render_template('login.html')


# (POST)
@app.route('/info', methods=['POST'])
def create_info():
    conn = None
    cur = None
    try:
        conn, cur = create_connection()

        data = request.get_json()
        password = data.get('password')
        salt = os.urandom(16)  # Salt yang digunakan untuk kriptografi
        encrypted_password = encrypt_password(password, salt)

        cur.execute("INSERT INTO mahasiswa (nama, deskripsi, password, salt) VALUES (%s, %s, %s, %s)",
                    (data.get('nama'), data.get('deskripsi'), encrypted_password, salt))
        conn.commit()

        return jsonify({'message': 'Data created successfully'})
    finally:
        close_connection(conn, cur)

#GET
@app.route('/info', methods=['GET'])
def get_info():
    try:
        conn, cur = create_connection()
        cur.execute("SELECT * FROM mahasiswa")
        result = cur.fetchone()
        if result:
            data = {
                'id': result[0],
                'nama': result[1],
                'deskripsi': result[2],
                'password': decrypt_password(result[3], result[4])  # Mendekripsi password
            }
            return jsonify(data)
        else:
            return jsonify({'message': 'Data not found'})
    finally:
        close_connection(conn, cur)

#PUT
@app.route('/info', methods=['PUT'])
def update_info():
    try:
        conn, cur = create_connection()

        data = request.get_json()
        password = data.get('password')
        salt = os.urandom(16)  # Salt yang digunakan untuk kriptografi
        encrypted_password = encrypt_password(password, salt)

        cur.execute("UPDATE mahasiswa SET nama=%s, deskripsi=%s, password=%s, salt=%s WHERE id=%s",
                    (data.get('nama'), data.get('deskripsi'), encrypted_password, salt, data.get('id')))
        conn.commit()

        return jsonify({'message': 'Data updated successfully'})
    finally:
        close_connection(conn, cur)

#DELETE
@app.route('/info', methods=['DELETE'])
def delete_info():
    try:
        conn, cur = create_connection()
        data = request.get_json()
        cur.execute("DELETE FROM mahasiswa WHERE id=%s", (data.get('id'),))
        conn.commit()

        return jsonify({'message': 'Data deleted successfully'})
    finally:
        close_connection(conn, cur)

if __name__ == '__main__':
    app.run(debug=True)
