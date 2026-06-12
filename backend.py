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
        gast = data.get('gast', 'Gast')
        bestandsnaam = data.get('naam', 'foto.jpg')

        if not base64_file:
            return jsonify({'error': 'No file'}), 400

        # Decode base64
        try:
            file_bytes = base64.b64decode(base64_file)
        except:
            return jsonify({'error': 'Invalid base64'}), 400

        # Cloudinary upload - FLAT STRUCTURE WITH GAST NAME
        if CLOUDINARY_URL and cloudinary.config().cloud_name:
            try:
                # Clean gast name
                gast_clean = gast.strip().replace(' ', '').replace(',', '').lower()
                # Use parts from bestandsnaam (timestamp_counter)
                parts = bestandsnaam.replace('.jpg', '').split('_')
                ts = parts[0] if len(parts) > 0 else '0'
                ct = parts[1] if len(parts) > 1 else '0'

                # PUBLIC ID: ALWAYS INCLUDES GAST NAME
                public_id = f"bruiloft_{gast_clean}_{ts}_{ct}"

                result = cloudinary.uploader.upload(
                    io.BytesIO(file_bytes),
                    resource_type='auto',
                    public_id=public_id,
                    overwrite=False
                )
                file_id = result.get('public_id')
                file_url = result.get('secure_url')
            except Exception as e:
                return jsonify({'error': f'Upload error: {str(e)}'}), 500
        else:
            file_id = f"local_{bestandsnaam}"
            file_url = None

        # Log entry
        foto_log.append({
            'datum': datetime.now().isoformat(),
            'gast': gast,
            'bestand': bestandsnaam,
            'id': file_id,
            'url': file_url
        })

        return jsonify({
            'success': True,
            'id': file_id,
            'url': file_url,
            'gast_used': gast_name if 'gast_name' in locals() else 'ERROR'
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
