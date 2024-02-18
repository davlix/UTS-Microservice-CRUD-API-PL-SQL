
# Microservice dengan Fitur Logging

Aplikasi ini adalah mikroservis berbasis Flask dengan integrasi database PostgreSQL. Aplikasi menyediakan fungsionalitas login pengguna, serta operasi CRUD (Create, Read, Update, Delete) untuk informasi mahasiswa.

## Fitur

- Otentikasi pengguna dengan penyimpanan sandi terenkripsi
- Operasi CRUD informasi mahasiswa
- Fitur logging untuk melacak peristiwa penting

## Memulai

### Prasyarat

- Python 3.x
- Flask
- psycopg2
- cryptography

### Instalasi

1. Clone repositori:

   ```bash
   git clone https://github.com/davlix/UTS-Microservice-CRUD-API-PL-SQL.git
   cd UTS-Microservice-CRUD-API-PL-SQL
   ```

2. Instal dependensi:

   ```bash
   pip install -r requirements.txt
   ```

3. Jalankan aplikasi:

   ```bash
   python app.py
   ```

   Aplikasi dapat diakses di `http://127.0.0.1:5000/`.

## Penggunaan

### Logging

Aplikasi menggunakan modul `logging` Python untuk mencatat peristiwa penting. File log dinamai `app.log` dan berisi informasi seperti login berhasil, percobaan login gagal, dan kesalahan pada berbagai fungsi.

### Contoh Entri Log

- Login Berhasil:

  ```
  2024-02-17 12:30:45 - INFO - Pengguna john_cena berhasil login.
  ```

- Login Gagal:

  ```
  2024-02-17 12:35:20 - WARNING - Pengguna jane_cena gagal login.
  ```

- Kesalahan pada Fungsi:

  ```
  2024-02-17 13:00:10 - ERROR - Kesalahan pada fungsi update_info: division by zero.
  ```

### Format Log

Entri log mengikuti format:

```
%(asctime)s - %(levelname)s - %(message)s
```

- `%(asctime)s`: Timestamp dari entri log.
- `%(levelname)s`: Level log (INFO, WARNING, ERROR, dll.).
- `%(message)s`: Pesan log yang berisi informasi relevan.

