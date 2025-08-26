Secure File Sharing System

A simple yet secure file sharing system built with Flask. 
Files are encrypted with AES before storage and decrypted upon download.

Features
- Secure file upload and download
- AES encryption for files at rest
- Basic key management with `.env`
- User-friendly web interface

Tech Stack
- Python Flask
- PyCryptodome
- HTML / CSS

How to Run
1. Clone this repo
2. Create `.env` with `AES_KEY=...`
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
