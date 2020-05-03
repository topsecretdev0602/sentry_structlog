Just some experiments with a minimal Django app for running [sentry](https://sentry.io/) along with [structlog](structlog.org) json logging setup

JSON structured messages make sentry issues and breadcrumbs hard to read, but are great for parsing and aggregating in ELK stack. 
We do some hacking around with structlog and sentry internals to make them work together nicely

Other related projects:

- [structlog-sentry](https://github.com/kiwicom/structlog-sentry)

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

6. Go create errors
    - http://0.0.0.0:8000/app/structlog
    - http://0.0.0.0:8000/app/stdlib

7. Go explore the code. 