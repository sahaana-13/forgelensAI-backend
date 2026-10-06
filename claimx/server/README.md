# CLAIMX — AI-Powered Digital Accident Reporting & Insurance FNOL Platform

**Tagline:** From Accident to Evidence-Ready Claim.

## Stack
- React.js + Vite + normal CSS
- FastAPI + SQLAlchemy
- PostgreSQL + psycopg2 (synchronous SQLAlchemy engine)
- Gemini 2.5 Flash through the Google GenAI SDK
- JWT + bcrypt
- Leaflet, Recharts, Lucide React
- ReportLab PDF generation

## Architecture
React → FastAPI → PostgreSQL / Gemini 2.5 → FNOL → PDF.

## PostgreSQL setup
Create the database first:

```sql
CREATE DATABASE claimx;
```

Copy `.env.example` to `.env` and update `DATABASE_URL`, `JWT_SECRET`, and `GEMINI_API_KEY`.
`DATABASE_URL` must point to the dedicated ClaimX database (for example,
`postgresql+psycopg2://<user>:<password>@localhost:5432/claimx`), not to an
unrelated database that happens to contain a `users` table.

## Backend
```bash
cd server
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python -m app.seed
uvicorn app.main:app --reload --port 8000
```

API docs: http://localhost:8000/docs

## Frontend
```bash
cd client
npm install
npm run dev
```

## Demo credentials
- Admin: `admin@claimx.com` / `Admin@123`
- Claimant: `user@claimx.com` / `User@123`

All seed identities and accidents are fictional.

## Important neutrality boundary
CLAIMX organizes reported information and evidence. It does not determine liability, fraud, coverage eligibility, claim approval/rejection, reserves, settlement amounts, or legal conclusions. AI output requires human verification.

## API highlights
- `/api/auth/register`, `/api/auth/login`, `/api/auth/me`
- `/api/profile`
- `/api/vehicles`
- `/api/insurance`
- `/api/accidents`, `/api/accidents/sos`
- `/api/accidents/{id}/evidence`
- `/api/interviews/start`, `/api/interviews/{id}/message`
- `/api/accidents/{id}/compare-statements`
- `/api/accidents/{id}/analyze-evidence`
- `/api/accidents/{id}/missing-information`
- `/api/accidents/{id}/fnol`, `/api/accidents/{id}/fnol/pdf`
- `/api/admin/dashboard`

## Known limitations
- Browser GPS/camera permissions depend on device/browser.
- Uploaded files are stored locally for the prototype.
- Gemini requires a valid API key; without one, the interview returns a configuration message rather than fabricated AI output.
- The prototype uses SQLAlchemy table creation during development rather than Alembic migrations.
