from flask import request, jsonify
from . import blueprint
from app.services.ml_service import load_model, predict_time_to_serve
from datetime import datetime, timedelta
from app import db
from app.models import Prediksi_Kedatangan, Antrian

@blueprint.route('/predict', methods=['POST'])
def predict_arrival_time():
    data = request.get_json()
    
    model = load_model()
    if not model:
        return jsonify({"message": "Model ML belum siap. Harap jalankan training terlebih dahulu.", "predicted_wait_time_minutes": None}), 503

    required_fields = ["id_antrian", "id_faskes", "tipe_faskes", "kapasitas_harian", "spesialis", "waktu_datang_pasien"]
    if not all(field in data for field in required_fields):
        return jsonify({"message": "Input tidak lengkap. Harap sertakan semua field wajib.", "predicted_wait_time_minutes": None}), 400

    antrian_obj = Antrian.query.get(data["id_antrian"])
    if not antrian_obj:
        return jsonify({"message": f"Antrian dengan id {data['id_antrian']} tidak ditemukan.", "predicted_wait_time_minutes": None}), 404

    try:
        predicted_minutes = predict_time_to_serve(
            id_faskes=data['id_faskes'],
            tipe_faskes=data['tipe_faskes'],
            kapasitas_harian=data['kapasitas_harian'],
            spesialis=data['spesialis'],
            waktu_datang_pasien_str=data['waktu_datang_pasien']
        )

        if predicted_minutes is None:
             return jsonify({"message": "Gagal melakukan prediksi. Cek ketersediaan data antrian aktif.", "predicted_wait_time_minutes": None}), 500

        estimated_time = datetime.fromisoformat(data['waktu_datang_pasien']) + timedelta(minutes=predicted_minutes)

        prediksi = Prediksi_Kedatangan(
            id_antrian=antrian_obj.id_antrian,
            waktu_prediksi=estimated_time,
            # akurasi_prediksi=None, 
            update_terakhir=datetime.now(),
            sumber_data="ML Model v1"
        )
        db.session.add(prediksi)
        db.session.commit()

        return jsonify({
            "message": "Prediksi berhasil dihitung dan disimpan.",
            "predicted_wait_time_minutes": round(predicted_minutes, 2),
            "estimated_service_time": estimated_time.isoformat()
        }), 200

    except Exception as e:
        db.session.rollback()  # rollback if anything fails
        return jsonify({"message": f"Terjadi kesalahan internal: {str(e)}", "predicted_wait_time_minutes": None}), 500
