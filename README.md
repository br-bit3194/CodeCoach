# CodeCoach

The AI companion that helps you understand your code repo, perform enhancements, debug, and generate PRDs.

## Quick Demo & Docs

- Demo video: [Demo.mp4](Demo.mp4)
- Final PDF (paper/report): [CodeCoach-Final.pdf](CodeCoach-Final.pdf)
- Final slides (PPTX): [CodeCoach-Final.pptx](CodeCoach-Final.pptx)
- Sample PRD (markdown): [frontend/public/sample-prd.md](frontend/public/sample-prd.md)

## Quickstart

1. Backend
   - See backend notes: [backend/README.md](backend/README.md)
   - From repo root:
     ```sh
     cd backend
     # inside dev container / locally with Python 3.12+
     pip install -r requirements.txt
     uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
     ```
   - Upload a zipped codebase to: POST http://localhost:8000/api/upload_codebase

2. Frontend
   - See frontend notes: [frontend/README.md](frontend/README.md)
   - From repo root:
     ```sh
     cd frontend
     npm install
     npm run dev
     ```
   - Open the app at the Vite dev URL (usually http://localhost:5173).

## Project Structure (high level)

- backend/ — FastAPI service that ingests codebase zips, builds embeddings, and serves search APIs.
- frontend/ — React + Vite UI for uploading codebases and asking questions.
- QA/ — evaluation scripts and question bank.
- Demo and final artifacts at repo root: [Demo.mp4](Demo.mp4), [CodeCoach-Final.pdf](CodeCoach-Final.pdf), [CodeCoach-Final.pptx](CodeCoach-Final.pptx)

## Notes & Links

- Upload endpoint: `/api/upload_codebase` — implemented in [`backend/src/app.py`](backend/src/app.py)
- Search endpoint: `/api/search` — implemented in [`backend/src/app.py`](backend/src/app.py)
- PRD generation helpers: [`backend/src/services/prd.py`](backend/src/services/prd.py)
- FAISS embeddings builder: [`backend/src/services/embedding.py`](backend/src/services/embedding.py)

## License

Apache 2.0 — see [LICENSE](LICENSE)
