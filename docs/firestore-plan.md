# Firestore Plan — Gray to Green Landscaping

## Collections

---

### `quoteRequests`

Stores all quote requests submitted via the website form.

**Document fields:**

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `fullName` | string | ✅ | Customer full name |
| `phone` | string | ✅ | Customer phone number |
| `email` | string | ✅ | Customer email |
| `address` | string | | Property address |
| `serviceId` | string | ✅ | Service ID (see api-contract.md) |
| `lawnSize` | string | | small / medium / large / xlarge / unsure |
| `description` | string | | Customer's description of the project |
| `preferredDate` | string | | ISO date string (YYYY-MM-DD) |
| `imageUrls` | array | | Public URLs of uploaded images (Cloud Storage) |
| `status` | string | | `new`, `contacted`, `quoted`, `closed` |
| `createdAt` | timestamp | | Set automatically on save |

---

### `appointments`

Stores appointment requests and links to Google Calendar events.

**Document fields:**

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `fullName` | string | ✅ | Customer full name |
| `phone` | string | ✅ | Customer phone |
| `email` | string | | Customer email |
| `address` | string | | Property address |
| `serviceId` | string | ✅ | Service ID |
| `appointmentDate` | string | ✅ | ISO date (YYYY-MM-DD) |
| `appointmentTime` | string | | e.g. `10:00 AM` |
| `notes` | string | | Gate codes, special access info |
| `calendarEventId` | string | | Google Calendar event ID (added post-creation) |
| `status` | string | | `pending`, `confirmed`, `completed`, `cancelled` |
| `createdAt` | timestamp | | Set automatically on save |

---

### `services`

Stores the list of services offered. Can be seeded via `firestore_service.seed_services()`.

**Document fields:**

| Field | Type | Notes |
|-------|------|-------|
| `id` | string | Document ID = service slug (e.g. `mulch-installation`) |
| `name` | string | Display name |
| `icon` | string | Emoji icon |
| `description` | string | Short description |
| `tag` | string | Badge label (e.g. "Most Popular") |
| `order` | number | Display order |

---

### `galleryImages`

Stores metadata for gallery images uploaded to Cloud Storage.

**Document fields:**

| Field | Type | Notes |
|-------|------|-------|
| `title` | string | Display title |
| `label` | string | Service label (e.g. "Mulch Installation") |
| `category` | string | Filter category slug (e.g. `mulch`, `hardscape`) |
| `imageUrl` | string | Public Cloud Storage URL |
| `beforeAfter` | boolean | Whether to show "Before & After" badge |
| `order` | number | Display order |
| `createdAt` | timestamp | Upload timestamp |

---

## Indexes

Firestore auto-indexes single-field queries. Composite indexes needed:

- `appointments` — `status` + `appointmentDate` (for admin queries)
- `galleryImages` — `category` + `order` (for filtered gallery)

Create these in the Firebase Console under **Firestore > Indexes** if needed.

---

## Security Rules (recommended)

```
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {

    // Public read for services and gallery
    match /services/{doc} {
      allow read: if true;
      allow write: if false; // admin only
    }

    match /galleryImages/{doc} {
      allow read: if true;
      allow write: if false; // admin only
    }

    // Write-only for form submissions (no read from client)
    match /quoteRequests/{doc} {
      allow create: if true;
      allow read, update, delete: if false;
    }

    match /appointments/{doc} {
      allow create: if true;
      allow read, update, delete: if false;
    }
  }
}
```
