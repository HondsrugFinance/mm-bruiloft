from flask import Flask, request, jsonify
from flask_cors import CORS
from google.oauth2.service_account import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
import base64
import io
import json
import os
from datetime import datetime
import gspread

app = Flask(__name__)
CORS(app)

# Google credentials from environment variable
GOOGLE_CREDS_JSON = os.environ.get("GOOGLE_CREDENTIALS", "{}")
SPREADSHEET_ID = os.environ.get("SPREADSHEET_ID")

def get_google_credentials():
    """Load Google service account credentials"""
    try:
        creds_dict = json.loads(GOOGLE_CREDS_JSON)
        return Credentials.from_service_account_info(creds_dict)
    except:
        return None

def get_drive_service():
    creds = get_google_credentials()
    if not creds:
        return None
    return build('drive', 'v3', credentials=creds)

def get_sheets_service():
    creds = get_google_credentials()
    if not creds:
        return None
    return build('sheets', 'v4', credentials=creds)

def get_or_create_folder(service, folder_name, parent_id=None):
    """Get or create folder in Google Drive"""
    query = f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
    if parent_id:
        query += f" and '{parent_id}' in parents"

    results = service.files().list(q=query, spaces='drive', fields='files(id, name)', pageSize=1).execute()
    files = results.get('files', [])

    if files:
        return files[0]['id']

    # Create folder
    file_metadata = {
        'name': folder_name,
        'mimeType': 'application/vnd.google-apps.folder'
    }
    if parent_id:
        file_metadata['parents'] = [parent_id]

    folder = service.files().create(body=file_metadata, fields='id').execute()
    return folder.get('id')

@app.route('/upload', methods=['POST'])
def upload():
    try:
        data = request.json
        base64_file = data.get('file')
        gast = data.get('gast', 'Unknown')
        apparaat = data.get('apparaat', 'unknown')
        bestandsnaam = data.get('naam', 'foto.jpg')

        if not base64_file:
            return jsonify({'error': 'No file'}), 400

        # Decode base64
        try:
            file_bytes = base64.b64decode(base64_file)
        except:
            return jsonify({'error': 'Invalid base64'}), 400

        # Get Google Drive service
        service = get_drive_service()
        if not service:
            return jsonify({'error': 'Google Drive not configured'}), 500

        # Get or create MM_Bruiloft_Fotos folder
        main_folder_id = get_or_create_folder(service, 'MM_Bruiloft_Fotos')

        # Get or create device subfolder
        device_folder_id = get_or_create_folder(service, apparaat, main_folder_id)

        # Upload file
        file_metadata = {
            'name': bestandsnaam,
            'parents': [device_folder_id]
        }
        media = MediaIoBaseUpload(io.BytesIO(file_bytes), mimetype='image/jpeg', resumable=True)
        file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        file_id = file.get('id')

        # Log to Google Sheet
        if SPREADSHEET_ID:
            try:
                sheets_service = get_sheets_service()
                sheets_service.spreadsheets().values().append(
                    spreadsheetId=SPREADSHEET_ID,
                    range='Fotos!A:E',
                    valueInputOption='USER_ENTERED',
                    body={'values': [[datetime.now().isoformat(), gast, apparaat, bestandsnaam, file_id]]}
                ).execute()
            except:
                pass  # Sheet logging optional

        return jsonify({
            'success': True,
            'id': file_id,
            'pad': f"{apparaat}/{bestandsnaam}"
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run(debug=False)
