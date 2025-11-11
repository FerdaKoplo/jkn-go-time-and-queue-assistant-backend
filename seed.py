import random
from app import create_app, db
from app.utils.config import Config
# Pastikan semua model di-import
from app.models import Peserta, Faskes, Dokter, Jadwal_Faskes, Antrian
from app.enums.enums import TipeFaskes, StatusAntrian
from datetime import datetime, date, time, timedelta

NAMA_PESERTA = [
    ("Andi", "1111111111111111"), ("Budi", "2222222222222222"),
    ("Caca", "3333333333333333"), ("Dedi", "4444444444444444"),
    ("Eka", "5555555555555555"), ("Fani", "6666666666666666"),
    ("Gilang", "7777777777777777"), ("Hana", "8888888888888888"),
]

app = create_app(Config)

with app.app_context():
    print("Menghapus data lama...")
    db.session.query(Antrian).delete()
    db.session.query(Jadwal_Faskes).delete()
    db.session.query(Dokter).delete()
    db.session.query(Faskes).delete()
    db.session.query(Peserta).delete()
    db.session.commit()

    print("Membuat Peserta...")
    peserta_list = []
    for i, (nama, nik) in enumerate(NAMA_PESERTA):
        peserta = Peserta(
            nama=nama,
            nik=f"{nik}",
            no_bpjs=f"BPJS{i:03d}",
            email=f"{nama.lower()}@example.com",
            no_hp=f"081234567{i:02d}",
            alamat=f"Jl. {nama} No.{i+1}",
            tanggal_lahir=date(1990 + i, 1 + i % 11, 1 + i % 27)
        )
        peserta_list.append(peserta)
    db.session.add_all(peserta_list)
    db.session.commit()

    print("Membuat Faskes...")
    faskes_list = [
        Faskes(
            nama_faskes="Puskesmas Melati",
            alamat="Jl. Melati No.1",
            kapasitas_harian=50,
            tipe_faskes=TipeFaskes.PUSKESMAS
        ),
        Faskes(
            nama_faskes="RSU Harapan Bangsa",
            alamat="Jl. Harapan No.2",
            kapasitas_harian=100,
            tipe_faskes=TipeFaskes.RSU
        ),
        Faskes(
            nama_faskes="Klinik Gigi Sehat",
            alamat="Jl. Gigi No.3",
            kapasitas_harian=30,
            tipe_faskes=TipeFaskes.KLINIK
        ),
    ]
    db.session.add_all(faskes_list)
    db.session.commit()

    print("Membuat Dokter...")
    dokter_list = [
        Dokter(nama_dokter="Dr. Siti", spesialis="Umum", id_faskes=faskes_list[0].id_faskes),
        Dokter(nama_dokter="Dr. Budi", spesialis="Umum", id_faskes=faskes_list[0].id_faskes),
        Dokter(nama_dokter="Dr. Joko", spesialis="Jantung", id_faskes=faskes_list[1].id_faskes),
        Dokter(nama_dokter="Dr. Ana", spesialis="Kulit", id_faskes=faskes_list[1].id_faskes),
        Dokter(nama_dokter="Dr. Rini", spesialis="Gigi", id_faskes=faskes_list[2].id_faskes),
    ]
    db.session.add_all(dokter_list)
    db.session.commit()

    print("Membuat Jadwal Faskes...")
    jadwal_list = [
        Jadwal_Faskes(id_dokter=dokter_list[0].id_dokter, tanggal=date(2023, 1, 1), jam_mulai=time(8,0), jam_selesai=time(12,0)),
        Jadwal_Faskes(id_dokter=dokter_list[1].id_dokter, tanggal=date(2023, 1, 1), jam_mulai=time(13,0), jam_selesai=time(17,0)),
        Jadwal_Faskes(id_dokter=dokter_list[2].id_dokter, tanggal=date(2023, 1, 1), jam_mulai=time(9,0), jam_selesai=time(15,0)),
        Jadwal_Faskes(id_dokter=dokter_list[3].id_dokter, tanggal=date(2023, 1, 1), jam_mulai=time(10,0), jam_selesai=time(14,0)),
        Jadwal_Faskes(id_dokter=dokter_list[4].id_dokter, tanggal=date(2023, 1, 1), jam_mulai=time(8,0), jam_selesai=time(16,0)),
    ]
    db.session.add_all(jadwal_list)
    db.session.commit()
    
    all_jadwal_ids = [j.id_jadwal for j in Jadwal_Faskes.query.all()]
    all_peserta_ids = [p.id_peserta for p in Peserta.query.all()]

    print("Membuat data Antrian historis untuk Training ML...")
    completed_antrian_list = []
    
    for i in range(200):
        random_jadwal_id = random.choice(all_jadwal_ids)
        random_peserta_id = random.choice(all_peserta_ids)
        
        jadwal = db.session.get(Jadwal_Faskes, random_jadwal_id)
        dokter = db.session.get(Dokter, jadwal.id_dokter)
        
        hari_lalu = random.randint(1, 60)
        jam_datang_max = jadwal.jam_selesai.hour - 1 if jadwal.jam_selesai.hour > jadwal.jam_mulai.hour else jadwal.jam_mulai.hour
        jam_datang = random.randint(jadwal.jam_mulai.hour, jam_datang_max)
        menit_datang = random.randint(0, 59)
        waktu_datang = datetime.combine(
            date.today() - timedelta(days=hari_lalu),
            time(jam_datang, menit_datang)
        )
        
        waktu_tunggu_menit = random.randint(5, 45) 
        waktu_panggil = waktu_datang + timedelta(minutes=waktu_tunggu_menit)
        
        if dokter.spesialis == "Umum":
            durasi_menit = random.randint(5, 15)
        elif dokter.spesialis == "Gigi":
            durasi_menit = random.randint(20, 60)
        elif dokter.spesialis == "Jantung":
            durasi_menit = random.randint(15, 40)
        elif dokter.spesialis == "Kulit":
            durasi_menit = random.randint(10, 25) 
        else:
            durasi_menit = random.randint(10, 20)
            
        waktu_selesai = waktu_panggil + timedelta(minutes=durasi_menit)

        jadwal_tutup_dt = datetime.combine(waktu_datang.date(), jadwal.jam_selesai)

        if waktu_panggil > jadwal_tutup_dt:
            waktu_panggil = jadwal_tutup_dt
            
        waktu_selesai = waktu_panggil + timedelta(minutes=durasi_menit)
        
        if waktu_selesai > jadwal_tutup_dt:
            waktu_selesai = jadwal_tutup_dt
            
            
        antrian = Antrian(
            id_peserta=random_peserta_id,
            id_jadwal=random_jadwal_id,
            status_antrian=StatusAntrian.DILAYANI,
            waktu_datang=waktu_datang,
            waktu_panggil=waktu_panggil,
      
      
            waktu_selesai=waktu_selesai
        )
        completed_antrian_list.append(antrian)

    db.session.add_all(completed_antrian_list)
    db.session.commit()
    
    print("Membuat antrian aktif (untuk testing)...")
    jadwal_tes_list = Jadwal_Faskes.query.all()
    active_antrian_list = [] # Inisialisasi
    if jadwal_tes_list:
        active_antrian_list = [
            Antrian(
                id_peserta=peserta_list[0].id_peserta,
                id_jadwal=jadwal_tes_list[0].id_jadwal, 
                status_antrian=StatusAntrian.MENUNGGU,
                waktu_datang=datetime.now() - timedelta(minutes=10)
            ),
            Antrian(
                id_peserta=peserta_list[1].id_peserta,
                id_jadwal=jadwal_tes_list[0].id_jadwal,
                status_antrian=StatusAntrian.MENUNGGU,
                waktu_datang=datetime.now() - timedelta(minutes=5)
            ),
        ]
        db.session.add_all(active_antrian_list)
        db.session.commit()

    print(f"Seeding selesai! Database sudah terisi dengan {len(completed_antrian_list)} data training ML dan {len(active_antrian_list)} data antrian aktif.")