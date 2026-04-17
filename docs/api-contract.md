# API Contract — Gray to Green Landscaping

> **DO NOT change route names or field names without updating this document and notifying both frontend and backend.**

---

## Base URL

- **Local dev:** `http://localhost:8080`
- **Production:** `https://<project-id>.appspot.com`

---

## Standard Response Format

All endpoints return JSON with this structure:

```json
{
  "success": true,
  "message": "Human-readable message"
}
```

On error:
```json
{
  "success": false,
  "message": "Description of what went wrong"
}
```

---

## Endpoints

### GET /api/services

Returns all available landscaping services.

**Response:**
```json
{
  "success": true,
  "message": "Services retrieved successfully.",
  "services": [
    {
      "id": "mulch-installation",
      "name": "Mulch Installation",
      "icon": "🍂",
      "description": "Fresh mulch installation...",
      "tag": "Most Popular",
      "order": 1
    }
  ]
}
```

---

### GET /api/gallery

Returns gallery image records.

**Response:**
```json
{
  "success": true,
  "message": "Gallery retrieved successfully.",
  "images": [
    {
      "id": "abc123",
      "title": "Front Bed Mulch",
      "label": "Mulch Installation",
      "category": "mulch",
      "imageUrl": "https://storage.googleapis.com/...",
      "beforeAfter": true,
      "order": 1
    }
  ]
}
```

---

### POST /api/quotes

Submit a quote request.

**Request body (JSON):**
```json
{
  "fullName": "John Smith",
  "phone": "248-555-1111",
  "email": "john@example.com",
  "address": "123 Main St, Royal Oak, MI",
  "serviceId": "mulch-installation",
  "lawnSize": "medium",
  "description": "Need cleanup and mulch in front beds.",
  "preferredDate": "2026-04-20"
}
```

**Required fields:** `fullName`, `phone`, `email`, `serviceId`

**Optional:** `address`, `lawnSize`, `description`, `preferredDate`

**Image upload:** Send as `multipart/form-data` with field name `projectImages` (multiple files allowed).

**Success Response (201):**
```json
{
  "success": true,
  "message": "Quote request received! We'll reach out within 24 hours.",
  "id": "firestore-doc-id"
}
```

---

### POST /api/appointments

Submit an appointment request. Also creates a Google Calendar event.

**Request body (JSON):**
```json
{
  "fullName": "John Smith",
  "phone": "248-555-1111",
  "email": "john@example.com",
  "address": "123 Main St, Royal Oak, MI",
  "serviceId": "mulch-installation",
  "appointmentDate": "2026-04-22",
  "appointmentTime": "10:00 AM",
  "notes": "Gate is unlocked. Use side entrance."
}
```

**Required fields:** `fullName`, `phone`, `serviceId`, `appointmentDate`

**Success Response (201):**
```json
{
  "success": true,
  "message": "Appointment requested! We'll confirm shortly.",
  "id": "firestore-doc-id",
  "calendarEventId": "google-calendar-event-id"
}
```

---

## Service IDs (locked — do not rename)

| ID | Display Name |
|----|-------------|
| `mulch-installation` | Mulch Installation |
| `lawn-care` | Lawn Care & Maintenance |
| `landscape-design` | Landscape Design |
| `hardscaping` | Hardscaping |
| `tree-shrub-trimming` | Tree & Shrub Trimming |
| `clean-ups` | Fall & Spring Clean-Ups |
| `rock-stone` | Rock & Stone Installation |
| `sod-installation` | Sod Installation |

---

## Lawn Size Values

| Value | Label |
|-------|-------|
| `small` | Small (under 1/4 acre) |
| `medium` | Medium (1/4 – 1/2 acre) |
| `large` | Large (1/2 – 1 acre) |
| `xlarge` | Extra Large (1+ acre) |
| `unsure` | Not sure |

---

## Gallery Categories (for filter buttons)

| Value | Display |
|-------|---------|
| `mulch` | Mulch |
| `design` | Landscape Design |
| `hardscape` | Hardscaping |
| `cleanup` | Clean-Ups |
| `trimming` | Trimming |

---

*Last updated: 2025. Any changes to this contract must be documented here before modifying code.*
