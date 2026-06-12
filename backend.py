from flask import Flask, request, jsonify
from flask_cors import CORS
import cloudinary
import cloudinary.uploader
import base64
import io
import json
import os
from datetime import datetime

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*", "methods": ["GET", "POST", "OPTIONS"]}}, allow_headers=["Content-Type"])

# Cloudinary config
CLOUDINARY_URL = os.environ.get("CLOUDINARY_URL", "")
if CLOUDINARY_URL:
    cloudinary.config(url=CLOUDINARY_URL)

# In-memory log (for demo; replace with DB if needed)
foto_log = []

@app.route('/upload', methods=['POST'])
def upload():
    try:
        data = request.json
        base64_file = data.get('file')
        gast = data.get('gast', 'Onbekend')
        apparaat = data.get('apparaat', 'unknown')
        bestandsnaam = data.get('naam', 'foto.jpg')

        if not base64_file:
            return jsonify({'error': 'Geen bestand'}), 400

        # Decode base64
        try:
            file_bytes = base64.b64decode(base64_file)
        except:
            return jsonify({'error': 'Invalid base64'}), 400

        # If Cloudinary configured, upload there
        if CLOUDINARY_URL and cloudinary.config().cloud_name:
            try:
                result = cloudinary.uploader.upload(
                    io.BytesIO(file_bytes),
                    resource_type='auto',
                    folder=f'mm-bruiloft/{apparaat}',
                    public_id=bestandsnaam.replace('.jpg', ''),
                    overwrite=True
                )
                file_id = result.get('public_id')
                file_url = result.get('secure_url')
            except Exception as e:
                return jsonify({'error': f'Upload failed: {str(e)}'}), 500
        else:
            # Fallback: just generate ID
            file_id = f"{apparaat}/{bestandsnaam}"
            file_url = None

        # Log
        entry = {
            'datum': datetime.now().isoformat(),
            'gast': gast,
            'apparaat': apparaat,
            'bestand': bestandsnaam,
            'id': file_id,
            'url': file_url
        }
        foto_log.append(entry)

        return jsonify({
            'success': True,
            'id': file_id,
            'pad': f"{apparaat}/{bestandsnaam}",
            'url': file_url
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok', 'fotos': len(foto_log)})

@app.route('/stats', methods=['GET'])
def stats():
    unique_devices = set(entry['apparaat'] for entry in foto_log)
    return jsonify({
        'total_fotos': len(foto_log),
        'unique_devices': len(unique_devices),
        'gasten': list(set(entry['gast'] for entry in foto_log))
    })

if __name__ == '__main__':
    app.run(debug=False)
