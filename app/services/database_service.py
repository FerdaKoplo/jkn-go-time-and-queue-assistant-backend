import pandas as pd
from app import db
from app.models import Antrian, Jadwal_Faskes, Dokter, Faskes
from app.enums.enums import StatusAntrian
from datetime import datetime

def get_training_data():
    print("Mengambil data training dari database...")
    
    query = db.session.query(
        Antrian.waktu_datang,
        Antrian.waktu_panggil,
        Antrian.waktu_selesai,
        Faskes.kapasitas_harian,
        Faskes.tipe_faskes,
        Dokter.spesialis
    ).join(
        Jadwal_Faskes, Antrian.id_jadwal == Jadwal_Faskes.id_jadwal
    ).join(
        Dokter, Jadwal_Faskes.id_dokter == Dokter.id_dokter
    ).join(
        Faskes, Dokter.id_faskes == Faskes.id_faskes
    ).filter(
        Antrian.status_antrian == StatusAntrian.DILAYANI,
        Antrian.waktu_panggil.isnot(None),
        Antrian.waktu_selesai.isnot(None)
    )
    
    try:
        with db.engine.connect() as connection:
            df = pd.read_sql(query.statement, connection)

        if 'tipe_faskes' in df.columns:
            df['tipe_faskes'] = df['tipe_faskes'].apply(lambda x: x.name)
        
        print(f"Berhasil mengambil {len(df)} baris data training.")
        return df
    except Exception as e:
        print(f"Error saat mengambil data training: {e}")
        return pd.DataFrame()

def get_current_antrian_status(faskes_id: int, current_timestamp: datetime) -> int:
    try:
        
        count = db.session.query(Antrian).join(
            Jadwal_Faskes, Antrian.id_jadwal == Jadwal_Faskes.id_jadwal
        ).join(
            Dokter, Jadwal_Faskes.id_dokter == Dokter.id_dokter
        ).filter(
            Dokter.id_faskes == faskes_id,
            Antrian.waktu_datang <= current_timestamp,
            Antrian.waktu_panggil.is_(None)
        ).count()
        
        return count

    except Exception as e:
        print(f"Error saat menghitung antrian aktif: {e}")
        return 0