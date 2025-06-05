from flask import request, jsonify
from . import data_ingestion_bp
from .processing import process_eye_tracking_data, process_voice_analysis_data

@data_ingestion_bp.route('/data/eye_tracking', methods=['POST'])
def receive_eye_tracking_data():
    data = request.get_json()
    print(f"Received eye tracking data: {data}") # Or use app.logger
    processed_data = process_eye_tracking_data(data)
    return jsonify({"message": "Eye tracking data received and processed", "data": processed_data}), 200

@data_ingestion_bp.route('/data/voice_analysis', methods=['POST'])
def receive_voice_analysis_data():
    data = request.get_json()
    print(f"Received voice analysis data: {data}") # Or use app.logger
    processed_data = process_voice_analysis_data(data)
    return jsonify({"message": "Voice analysis data received and processed", "data": processed_data}), 200
