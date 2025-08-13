# ♟ Chess Tournament Manager (CLI)

Manage chess clubs, players, and tournaments from a friendly command-line interface.\
Built with Python, flake8-linting, and HTML lint reports for clean, maintainable code.

---

## 📋 Features

- Manage chess clubs and player rosters
- Create and run multiple tournaments
- Register players, enter match results, and advance rounds
- Auto-generate tournament reports
- Linting with flake8 + HTML report generation

---

## 🛠 Tech Stack

- **Language:** Python 3.9

- **Linting:** flake8 + flake8-html

- **Data storage:** JSON files (`/data` folder)



## 🚀 Getting Started

### 1. Clone and enter folder

```bash
git clone <REPO_URL>
cd <FOLDER_NAME>
```

### 2. Create and activate venv

```bash
python -m venv .venv
# Windows
. .venv/Scripts/activate
# macOS/Linux
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## ▶ Running the App

```bash
python manage_clubs.py
```

Follow the on-screen menus to navigate clubs, tournaments, and players.

---

## 🧹 Linting & HTML Report

### Run flake8 normally

```bash
flake8 .
```

### Generate HTML report

```bash
flake8 --format=html --htmldir=flake8_report
```

Open `flake8_report/index.html` in your browser to view the report.

---

##

---

##

