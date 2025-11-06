from flask import jsonify
from . import blueprint
from app.services.ml_service import load_model

@blueprint.route('/status', methods=['GET'])
def get_status():
    
    model = load_model()
    model_status = "OK" if model else "NOT LOADED / NEEDS TRAINING"
    
    return jsonify({
        "status": "Running",
        "service": "Faskes Queue Assistant API",
        "ml_model": model_status,
        "version": "v1.0"
    }), 200

@blueprint.route('/train', methods=['POST'])
def trigger_training():
    from app.services.ml_service import train_and_save_model
    
    try:
        if train_and_save_model():
            return jsonify({"message": "ML training berhasil dipicu dan selesai.", "status": "success"}), 200
        else:
            return jsonify({"message": "Gagal memicu training. Periksa data atau log.", "status": "failed"}), 500
    except Exception as e:
        return jsonify({"message": f"Terjadi error saat training: {str(e)}", "status": "error"}), 500
