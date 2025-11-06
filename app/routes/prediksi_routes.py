from flask import request, jsonify
from app.routes import blueprint
from app.services.ml_service import load_model, predict_time_to_serve
from datetime import datetime, timedelta 


@blueprint.route('/predict', methods=['POST'])
def predict_arrival_time():
    data = request.get_json()
    
    model = load_model()
    if not model:
        return jsonify({"message": "Model ML belum siap. Harap jalankan training terlebih dahulu.", "predicted_wait_time_minutes": None}), 503

    required_fields = ["id_faskes", "tipe_faskes", "kapasitas_harian", "spesialis", "waktu_datang_pasien"]
    if not all(field in data for field in required_fields):
        return jsonify({"message": "Input tidak lengkap. Harap sertakan semua field wajib.", "predicted_wait_time_minutes": None}), 400

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
        
        return jsonify({
            "message": "Prediksi berhasil dihitung.",
            "predicted_wait_time_minutes": round(predicted_minutes, 2),
            "estimated_service_time": (datetime.fromisoformat(data['waktu_datang_pasien']) + 
                                       timedelta(minutes=predicted_minutes)).isoformat()
        }), 200

    except Exception as e:
        return jsonify({"message": f"Terjadi kesalahan internal: {str(e)}", "predicted_wait_time_minutes": None}), 500
