Just some experiments with a minimal Django app for running [sentry](https://sentry.io/) along with [structlog](structlog.org) json logging setup

---

To run (sorry no docker or uwsgi here):

Needs Python 3.6+

1. Install requirements (preferrably in a virtual environment)

    ```shell
    pip install -r requirements.txt
    ```

2. Sign up for sentry, create a project and get a DSN

3. Copy `.env.template` to `.env`

    ```shell
    cp .env.template .env
    ```

4. Edit `.env` with your favorite editor and paste your Sentry DSN

    ```
    SENTRY_DSN=https://{...}@{...}.ingest.sentry.io/{...}
    ```

5. Run the dev server
 
    ```shell
    python manage.py runserver 0.0.0.0:8000
    ```

6. Go to http://0.0.0.0:8000

7. Go explore the code at `app/`, create errors