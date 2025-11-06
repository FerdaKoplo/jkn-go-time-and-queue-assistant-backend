from app.__init__ import db
from app.enums.enums import StatusAntrian

class Antrian(db.Model):
    __tablename__ = 'antrian'

    id_antrian = db.Column(db.Integer, primary_key=True)
    id_peserta = db.Column(db.Integer, db.ForeignKey('peserta.id_peserta'), nullable=False)
    id_jadwal = db.Column(db.Integer, db.ForeignKey('jadwal_faskes.id_jadwal'), nullable=False)
    status_antrian = db.Column(db.Enum(StatusAntrian), nullable=False)
    waktu_datang = db.Column(db.DateTime)
    waktu_dilayani = db.Column(db.DateTime)
    
    prediksi_kedatangan = db.relationship('Prediksi_Kedatangan', backref='antrian', lazy=True, uselist=False)
    monitoring_antrian = db.relationship('Monitoring_Antrian', backref='antrian', lazy=True)