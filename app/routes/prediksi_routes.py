from flask import request, jsonify
from . import blueprint
from app.services.ml_service import load_model, predict_service_duration
from datetime import datetime
from app import db

@blueprint.route('/predict_duration', methods=['POST'])
def predict_duration_endpoint():
    data = request.get_json()
    
    model = load_model()
    if not model:
        return jsonify({"message": "Model ML belum siap. Harap jalankan training terlebih dahulu.", "predicted_service_duration_minutes": None}), 503

    required_fields = ["tipe_faskes", "kapasitas_harian", "spesialis", "waktu_datang_pasien"]
    if not all(field in data for field in required_fields):
        return jsonify({"message": "Input tidak lengkap. Harap sertakan semua field wajib.", "predicted_service_duration_minutes": None}), 400

    try:
        predicted_minutes = predict_service_duration(
            tipe_faskes=data['tipe_faskes'],
            kapasitas_harian=data['kapasitas_harian'],
            spesialis=data['spesialis'],
            waktu_datang_pasien_str=data['waktu_datang_pasien']
        )

        if predicted_minutes is None:
             return jsonify({"message": "Gagal melakukan prediksi.", "predicted_service_duration_minutes": None}), 500

        
        return jsonify({
            "message": "Prediksi durasi layanan berhasil dihitung.",
            "predicted_service_duration_minutes": round(predicted_minutes, 2)
        }), 200

    except Exception as e:
        return jsonify({"message": f"Terjadi kesalahan internal: {str(e)}", "predicted_service_duration_minutes": None}), 500