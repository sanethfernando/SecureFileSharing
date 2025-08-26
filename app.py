from flask import Flask, request, render_template, send_file, redirect, url_for, flash
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import os, sqlite3, base64
from datetime import datetime
from io import BytesIO
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()
AES_KEY_B64 = os.environ.get("AES_KEY")
KEY = base64.b64decode(AES_KEY_B64)  # AES key for encryption/decryption

app = Flask(__name__)
app.secret_key = get_random_bytes(16)

UPLOAD_FOLDER = "uploads"
DB_PATH = "files.db"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# --- Database helpers ---
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT,
            uploaded_at TEXT
        )
    """)
    conn.commit()
    conn.close()

def add_file_record(filename):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO files (filename, uploaded_at) VALUES (?, ?)",
              (filename, datetime.utcnow().isoformat()))
    conn.commit()
    conn.close()

def get_all_files():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT filename, uploaded_at FROM files ORDER BY uploaded_at DESC")
    rows = c.fetchall()
    conn.close()
    return rows

# --- Encryption helpers ---
def encrypt_file(file_data):
    cipher = AES.new(KEY, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(file_data)
    return cipher.nonce, ciphertext, tag

def decrypt_file(nonce, ciphertext, tag):
    cipher = AES.new(KEY, AES.MODE_EAX, nonce=nonce)
    return cipher.decrypt_and_verify(ciphertext, tag)

# --- Routes ---
@app.route("/")
def index():
    init_db()
    files = get_all_files()
    return render_template("index.html", files=files)

@app.route("/upload", methods=["POST"])
def upload():
    if "file" not in request.files:
        flash("No file selected", "error")
        return redirect(url_for("index"))
    file = request.files["file"]
    if file.filename == "":
        flash("Empty filename", "error")
        return redirect(url_for("index"))

    data = file.read()
    nonce, ciphertext, tag = encrypt_file(data)

    filepath = os.path.join(UPLOAD_FOLDER, file.filename + ".enc")
    with open(filepath, "wb") as f:
        f.write(nonce + tag + ciphertext)

    add_file_record(file.filename)
    flash(f"File {file.filename} uploaded and encrypted successfully!", "success")
    return redirect(url_for("index"))

@app.route("/download/<filename>")
def download(filename):
    filepath = os.path.join(UPLOAD_FOLDER, filename + ".enc")
    if not os.path.exists(filepath):
        flash("File not found", "error")
        return redirect(url_for("index"))

    with open(filepath, "rb") as f:
        nonce = f.read(16)
        tag = f.read(16)
        ciphertext = f.read()

    plaintext = decrypt_file(nonce, ciphertext, tag)
    return send_file(BytesIO(plaintext), as_attachment=True, download_name=filename)

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
