from app.__init__ import db 
from app.enums.enums import JenisReminder

class Peserta(db.Model):
    __tablename__ = 'peserta'

    id_peserta = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(255), nullable=False)
    nik = db.Column(db.String(16))
    no_bpjs = db.Column(db.String(20))
    email = db.Column(db.String(100))
    no_hp = db.Column(db.String(15))
    alamat = db.Column(db.Text)
    tanggal_lahir = db.Column(db.Date)
    preferensi_reminder = db.Column(db.String(50)) 

    antrian = db.relationship('Antrian', backref='peserta', lazy=True)
    reminder = db.relationship('Reminder', backref='peserta', lazy=True)
    riwayat_kunjungan = db.relationship('Riwayat_Kunjungan', backref='peserta', lazy=True)