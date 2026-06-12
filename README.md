# Mike & Martine — Foto Upload App

PWA + Cloudinary backend. **Volledige setup in ~5 minuten.**

## Snel Deploy

### Stap 1: Cloudinary Account (1 min)

https://cloudinary.com/users/register/free (gratis!) → Copy Environment Variable

### Stap 2: Deploy Backend op Render (3 min)

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/HondsrugFinance/mm-bruiloft)

Bij "Environment Variables":
- `CLOUDINARY_URL` = Plak hier je Cloudinary Environment Variable (uit Stap 1)

### Stap 3: Update Frontend URL (1 min)

In **index.html** regel ~51:
```javascript
const API_URL = "https://JOUW-RENDER-URL.onrender.com/upload";
```

Git commit & push.

---

## App URLs

- **Upload app:** https://hondsrugfinance.github.io/mm-bruiloft/
- **QR kaartje:** https://hondsrugfinance.github.io/mm-bruiloft/qr-kaartje.html
- **Backend stats:** https://JOUW-RENDER-URL.onrender.com/stats

## Hoe Werkt Het

1. Guest opent app → voert naam in → maakt max 10 foto's
2. Foto wordt gecomprimeerd → verstuurd naar backend
3. Backend slaat op in Cloudinary (cloud storage)
4. Service worker cacht alles (werkt offline)

## QR Kaartje (Print Dit)

1. Open qr-kaartje.html
2. Voer de app URL in
3. "Maak QR" → "Print" → PDF → Print op A6 (10×15cm)

## Stats

Alle backend logs:
```
GET https://JOUW-RENDER-URL.onrender.com/stats
```

Response:
```json
{
  "total_fotos": 45,
  "unique_devices": 23,
  "gasten": ["Alice", "Bob", ...]
}
```
