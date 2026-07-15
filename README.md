# Kreata Designs — Backend

FastAPI + PostgreSQL + Cloudinary backend for the Kreata Designs website.

## Stack

- **FastAPI** — REST API
- **PostgreSQL** (via SQLAlchemy) — database
- **Cloudinary** — image storage for the gallery
- **JWT** (python-jose + bcrypt) — admin authentication

## 1. Setup

```bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## 2. Configure environment variables

Copy `.env.example` to `.env` and fill in your real values:

```bash
cp .env.example .env
```

- `DATABASE_URL` — your PostgreSQL connection string, e.g.
  `postgresql://postgres:yourpassword@localhost:5432/kreatadesigns`
- `SECRET_KEY` — any long random string (used to sign JWT tokens)
- `ADMIN_USERNAME` / `ADMIN_PASSWORD` — the admin login created automatically the first time
  the app starts. **Change the password before going live.**
- `CLOUDINARY_CLOUD_NAME`, `CLOUDINARY_API_KEY`, `CLOUDINARY_API_SECRET` — from your Cloudinary
  dashboard (cloudinary.com → Settings → API Keys)
- `FRONTEND_URL` — your deployed frontend URL, for CORS (kreatadesigns.com and localhost:3000
  are already allowed by default)

## 3. Create the database

Make sure PostgreSQL is running and the database in `DATABASE_URL` exists, e.g.:

```bash
createdb kreatadesigns
```

Tables are created automatically on first startup — no separate migration step needed.

## 4. Run it

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

- API root: http://localhost:8000
- Interactive docs (Swagger UI): http://localhost:8000/docs

On first startup, an admin account is created automatically using `ADMIN_USERNAME` /
`ADMIN_PASSWORD` from your `.env`. A few sample testimonials are also seeded so the site
isn't empty — edit or delete them from the admin dashboard once you have real reviews.

## API overview

| Endpoint | Method | Auth | Purpose |
|---|---|---|---|
| `/api/auth/login` | POST | — | Admin login, returns a JWT |
| `/api/auth/me` | GET | Admin | Current admin details |
| `/api/gallery/` | GET | — | List gallery images |
| `/api/gallery/` | POST | Admin | Upload an image (multipart: `title`, `description`, `category`, `file`) |
| `/api/gallery/{id}` | DELETE | Admin | Delete an image |
| `/api/announcements/` | GET | — | List announcements (`?active_only=false` for all) |
| `/api/announcements/` | POST/PUT/DELETE | Admin | Manage announcements |
| `/api/testimonials/` | GET | — | List testimonials |
| `/api/testimonials/` | POST/PUT/DELETE | Admin | Manage testimonials |
| `/api/comments/` | POST | — | Visitors submit a message |
| `/api/comments/` | GET | Admin | View submitted messages |
| `/api/comments/{id}/read` | PATCH | Admin | Mark a message read |
| `/api/stats/` | GET | Admin | Dashboard summary counts |

## Deployment notes

- Any host that runs Python works (Render, Railway, Fly.io, a VPS, etc.). Start command:
  `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- Use a managed PostgreSQL instance in production (Render/Railway/Neon/Supabase all work fine).
- Set all the variables from `.env.example` in your host's environment settings — don't commit
  a real `.env` file.
- Consider adding Alembic migrations later if the schema needs to evolve after launch (this
  project uses `create_all()` on startup for simplicity, which is safe for new tables but won't
  auto-alter existing ones).
