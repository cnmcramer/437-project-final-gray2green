# Gray to Green Landscaping — Website

> Cloud Computing final project (437) — Full-stack landscaping website using 4 Google Cloud services.

## Live Site
Deployed on Google App Engine: `https://project-final-gray2green.uc.r.appspot.com/`

---

## Project Overview

A working prototype website for **Gray to Green**, a Metro Detroit landscaping company. Customers can:
- View all services offered
- Browse a gallery of completed projects
- Submit a quote request (with optional image upload)
- Schedule an appointment (auto-added to Google Calendar)

- **App Engine** hosts the Flask web app and handles all incoming HTTP requests, every page load and form submission runs through it.
- **Firestore** is the database, storing quote requests, appointment records, service listings, and gallery image metadata.
- **Cloud Storage** holds the actual image files customers upload with their quote requests, with the resulting file URL saved back into Firestore.
- **Google Calendar API** turns appointment form submissions into real calendar events, giving the business owner a usable schedule entry for every booking.

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | HTML5, CSS3, Vanilla JS |
| Backend | Python / Flask |
| Hosting | Google App Engine |
| Database | Google Cloud Firestore |
| File Storage | Google Cloud Storage |
| Scheduling | Google Calendar API |
| Version Control | GitHub |

---

## Project Structure

```
437-project-final-gray2green/
│
├── app.yaml                     # App Engine config
├── requirements.txt             # Python dependencies
├── README.md
├── .gitignore
│
├── app/
│   ├── main.py                  # Flask app entry point
│   ├── routes/
│   │   ├── quotes.py            # POST /api/quotes
│   │   ├── appointments.py      # POST /api/appointments
│   │   ├── gallery.py           # GET /api/gallery
│   │   └── services.py          # GET /api/services
│   │
│   ├── templates/
│   │   ├── index.html           # Homepage
│   │   ├── services.html        # Services page
│   │   ├── gallery.html         # Gallery page
│   │   ├── quote.html           # Quote request form
│   │   └── contact.html         # Contact + appointment form
│   │
│   ├── static/
│   │   ├── css/style.css        # Full design system
│   │   ├── js/main.js           # Form logic, gallery, API calls
│   │   └── images/              # Local images (logo, etc.)
│   │
│   └── services/
│       ├── firestore_service.py # Firestore CRUD helpers
│       ├── storage_service.py   # Cloud Storage upload helpers
│       └── calendar_service.py  # Google Calendar event creation
│
├── docs/
│   ├── api-contract.md          # Locked API spec
│   ├── firestore-plan.md        # DB collections & schema
│   └── deployment-notes.md      # Setup & deploy guide
│
└── sample_data/
    └── services.json            # Seed data reference
```

---

## Local Development

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app/main.py
```

Open `http://localhost:8080`

> Firestore, Storage, and Calendar are mocked in local dev — no credentials needed to run the site.

---

## API Endpoints

| Method | Route | Description |
|--------|-------|-------------|
| GET | `/api/services` | List all services |
| GET | `/api/gallery` | List gallery images |
| POST | `/api/quotes` | Submit a quote request |
| POST | `/api/appointments` | Schedule an appointment |

See `docs/api-contract.md` for full request/response specs.

---

## Deployment

```bash
gcloud app deploy
```

See `docs/deployment-notes.md` for full setup instructions.

---

## Disclaimer

*This code was created with the assistance of Claude, an AI assistant made by Anthropic. All code has been reviewed and tested for correctness.*

---

## Business Info

**Gray to Green Landscaping**
- 📞 248-412-3767
- ✉️ graytogreen.services@gmail.com
- 📍 Metro Detroit, MI (based near Royal Oak)
- [Google](https://g.page/r/10eyR3NRwzQavEArj) | [Instagram](https://www.instagram.com/graytogreenlandscaping) | [Facebook](https://www.facebook.com/share/1DL8rRZTFi/) | [TikTok](https://www.tiktok.com/@graytogreenlandscaping)
