# Setup — Mike & Martine Foto App

**Minimale setup!** Alleen Cloudinary (gratis).

## 1. Cloudinary Account (2 min)

1. Go to: https://cloudinary.com/users/register/free
2. Sign up (gratis)
3. Dashboard → **Environment Variable kopieëren** (iets als: `cloudinary://123456:abc@xyz`)

## 2. Deploy op Render (3 min)

1. https://render.com → New Web Service
2. Connect GitHub: `HondsrugFinance/mm-bruiloft`
3. Settings:
   - **Name:** `mm-bruiloft-api`
   - **Runtime:** Python
   - **Build:** `pip install -r requirements.txt`
   - **Start:** `gunicorn backend:app`
4. **Environment Variable:**
   - Key: `CLOUDINARY_URL`
   - Value: Plak je Cloudinary Environment Variable (uit stap 1)
5. **Deploy!**
6. Kopieer de Render URL (bijv: `https://mm-bruiloft-api.onrender.com`)

## 3. Update Frontend (2 min)

In **index.html** regel ~51, vervang de API_URL:
```javascript
const API_URL = "https://mm-bruiloft-api.onrender.com/upload";
```

Commit & push naar GitHub.

## 4. Test! (1 min)

- Open: https://hondsrugfinance.github.io/mm-bruiloft/
- Voer naam in
- Maak foto
- Check Cloudinary dashboard → Media Library → mm-bruiloft folder

## Stats Endpoint

Backend biedt ook een stats endpoint:
```
https://mm-bruiloft-api.onrender.com/stats
```

Dit toont totaal fotos, unique devices, en gast namen.

## Troubleshooting

- **"Upload failed"** → Check Cloudinary URL in Render env vars
- **Fotos niet zichtbaar** → Wacht 1 min op Cloudinary sync
- **App URL zwart** → Wacht 1 min op GitHub Pages deploy
- **API error** → Check Render logs: `https://dashboard.render.com`
