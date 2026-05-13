# 🌤️ Weather Analytics Dashboard

A production-ready **interactive weather analytics dashboard** built with Python Dash & Plotly.
Visualises 2 years of weather data for 10 major Indian cities with real-time filtering.

---

## 📸 Features

| Feature | Details |
|---|---|
| **KPI Cards** | Avg / Max / Min Temperature, Avg Humidity, Avg Wind Speed |
| **Temperature Trend** | Line chart — daily avg across selected cities |
| **7-Day Moving Average** | Smoothed temperature trend |
| **Monthly Humidity** | Bar chart grouped by month |
| **Condition Distribution** | Donut pie chart |
| **Wind vs Temp Scatter** | Colour-coded by weather condition |
| **Correlation Heatmap** | Temp / Humidity / Wind / Pressure |
| **City Box Plot** | Temperature distribution per city |
| **Sidebar Filters** | City, Condition, Temp Range, Humidity Range, Date Range |

---

## 🗂️ Folder Structure

```
Weather Analytics Dashboard/
│
├── app.py                  ← Main entry point (run this)
│
├── config/
│   ├── __init__.py
│   ├── setting.py          ← Master config (colours, paths, app settings)
│   └── settings.py         ← Re-export shim (keeps all imports consistent)
│
├── components/
│   ├── __init__.py
│   ├── cards.py            ← KPI card HTML builders
│   ├── charts.py           ← All Plotly chart functions
│   └── filters.py          ← Sidebar filter controls
│
├── utilis/
│   ├── __init__.py
│   ├── data_loader.py      ← CSV loader with validation
│   ├── preprocessing.py    ← Cleaning, feature engineering, filtering
│   └── analytics.py        ← KPI & chart aggregation functions
│
├── data/
│   ├── generate_data.py    ← Run this FIRST to create weather.csv
│   └── weather.csv         ← Auto-generated dataset (10 cities × 2 years)
│
├── assets/
│   └── style.css           ← Premium dark-mode UI theme (Dash auto-loads)
│
├── logs/
│   └── dashboard.log       ← Runtime logs (auto-created)
│
├── notebooks/              ← Jupyter notebooks for EDA (optional)
├── outputs/                ← Saved charts/exports (optional)
│
├── requirements.txt        ← All Python dependencies
├── .env.example            ← Environment variable template
└── README.md
```

---

## ⚙️ Setup Instructions (Step by Step)

### Step 1 — Prerequisites
- Python 3.9 or higher installed
- VS Code (recommended)
- Git (optional)

Verify Python:
```bash
python --version
```

---

### Step 2 — Create Virtual Environment

```bash
# Open terminal in the project folder
cd "Weather Analytics Dashboard"

# Create virtual environment
python -m venv venv

# Activate (Windows PowerShell)
.\venv\Scripts\Activate.ps1

# Activate (Windows CMD)
venv\Scripts\activate.bat
```

> **Note:** You should see `(venv)` in your terminal prompt after activation.

---

### Step 3 — Install Dependencies

```bash
pip install -r requirements.txt
```

This installs: `dash`, `plotly`, `pandas`, `numpy`, `scikit-learn`, `gunicorn`, `python-dotenv`

---

### Step 4 — Generate Dataset

```bash
python data/generate_data.py
```

This creates `data/weather.csv` with **7,300 rows** covering 10 cities × 730 days (2023–2024).

---

### Step 5 — (Optional) Create .env File

```bash
copy .env.example .env
```

Edit `.env` only if you want to change the port or host. Defaults work out of the box.

---

### Step 6 — Run the Dashboard

```bash
python app.py
```

Open your browser and go to: **http://127.0.0.1:8050**

---

## 🚀 Quick Start (All Steps in One)

```bash
python -m venv venv && .\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python data/generate_data.py
python app.py
```

---

## 🧰 Tech Stack

| Layer | Technology |
|---|---|
| **UI Framework** | Plotly Dash 2.x |
| **Charts** | Plotly 5.x |
| **Data Processing** | Pandas 2.x, NumPy |
| **Styling** | Vanilla CSS (dark theme) |
| **Logging** | Python `logging` |
| **Production Server** | Gunicorn |
| **Config Management** | python-dotenv |

---

## ❌ Common Errors & Fixes

| Error | Cause | Fix |
|---|---|---|
| `FileNotFoundError: weather.csv` | Dataset not generated | Run `python data/generate_data.py` |
| `ModuleNotFoundError: dash` | venv not activated or packages not installed | Activate venv, then `pip install -r requirements.txt` |
| `Port 8050 already in use` | Another app is running on port 8050 | Change `APP_PORT=8051` in `.env` or kill the other process |
| `cannot import name 'X'` | Python path issue | Always run `python app.py` from the project root folder |
| `No data for selected filters` | Filters too restrictive | Click **Reset Filters** in the sidebar |
| `Script cannot be loaded` (PowerShell) | Execution policy | Run: `Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned` |

---

## 🔮 Future Improvements

- [ ] Real-time weather via OpenWeatherMap API
- [ ] ML-based temperature forecasting (Prophet / LSTM)
- [ ] Export filtered data as CSV / PDF
- [ ] Multi-language support (Hindi / English toggle)
- [ ] PWA / mobile-responsive layout
- [ ] User authentication with login page

---

## 🚢 Deployment

### Render.com (Free)
```bash
# Procfile content:
web: gunicorn app:server
```

### Docker
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
RUN python data/generate_data.py
EXPOSE 8050
CMD ["gunicorn", "-b", "0.0.0.0:8050", "app:server"]
```

---

## 📝 License

MIT — free to use, modify, and distribute.
