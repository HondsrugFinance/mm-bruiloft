# Mike & Martine — Foto Upload App

PWA voor bruiloft fotoupload via Google Drive.

## Files

- **index.html** — Main app (foto upload)
- **qr-kaartje.html** — QR code tafelkaartje (print dit)
- **sw.js** — Service worker (offline cache)
- **manifest.json** — PWA manifest
- **google-apps-script.gs** — Backend (Google Drive + Sheet)

## Deploy

### Backend (Google Apps Script)

1. Ga naar Google Apps Script: https://script.google.com
2. Nieuw project → Kopieeer inhoud van `google-apps-script.gs`
3. Deploy → New → Web app
   - Execute as: **Me** (jouw account)
   - Allow access: **Anyone**
4. Kopieer de URL en plak in **index.html** regel 51: `const API_URL = "..."`

### Frontend (GitHub Pages)

1. Zet deze folder op GitHub
2. Enable Pages → Deploy from main branch
3. URL: `https://hondsrugfinance.github.io/mm-bruiloft/`

## QR Code Kaartje

1. Open `qr-kaartje.html`
2. Voer de app URL in
3. Click "Maak QR"
4. Click "Print" → Save as PDF
5. Print op A6 (of 10×15cm)

## Hoe Werkt Het

1. **Guest** → App opent → Voert naam in → Maakt foto's
2. **App** → Comprimeert foto → Base64 → POST naar Google Apps Script
3. **Backend** → Decodeert → Slaat op in Google Drive folder `MM_Bruiloft_Fotos/{apparaat_id}`
4. **Sheet** → Logt datum/gast/bestand in Google Sheet
5. **Offline** → Als WiFi uit → Wachten in IndexedDB → Auto-retry als online

## Troubleshooting

- **"Upload Error"** → Check API URL in index.html
- **Google Drive folder niet zichtbaar** → Check Google Apps Script execution
- **QR code werkt niet** → Controleer URL spelling
