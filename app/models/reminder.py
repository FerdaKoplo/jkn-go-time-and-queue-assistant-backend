from app.__init__ import db
from app.enums.enums import JenisReminder

class Reminder(db.Model):
    __tablename__ = 'reminder'

    id_reminder = db.Column(db.Integer, primary_key=True)
    id_peserta = db.Column(db.Integer, db.ForeignKey('peserta.id_peserta'), nullable=False)
    id_prediksi = db.Column(db.Integer, db.ForeignKey('prediksi_kedatangan.id_prediksi'), nullable=False)
    waktu_kirim = db.Column(db.DateTime)
    jenis_reminder = db.Column(db.Enum(JenisReminder), nullable=False)
    status_kirim = db.Column(db.String(50))
    pesan = db.Column(db.Text)
    lokasi_trigger = db.Column(db.String(255))