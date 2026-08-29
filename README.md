# UnlockPDF

A simple web app to remove password protection from a PDF file, when you know the password.

## Setup

```bash
pip install -r requirements.txt
python app.py
```

Then open http://localhost:5000 in your browser.

## Usage

1. Upload a PDF file.
2. Enter the password (leave blank if the PDF isn't password-protected).
3. Click "Unlock PDF" to download the unlocked file.

## Notes

- Files are processed in memory and are not saved on the server.
- Only use this tool on PDFs you own or have explicit permission to unlock.
- Max upload size: 25 MB (configurable in `app.py`).

## Tech stack

- [Flask](https://flask.palletsprojects.com/) — backend web server
- [pypdf](https://pypdf.readthedocs.io/) — PDF decryption/writing
