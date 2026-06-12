# Setup Instructies — Mike & Martine Foto App

## Fase 1: Google Drive Credentials (5 min)

1. **Google Cloud Console:** https://console.cloud.google.com
2. New Project → "MM Bruiloft"
3. **Enable APIs:**
   - Search "Google Drive API" → Enable
   - Search "Google Sheets API" → Enable
4. **Service Account:**
   - Ga naar "Service Accounts"
   - Create Service Account → "mm-bruiloft"
   - Grant access: "Editor"
5. **Keys:**
   - Click account → "Keys" tab
   - Add Key → JSON
   - **Save het JSON bestand** (dit is je `GOOGLE_CREDENTIALS`)

## Fase 2: Deploy op Render (5 min)

1. **Render.com:** https://render.com (login/signup)
2. **New Web Service** → Connect GitHub repo: `HondsrugFinance/mm-bruiloft`
3. **Settings:**
   - Name: `mm-bruiloft-api`
   - Runtime: Python
   - Build: `pip install -r requirements.txt`
   - Start: `gunicorn backend:app`
4. **Environment Variables:**
   - `GOOGLE_CREDENTIALS` = **Inhoud van je JSON bestand** (copy-paste hele file)
   - `SPREADSHEET_ID` = (laat leeg voor nu, optional)
5. Deploy!
6. **Kopieer de URL** (bijv: `https://mm-bruiloft-api.onrender.com`)

## Fase 3: Update Frontend URL (2 min)

1. **index.html** → Regel ~51:
```javascript
const API_URL = "https://mm-bruiloft-api.onrender.com/upload";
```
(vervang met jouw Render URL)

2. Commit & push naar GitHub

## Fase 4: Test (1 min)

- App: https://hondsrugfinance.github.io/mm-bruiloft/
- Voer naam in → Maak foto → Check Google Drive `MM_Bruiloft_Fotos` folder

## (Optional) Google Sheet Logging

Wil je foto metadata in een Google Sheet?

1. Create Google Sheet → Zet kolommen: "Datum", "Gast", "Apparaat", "Bestand", "Drive ID"
2. Copy de Sheet ID (URL: `/spreadsheets/d/SHEET_ID/edit`)
3. Render env var: `SPREADSHEET_ID = SHEET_ID`
4. Restart Render service

## Troubleshooting

- **"Google Drive not configured"** → Check GOOGLE_CREDENTIALS env var
- **Folder niet zichtbaar** → Service account email moet Drive access hebben
- **App URL zwart** → Wacht 1 min op GitHub Pages deploy
