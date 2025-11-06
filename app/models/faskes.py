from app.__init__ import db
from app.enums.enums import TipeFaskes

class Faskes(db.Model):
    __tablename__ = 'faskes'

    id_faskes = db.Column(db.Integer, primary_key=True)
    nama_faskes = db.Column(db.String(255), nullable=False)
    alamat = db.Column(db.Text)
    kapasitas_harian = db.Column(db.Integer)
    tipe_faskes = db.Column(db.Enum(TipeFaskes), nullable=False)

    dokter = db.relationship('Dokter', backref='faskes', lazy=True)
    riwayat_kunjungan = db.relationship('Riwayat_Kunjungan', backref='faskes', lazy=True)
    monitoring_antrian = db.relationship('Monitoring_Antrian', backref='faskes', lazy=True)