from app.__init__ import db

class Dokter(db.Model):
    __tablename__ = 'dokter'

    id_dokter = db.Column(db.Integer, primary_key=True)
    nama_dokter = db.Column(db.String(255), nullable=False)
    spesialis = db.Column(db.String(100))
    id_faskes = db.Column(db.Integer, db.ForeignKey('faskes.id_faskes'), nullable=False)

    jadwal = db.relationship('Jadwal_Faskes', backref='dokter', lazy=True)