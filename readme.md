🔐 Secure File Upload and Encryption System

This project is a Flask-based web application that allows users to securely upload and download files.
All uploaded files are encrypted using AES (Advanced Encryption Standard) before being stored on the server, ensuring confidentiality and protection against unauthorized access.
When users download a file, the application automatically decrypts it and returns the original content.

✨ Features

📂 Upload any type of file (text, images, documents, etc.)

🔒 AES-CBC encryption for data security

🛡️ AES key management using a .env file (Base64 encoded)

⏳ Displays uploaded files with timestamp (UTC)

⬇️ Download files in their original form after automatic decryption

🗄️ Encrypted files stored securely with .enc extension

🛠️ Tech Stack

Python 3.10+

Flask (lightweight web framework)

PyCryptodome (for AES encryption/decryption)

dotenv (to manage secret keys securely)

HTML + Bootstrap (for front-end UI)

🚀 How It Works

Upload: User selects a file and uploads it.

File is immediately encrypted with AES and saved as <filename>.enc.

Storage: Only encrypted versions are stored in the uploads/ folder.

Opening these directly will show unreadable gibberish.

Download: When a user downloads, the file is decrypted back to the original version automatically.

📂 Project Structure
.
├── app.py           # Flask backend
├── index.html       # Frontend template
├── uploads/         # Folder to store encrypted files
├── .env             # Stores AES_KEY (Base64 encoded)
├── requirements.txt # Python dependencies
└── README.md        # Project documentation

🔑 Security

AES-128 encryption (16-byte key) with random IV (Initialization Vector) for each file

.env file ensures the key is not hardcoded in source code

Encrypted files cannot be read without the correct AES key

📸 Screenshots

File upload form

Uploaded files list with timestamps

Download button (returns original decrypted file)

🎯 Use Cases

Securely share files in small teams

University / internship projects for demonstrating cryptography concepts

Training tool for data confidentiality in web applications
