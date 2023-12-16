Berikut adalah versi dokumentasi dalam format Markdown (README.md):

```markdown
# Dokumentasi Aplikasi Flask CRUD dengan Enkripsi Password AES-256

## Instalasi

### 1. 

```bash
python -m venv venv
```

Kemudian aktifkan:

- **Windows:**
  ```bash
  venv\Scripts\activate
  ```

- **Linux atau macOS:**
  ```bash
  source venv/bin/activate
  ```

### 2. Instalasi Dependencies

```bash
pip install Flask psycopg2 cryptography
```

- `Flask`: Framework web untuk Python.
- `psycopg2`: Driver PostgreSQL untuk Python.
- `cryptography`: Pustaka untuk operasi kriptografi, digunakan untuk enkripsi dan dekripsi AES-256.

## Konfigurasi Database

1. Pastikan PostgreSQL telah terinstall dan berjalan.
2. Buat database baru dengan nama "dep"
3. Sesuaikan konfigurasi koneksi database di file aplikasi Flask (`app.py`) dengan informasi database.

```python
db_config = {
    'dbname': 'dep',
    'user': 'postgres',
    'password': 'demauye0911',
    'host': 'localhost',
    'port': '5432'
}
```

## Menjalankan Aplikasi

1. Jalankan aplikasi Flask dengan perintah:

```bash
python app.py
```

Aplikasi akan berjalan di `http://127.0.0.1:5000/` atau URL lain yang ditampilkan di terminal.

## Penggunaan API Endpoints

### 1. Menambah Data Mahasiswa (POST)

- Endpoint: `http://127.0.0.1:5000/info`
- Metode: `POST`
- Contoh Body JSON:

```json
{
    "nama": "John Doe",
    "deskripsi": "Mahasiswa baru",
    "password": "secure_password"
}
```

### 2. Mendapatkan Data Mahasiswa (GET)

- Endpoint: `http://127.0.0.1:5000/info`
- Metode: `GET`
- Menampilkan data mahasiswa pertama dari database.

### 3. Memperbarui Data Mahasiswa (PUT)

- Endpoint: `http://127.0.0.1:5000/info`
- Metode: `PUT`
- Contoh Body JSON untuk memperbarui data:

```json
{
    "id": 1,
    "nama": "John Doe",
    "deskripsi": "Mahasiswa lama",
    "password": "new_secure_password"
}
```

### 4. Menghapus Data Mahasiswa (DELETE)

- Endpoint: `http://127.0.0.1:5000/info`
- Metode: `DELETE`
- Contoh Body JSON untuk menghapus data:

```json
{
    "id": 1
}
```
