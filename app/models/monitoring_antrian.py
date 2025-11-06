from app.__init__ import db

class Monitoring_Antrian(db.Model):
    __tablename__ = 'monitoring_antrian'

    id_monitor = db.Column(db.Integer, primary_key=True)
    id_faskes = db.Column(db.Integer, db.ForeignKey('faskes.id_faskes'), nullable=False)
    id_antrian = db.Column(db.Integer, db.ForeignKey('antrian.id_antrian'), nullable=False)
    tanggal = db.Column(db.Date)
    total_antrian = db.Column(db.Integer)
    rata_waktu_tunggu = db.Column(db.Float)
    akurasi_prediksi = db.Column(db.Float)