from app import create_app, db
from app.utils.config import Config
from app.models import Peserta, Faskes, Dokter, Jadwal_Faskes, Antrian
from app.enums.enums import TipeFaskes, StatusAntrian
from datetime import datetime, date, time, timedelta

app = create_app(Config)

with app.app_context():
    # Clear existing data
    db.session.query(Antrian).delete()
    db.session.query(Jadwal_Faskes).delete()
    db.session.query(Dokter).delete()
    db.session.query(Faskes).delete()
    db.session.query(Peserta).delete()
    db.session.commit()

    # Create Peserta
    peserta_list = [
        Peserta(
            nama="Andi",
            nik="1234567890123456",
            no_bpjs="BPJS001",
            email="andi@example.com",
            no_hp="08123456789",
            alamat="Jl. Andi No.1",
            tanggal_lahir=date(1990,1,1)
        ),
        Peserta(
            nama="Budi",
            nik="2345678901234567",
            no_bpjs="BPJS002",
            email="budi@example.com",
            no_hp="08123456780",
            alamat="Jl. Budi No.2",
            tanggal_lahir=date(1985,5,5)
        ),
    ]
    db.session.add_all(peserta_list)
    db.session.commit()

    # Create Faskes
    faskes_list = [
        Faskes(
            nama_faskes="Faskes A",
            alamat="Jl. A No.1",
            kapasitas_harian=50,
            tipe_faskes=TipeFaskes.PUSKESMAS
        ),
        Faskes(
            nama_faskes="Faskes B",
            alamat="Jl. B No.2",
            kapasitas_harian=30,
            tipe_faskes=TipeFaskes.RSU
        ),
    ]
    db.session.add_all(faskes_list)
    db.session.commit()

    # Create Dokter
    dokter_list = [
        Dokter(nama_dokter="Dr. Siti", spesialis="Umum", id_faskes=faskes_list[0].id_faskes),
        Dokter(nama_dokter="Dr. Joko", spesialis="Gigi", id_faskes=faskes_list[1].id_faskes),
    ]
    db.session.add_all(dokter_list)
    db.session.commit()

    # Create Jadwal_Faskes
    jadwal_list = [
        Jadwal_Faskes(
            id_dokter=dokter_list[0].id_dokter,
            tanggal=date.today(),
            jam_mulai=time(8,0),
            jam_selesai=time(12,0)
        ),
        Jadwal_Faskes(
            id_dokter=dokter_list[1].id_dokter,
            tanggal=date.today(),
            jam_mulai=time(13,0),
            jam_selesai=time(17,0)
        ),
    ]
    db.session.add_all(jadwal_list)
    db.session.commit()

    # Active queues (for testing /predict)
    active_antrian_list = [
        Antrian(
            id_peserta=peserta_list[0].id_peserta,
            id_jadwal=jadwal_list[0].id_jadwal,
            status_antrian=StatusAntrian.MENUNGGU,
            waktu_datang=datetime.now(),
            waktu_dilayani=None
        ),
        Antrian(
            id_peserta=peserta_list[1].id_peserta,
            id_jadwal=jadwal_list[1].id_jadwal,
            status_antrian=StatusAntrian.MENUNGGU,
            waktu_datang=datetime.now(),
            waktu_dilayani=None
        ),
    ]
    db.session.add_all(active_antrian_list)

    # Completed queues (for training ML)
    completed_antrian_list = [
        Antrian(
            id_peserta=peserta_list[0].id_peserta,
            id_jadwal=jadwal_list[0].id_jadwal,
            status_antrian=StatusAntrian.DILAYANI,
            waktu_datang=datetime.now() - timedelta(minutes=60),
            waktu_dilayani=datetime.now() - timedelta(minutes=30)
        ),
        Antrian(
            id_peserta=peserta_list[1].id_peserta,
            id_jadwal=jadwal_list[1].id_jadwal,
            status_antrian=StatusAntrian.DILAYANI,
            waktu_datang=datetime.now() - timedelta(minutes=50),
            waktu_dilayani=datetime.now() - timedelta(minutes=20)
        ),
    ]
    db.session.add_all(completed_antrian_list)

    db.session.commit()

    print("Seeding selesai! Database sudah terisi dengan data contoh, termasuk antrian aktif dan historis untuk training ML.")
