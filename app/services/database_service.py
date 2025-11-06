from app import db 
from app.models import Antrian, Jadwal_Faskes, Dokter, Faskes
import pandas as pd
from datetime import datetime
from sqlalchemy import text 
def get_training_data():
    try:
        query = db.session.query(
            Antrian.waktu_datang,
            Antrian.waktu_dilayani,
            Faskes.kapasitas_harian,
            Faskes.tipe_faskes,
            Dokter.spesialis,
            Jadwal_Faskes.tanggal
        ).join(
            Jadwal_Faskes, Antrian.id_jadwal == Jadwal_Faskes.id_jadwal
        ).join(
            Dokter, Jadwal_Faskes.id_dokter == Dokter.id_dokter
        ).join(
            Faskes, Dokter.id_faskes == Faskes.id_faskes
        ).filter(
            Antrian.waktu_datang.isnot(None),
            Antrian.waktu_dilayani.isnot(None)
        )
        
        with db.session.connection() as connection:
            df = pd.read_sql(query.statement, connection)
        
        
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
            Antrian.waktu_dilayani.is_(None)
        ).count()
        
        return count

    except Exception as e:
        print(f"Error saat menghitung antrian aktif: {e}")
        return 0
