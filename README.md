# CareerPilot AI

CareerPilot AI is a Flask-based career toolkit with a premium dark UI. It includes resume parsing and checklist scoring, skill detection, improvement suggestions, job-description matching, interview preparation, a job application tracker, and downloadable PDF reports.

## What works without an AI API

- Registration, login, password hashing, and per-user data separation
- PDF, DOCX, and TXT resume parsing
- Rule-based resume checklist score and improvement suggestions
- Skill extraction and job description skill matching
- Job tracker with status updates and delete
- PDF report generation
- Interview question fallback
- Error handling for invalid files, large uploads, missing records, and database constraints

## Optional free-tier AI

Groq powers AI feedback for job matching and interview preparation when a user supplies their own API key. The app works without it. Free tier availability and rate limits can change. Do not put an API key in frontend code or commit `.env`.

## Windows + VS Code setup

1. Install Python 3.11 or 3.12 from python.org. During installation, enable **Add Python to PATH**.
2. Extract this project ZIP.
3. Open the extracted `CareerPilot-AI` folder in VS Code.
4. Open Terminal → New Terminal.
5. Create and activate a virtual environment:

   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

   If PowerShell blocks activation, use Command Prompt terminal:

   ```bat
   .venv\Scripts\activate.bat
   ```

6. Install dependencies:

   ```powershell
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```

7. Copy `.env.example` to `.env`. In PowerShell:

   ```powershell
   Copy-Item .env.example .env
   ```

8. Optional AI setup: create your own key in the official Groq Console and add it to `.env` as `GROQ_API_KEY=your_real_key`. If you leave it blank, offline fallback features still work.
9. Run the app:

   ```powershell
   python app.py
   ```

10. Open `http://127.0.0.1:5000`.

The database and temporary uploads are created automatically under `instance/`. Uploaded resumes are deleted from the temporary upload folder after extraction; extracted text and analysis history are stored in the local SQLite database for the logged-in user.

## Main pages

- `/` — landing page
- `/register` and `/login` — account access
- `/dashboard` — recent activity
- `/analyze` — upload and analyze a resume
- `/analysis/<id>` — report and suggestions
- `/analysis/<id>/match` — paste a job description
- `/interview` — interview practice
- `/jobs` — application tracker

## API behavior and limitations

- The score is a transparent resume checklist score, not a real ATS vendor score or a hiring prediction.
- Skill matching checks the skills in the built-in dictionary. It cannot understand every synonym or context.
- Scanned/image-only PDFs may not contain extractable text. Use OCR separately or upload a text-based PDF/DOCX/TXT.
- AI responses require internet access and a valid Groq API key. Timeouts, invalid keys, and rate limits are handled with messages and offline fallbacks.
- Job listings are not fetched from an external jobs API. The job tracker stores jobs you enter yourself; this avoids fake or unreliable live job listings and keeps the project free to run.
- Local SQLite is suitable for a demo and small personal deployment. For a multi-user production deployment, use managed PostgreSQL, secure cookie settings, HTTPS, backups, and a persistent disk.

## Quick checks

1. Register a new account.
2. Log out and log back in.
3. Upload a text-based PDF, DOCX, or TXT resume.
4. Open the analysis report and download the PDF.
5. Paste a job description of at least 40 characters into Job Match.
6. Generate interview questions with and without `GROQ_API_KEY`.
7. Save a job, update its status, and delete it.
8. Create a second account and verify the first account's analyses/jobs are not visible.
9. Try an unsupported file type and a file over 5 MB; the app should show a clear message.

## Deployment notes

A simple demo can be deployed to a Python host that supports Flask/Gunicorn. Set these environment variables in the host dashboard:
- `FLASK_SECRET_KEY` — long random secret
- `GROQ_API_KEY` — optional
- `GROQ_MODEL` — optional

Start command:

```bash
gunicorn app:app
```

**Persistence warning:** some free hosting plans use ephemeral filesystems and may delete SQLite data after restart/redeploy. Use a persistent disk or managed PostgreSQL for persistent accounts and analysis history. Never deploy with Flask debug mode enabled. Confirm the hosting provider's current free-plan and persistent-storage policies before choosing it.
