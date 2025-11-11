import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import joblib
import os
from datetime import datetime, timedelta
from app.utils.config import Config
from .database_service import get_training_data 
from app import db

MODEL_FILE = Config.MODEL_PATH
model_pipeline = None

def get_model_pipeline():
    global model_pipeline
    if model_pipeline is None and os.path.exists(MODEL_FILE):
        model_pipeline = joblib.load(MODEL_FILE)
    return model_pipeline

def preprocess_features(df, training=True):
    
    if training:
        df['durasi_layanan_menit'] = (df['waktu_selesai'] - df['waktu_panggil']).dt.total_seconds() / 60
    
    if 'waktu_datang' in df.columns and pd.api.types.is_datetime64_any_dtype(df['waktu_datang']):
        df['jam_datang'] = df['waktu_datang'].dt.hour
        df['hari_datang'] = df['waktu_datang'].dt.dayofweek 
    
    numerical_features = ['kapasitas_harian', 'jam_datang']
    categorical_features = ['tipe_faskes', 'hari_datang', 'spesialis']
    
    cols_to_drop = [col for col in ['waktu_panggil', 'waktu_selesai', 'waktu_datang', 'tanggal'] if col in df.columns]

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), [f for f in numerical_features if f in df.columns]),
            ('cat', OneHotEncoder(handle_unknown='ignore'), [f for f in categorical_features if f in df.columns])
        ],
        remainder='drop' 
    )
    
    df_features = df.drop(columns=cols_to_drop, errors='ignore')
    
    return df_features, preprocessor

def train_and_save_model():
    global model_pipeline
    print("Memulai training model untuk DURASI LAYANAN...")
    df = get_training_data()
    
    if df.empty or 'waktu_panggil' not in df.columns or 'waktu_selesai' not in df.columns:
        print("Gagal memuat data atau kolom 'waktu_panggil'/'waktu_selesai' tidak ada.")
        return False

    df_features, preprocessor = preprocess_features(df, training=True)
    
    
    X = df_features.drop(columns=['durasi_layanan_menit'])
    Y = df_features['durasi_layanan_menit']
    
    if 'waktu_datang' not in df.columns:
        print("Kolom 'waktu_datang' (dibutuhkan untuk fitur 'jam_datang') tidak ditemukan.")
        return False
    
    X_train, _, Y_train, _ = train_test_split(X, Y, test_size=0.2, random_state=42)
    
    model_pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('regressor', RandomForestRegressor(n_estimators=100, max_depth=8, random_state=42, n_jobs=-1))
    ])
    
    model_pipeline.fit(X_train, Y_train)
    
    os.makedirs(os.path.dirname(MODEL_FILE), exist_ok=True)
    joblib.dump(model_pipeline, MODEL_FILE)
    print(f"Training durasi layanan selesai. Model disimpan di: {MODEL_FILE}")
    
    get_model_pipeline()
    return True

def load_model():
    return get_model_pipeline()

def predict_service_duration(tipe_faskes, kapasitas_harian, spesialis, waktu_datang_pasien_str):
    model = get_model_pipeline()
    if model is None:
        return None

    waktu_datang = datetime.fromisoformat(waktu_datang_pasien_str)
    
    
    input_data = {
        'kapasitas_harian': [kapasitas_harian],
        'tipe_faskes': [tipe_faskes],
        'spesialis': [spesialis],
        'waktu_datang': [waktu_datang] 
    }
    input_df = pd.DataFrame(input_data)
    
    input_df['jam_datang'] = input_df['waktu_datang'].dt.hour
    input_df['hari_datang'] = input_df['waktu_datang'].dt.dayofweek
    
    X_cols = ['kapasitas_harian', 'tipe_faskes', 'spesialis', 'jam_datang', 'hari_datang']
    X_input = input_df[X_cols]

    prediction_array = model.predict(X_input)
    
    return prediction_array[0]