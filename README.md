# JKN Go Time and Queue Assistant Backend

## Overview

This is the backend for the JKN Go Time and Queue Assistant, a Flask-based application that predicts patient wait times at healthcare facilities using a machine learning model and manages queue data.

The system allows:

* Storing and managing patients (`Peserta`), healthcare facilities (`Faskes`), doctors (`Dokter`), schedules (`Jadwal_Faskes`), and queues (`Antrian`).
* Training a machine learning model to predict waiting times.
* Making predictions for patient arrival and expected service time.
* Storing predictions in `Prediksi_Kedatangan` with future accuracy calculations.

## Requirements

* Python 3.9+
* MySQL
* Pip packages listed in `requirements.txt`

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/FerdaKoplo/jkn-go-time-and-queue-assistant-backend.git
cd jkn-go-time-and-queue-assistant-backend
```

### 2. Create virtual environment

```bash
python -m venv env
source env/bin/activate  # macOS/Linux
env\Scripts\activate     # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure database

* Set up a MySQL database and update `app/utils/config.py` with your DB credentials.
* Ensure database exists, e.g., `db_faskes`.

### 5. Initialize database

```bash
python
>>> from app import create_app, db
>>> from app.utils.config import Config
>>> app = create_app(Config)
>>> with app.app_context():
...     db.create_all()
```

### 6. Seed example data (optional, for testing)

```bash
python seed_data.py
```

This will populate the tables: `Peserta`, `Faskes`, `Dokter`, `Jadwal_Faskes`, `Antrian`.

### 7. Run the application

```bash
python run.py
```

The API will run at `http://127.0.0.1:5000`.

## API Endpoints

### 1. Health & Status

**GET /api/v1/status**

* Returns the service status and ML model load state.

### 2. Trigger ML Training

**POST /api/v1/train**

* Triggers training the machine learning model using historical queue data.
* Response example:

```json
{
  "message": "ML training berhasil dipicu dan selesai.",
  "status": "success"
}
```

### 3. Predict Arrival Time

**POST /api/v1/predict**

* Input JSON:

```json
{
  "id_antrian": 1,
  "id_faskes": 1,
  "tipe_faskes": "PUSKESMAS",
  "kapasitas_harian": 50,
  "spesialis": "Umum",
  "waktu_datang_pasien": "2025-11-06T08:00:00"
}
```

* Response example:

```json
{
  "message": "Prediksi berhasil dihitung dan disimpan.",
  "predicted_wait_time_minutes": 30.0,
  "estimated_service_time": "2025-11-06T08:30:00"
}
```

* Stores prediction in `Prediksi_Kedatangan`. will be updated once actual service time (`waktu_dilayani`) is recorded.

## Testing ML Model

1. Ensure `Antrian` table has historical served data (`waktu_dilayani` filled) to train.
2. Trigger training:

```bash
curl -X POST http://127.0.0.1:5000/api/v1/train
```

3. Make prediction for an existing queue:

```bash
curl -X POST http://127.0.0.1:5000/api/v1/predict \
-H "Content-Type: application/json" \
-d '{
    "id_antrian": 1,
    "id_faskes": 1,
    "tipe_faskes": "PUSKESMAS",
    "kapasitas_harian": 50,
    "spesialis": "Umum",
    "waktu_datang_pasien": "2025-11-06T08:00:00"
}'
```

## Notes

* `Prediksi_Kedatangan` is used to store predictions for future analysis.
* Use `APScheduler` to schedule retraining jobs (e.g., weekly).

## Directory Structure

```
jkn-go-time-and-queue-assistant-backend/
├── app/
│   ├── __init__.py
│   ├── routes/
│   ├── services/
│   ├── models.py
│   ├── utils/
│   └── extension.py
├── run.py
├── seed_data.py
├── requirements.txt
└── README.md  (this file)
```

## Contribution

* Fork the repository.
* Set up your local environment following this README.
* Run and test ML predictions.
* Create pull requests for improvements or bug fixes.

---
