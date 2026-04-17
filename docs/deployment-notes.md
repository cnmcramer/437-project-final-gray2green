# Deployment Notes — Gray to Green Landscaping

## Local Development

### Prerequisites
- Python 3.12+
- Google Cloud SDK (`gcloud`) installed and authenticated

### Setup

```bash
# Clone the repo
git clone <repo-url>
cd 437-project-final-gray2green

# Create virtual environment
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run locally
python app/main.py
# → http://localhost:8080
```

> The app runs fully in "local dev mode" — Firestore, Cloud Storage, and Calendar will log
> messages instead of making real API calls. No credentials needed to run and test the UI.

---

## Google Cloud Setup

### 1. Create a GCP Project

```bash
gcloud projects create gray-to-green-landscaping
gcloud config set project gray-to-green-landscaping
```

### 2. Enable Required APIs

```bash
gcloud services enable \
  appengine.googleapis.com \
  firestore.googleapis.com \
  storage.googleapis.com \
  calendar-json.googleapis.com
```

### 3. Create Firestore Database

In the GCP Console:
- Go to **Firestore** → **Create Database**
- Choose **Native mode**
- Select region: `us-central1`

Seed the services collection (run once):
```python
from app.services.firestore_service import seed_services
seed_services()
```

### 4. Create Cloud Storage Bucket

```bash
gsutil mb -l us-central1 gs://gray-to-green-uploads
gsutil defacl set public-read gs://gray-to-green-uploads
```

Update `GCS_BUCKET` in `app.yaml` to match.

### 5. Google Calendar API

- Go to GCP Console → **APIs & Services** → **Credentials**
- Create a **Service Account**
- Download the JSON key → save as `service_account.json` in project root
- Share your Google Calendar with the service account email (give "Make changes to events" permission)
- Update `GOOGLE_CALENDAR_ID` in `app.yaml` with your calendar ID

> ⚠️ Do NOT commit `service_account.json` to Git. It's in `.gitignore`.

---

## Deploy to App Engine

```bash
# Make sure you're authenticated
gcloud auth login
gcloud config set project <your-project-id>

# Deploy
gcloud app deploy

# View the live app
gcloud app browse
```

### First deploy checklist:
- [ ] `app.yaml` has correct `GCS_BUCKET` and `GOOGLE_CALENDAR_ID`
- [ ] Firestore database created
- [ ] Cloud Storage bucket created with public-read ACL
- [ ] Service account created and Calendar shared
- [ ] `requirements.txt` is up to date

---

## Environment Variables

Set in `app.yaml` under `env_variables`:

| Variable | Description |
|----------|-------------|
| `GCS_BUCKET` | Cloud Storage bucket name |
| `GOOGLE_CALENDAR_ID` | Google Calendar ID (e.g. `primary` or full email) |

On App Engine, the app uses **Application Default Credentials** automatically — no service account JSON file needed in production.

---

## Branch Strategy

| Branch | Owner | Purpose |
|--------|-------|---------|
| `main` | Both | Stable, deployable code |
| `frontend-caleb` | Caleb | HTML/CSS/JS work |
| `backend` | Gabe | Flask/Firestore/APIs |

**Merge flow:** feature branch → PR → review → merge to main → deploy

---

## Testing API Endpoints

```bash
# Test services
curl http://localhost:8080/api/services

# Test quote submission
curl -X POST http://localhost:8080/api/quotes \
  -H "Content-Type: application/json" \
  -d '{"fullName":"Test User","phone":"248-555-0000","email":"test@test.com","serviceId":"mulch-installation"}'

# Test appointment
curl -X POST http://localhost:8080/api/appointments \
  -H "Content-Type: application/json" \
  -d '{"fullName":"Test User","phone":"248-555-0000","serviceId":"lawn-care","appointmentDate":"2026-05-01"}'
```
