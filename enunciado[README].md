# LogMeal — Full-stack Technical Take-Home (Spec-Only Pack)

**Submission window:** 48 h · **Estimated effort:** 6–8 h

Implement a small **API + Front-end** to upload images, list them, and analyse one image by id — plus the **Share Link (10min TTL)** feature.

## What you must build

- Backend (using Python Flask) with at least these endpoints (see `docs/openapi.yaml` documentation):
  - `POST /api/upload_image`
  - `GET  /api/list_images`
  - `POST /api/analyse_image` (must return some information about the image)
  - `POST /api/share_image` (returns `{ token, url, expires_at }`)
  - `GET  /s/{token}` (public HTML page with OG tags)

- Front-end (using at least HTML + CSS + JS) that lets a user:
  - Upload an image, list images, analyse an image.
  - Generate and open a **share link**.

- Containers: `docker-compose up --build` must bring up frontend (3000) and backend (8000) without extra steps (see Docker Compose https://docs.docker.com/compose/).

- README.md file explaining what you developed and including the instructions of how to run the code.

- Submit the code in a Gitlab or Github repository.

## Optional extra tasks

- Basic test suite (pytest or similar) and coverage ≥60%. Include inside 'tests' folder.
- Serve Swagger UI from the backend (using `docs/openapi.yaml`).
- CI (GitHub Actions) that builds containers and runs tests.
- S3-compatible storage (e.g., MinIO in docker-compose).
- i18n EN/ES in the frontend using JSON string tables.
- Strict typing (mypy/tsc) with no errors.

## Fair play

- Do not exceed 6–8 h of effort.
- You may change technologies if you explain it in the README.
- Keep commits small and meaningful.
