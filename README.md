# OBMS
A simple Django + postgres starter app. Includes cli. </br>
**Note: Uses the built-in Django frontend.**

## Startup instructions
### System Requirements
- [Docker](https://www.docker.com/products/docker-desktop/)

### Starting the application
- Add a `.env` file to the root of the project.
    - Should have:
        - `POSTGRES_DB=<postgres-db>`
        - `POSTGRES_PASSWORD=<postgres-pw>`
        - `POSTGRES_NAME=<postgres-name>`
        - `POSTGRES_USER=<postgres-user>`
        - `DJANGO_SUPERUSER_USERNAME=<superuser_username>`
        - `DJANGO_SUPERUSER_EMAIL=<superuser_email>`
        - `DJANGO_SUPERUSER_PASSWORD=<superuser_pw>`
- If you want to run locally (not recommended):
    - virtualenv (`python3 -m pip install --user virtualenv`)
        - Then, navigate to root of git project
        - `python3 -m virtualenv <env-name>`
    - Run `pip install -r requirements.txt` inside your virtualenv
    - Change settings.py `DATABASES` var in the django project to your postgres name, user, password, and host to localhost.
- To run containerized, first start Docker:
    - On the first run, navigate to root of project and run `docker compose up --build`.
    - On subsequent runs, just run `docker compose up`.
- Navigate to `127.0.0.1:8000` to view the web app.
- Run `obms` in the app container to access the CLI.
