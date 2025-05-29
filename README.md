# Backplane
![Logo](backplane/static/logo.png)

## About

Backplane is a vintage computer hardware inventory and asset tracking system designed to manage components, systems, and docs for various retro/vintage computing things.

Backplane is built using Flask (Python), SQLite, and WTForms, and provides various features like:

- Component and system management
- Automatic part ID generation
- Easily fillable forms
- Relevancy tags system
- Search/filtering functions
- File/documentation upload per component
- Editable fields

---

## Installation

### 1. **Clone the repository**
```bash
git clone https://github.com/EekRats/backplane.git
cd backplane
```

### 2. **Create a virtual environment**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. **Install dependencies**
```bash
pip install -r requirements.txt
```

### 4. **Run the app**
```bash
python3 run.py
```

### 5. Navigate to 127.0.0.1:5000

---

## Configuration

All configuration is in `config.py`. You can modify:
- UPLOAD_FOLDER (where documentation is stored)
- MAX_CONTENT_LENGTH (max filesize for uploads)
- ALLOWED_EXTENSIONS (which file types can be uploaded; currently disabled as this is designed to be hosted privately)
- SQLALCHEMY_DATABASE_URI (path to database)
- TYPE_LABELS (Values and Labels for part type tracking)

---

## License

Backplane is licensed under the GNU GPLv3.
See LICENSE for full terms.
Essentially, you are free to use, modify, and redistribute, as long as you share alike.

---

## Roadmap/Ideas/etc.

- Barcode/QR/NFC tag integration
- Check-in/check-out system
- API
- Further UI polish

---

## Contributing

PRs are more than welcome! Create an issue or fork the repo and submit changs