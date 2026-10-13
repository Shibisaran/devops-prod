# Simple Login App (Django + PostgreSQL)

A small login portal with:

- Frontend: Django templates + CSS
- Backend: Python Django
- Database: PostgreSQL
- Tests: 8 pytest cases
- CI: Jenkinsfile ready for GitHub SCM

Demo login after first migrate:

- Username: `demo`
- Password: `demo1234`

## Project layout

```
config/          Django project settings
accounts/        Login views, forms, URLs
templates/       Login and dashboard pages
static/css/      Frontend styles
tests/           pytest test cases
Jenkinsfile      Jenkins pipeline
docker-compose.yml
```

Recommended Python: 3.12 or newer. Docker uses Python 3.12.

## Local setup (without Docker)

1. Create and start PostgreSQL, then create database `login_db`.
2. Copy environment values:

```bash
cp .env.example .env
```

3. Install dependencies and run:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
export $(grep -v '^#' .env | xargs)
python manage.py migrate
python manage.py ensure_demo_user
python manage.py runserver
```

Open http://127.0.0.1:8000/

## Run with Docker + PostgreSQL

```bash
docker compose up --build
```

App: http://127.0.0.1:8000/  
Postgres: `localhost:5432` (`login_db` / `login_user` / `login_pass`)

## Tests

Jenkins and local pytest use SQLite so CI does not need a live Postgres instance. The running app still uses PostgreSQL.

```bash
source .venv/bin/activate
pip install -r requirements-dev.txt
pytest
```

The eight cases cover:

1. Login page loads
2. Username, password, and CSRF fields render
3. Valid credentials redirect to dashboard
4. Wrong password shows an error
5. Unknown user cannot log in
6. Empty fields fail validation
7. Dashboard requires login
8. Logout ends the session

## GitHub

```bash
git init
git add .
git commit -m "Add Django login app with pytest and Jenkins pipeline"
git branch -M main
git remote add origin https://github.com/<your-user>/<your-repo>.git
git push -u origin main
```

Do not commit `.env`. Keep secrets in Jenkins credentials or your host environment.

## Jenkins (pull from GitHub)

1. Install Jenkins plugins: **Pipeline**, **Git**, **JUnit**.
2. On GitHub, create a Personal Access Token (or use SSH keys) with repo read access.
3. In Jenkins: **Manage Jenkins → Credentials** and add the GitHub token or SSH key.
4. **New Item → Pipeline**.
5. Under **Pipeline**, choose **Pipeline script from SCM**.
   - SCM: Git
   - Repository URL: your GitHub repo
   - Credentials: the credential from step 3
   - Branch: `*/main`
   - Script Path: `Jenkinsfile`
6. Optional webhook: GitHub repo **Settings → Webhooks →** Jenkins URL  
   `http://<jenkins-host>:8080/github-webhook/`
7. Make sure the Jenkins agent has `python3`, `python3-venv`, and `pip`.
8. Run **Build Now**. Pytest results appear in the Jenkins test report from `reports/junit.xml`.
