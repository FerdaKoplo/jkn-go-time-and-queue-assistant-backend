from app.__init__ import db

class Jadwal_Faskes(db.Model):
    __tablename__ = 'jadwal_faskes'

    id_jadwal = db.Column(db.Integer, primary_key=True)
    id_dokter = db.Column(db.Integer, db.ForeignKey('dokter.id_dokter'), nullable=False)
    id_layanan = db.Column(db.Integer) 
    tanggal = db.Column(db.Date, nullable=False)
    jam_mulai = db.Column(db.Time)
    jam_selesai = db.Column(db.Time)

    antrian = db.relationship('Antrian', backref='jadwal', lazy=True)