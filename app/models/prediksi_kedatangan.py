from app.__init__ import db

class Prediksi_Kedatangan(db.Model):
    __tablename__ = 'prediksi_kedatangan'

    id_prediksi = db.Column(db.Integer, primary_key=True)
    id_antrian = db.Column(db.Integer, db.ForeignKey('antrian.id_antrian'), nullable=False)
    waktu_prediksi = db.Column(db.DateTime)
    # akurasi_prediksi = db.Column(db.Float)
    update_terakhir = db.Column(db.DateTime)
    sumber_data = db.Column(db.String(100))

    reminder = db.relationship('Reminder', backref='prediksi', lazy=True)