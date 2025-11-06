from app.__init__ import db

class Riwayat_Kunjungan(db.Model):
    __tablename__ = 'riwayat_kunjungan'

    id_riwayat = db.Column(db.Integer, primary_key=True)
    id_peserta = db.Column(db.Integer, db.ForeignKey('peserta.id_peserta'), nullable=False)
    id_faskes = db.Column(db.Integer, db.ForeignKey('faskes.id_faskes'), nullable=False)
    id_layanan = db.Column(db.Integer)
    tanggal_kunjungan = db.Column(db.Date)
    status = db.Column(db.String(50))