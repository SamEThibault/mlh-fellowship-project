# Production Engineering - Portfolio Site

## Inspiration
With the help of [Luke](https://github.com/lukecheseldine) and [Mustafa](https://github.com/Mustaballer), this portfolio site was born during the first week of our MLH Fellowship's Orientation Hackathon. We wanted to build a website with an intuitive structure to prioritize UX. 

## What it does
This is a portfolio website with a modular design built as a template for others to add their information in JSON format or from a database table, and be able to display it through this application. Multiple scripts are added for convenience such as unit and integration tests, API endpoint tests, and a re-deployment script. These are all leveraged through GitHub actions to create a CI/CD pipeline that tests code from pull requests, and re-deploys on pushes to main.

The Flask application, MariaDB database, and NGINX reverse proxy are all containerized and orchestrated by Docker. The image configuration files are included and should be used for quick and easy deployment (see below).

NGINX is used as a reverse proxy to serve data utilizing the SSL protocol and to limit the rate of connections to target endpoints. Its configuration file is found inside the `user_conf.d` folder.

## How it was built
- Flask
- Jinja
- HTML
- CSS
- JavaScript
- Bootstrap V5.0
- NGINX
- MariaDB / MySQL
- Docker

## Requirements
- Git
- Python => 3.0 (dev)
- Venv          (dev)
- Docker        (prod)
- MySQL Server  (dev)

## Installation (Development)
The application is currently deployed on a CentOS server [right here!](http://samthibault.live) The Bash redeploy script is included for the user's convenience to re-base and deploy the most recent version of the application with a single command.

An example.env file is provided @ root: the user should create a .env file at the root of the project following the conventions outlined in that file.
For testing purposes, set up a local MySQL server / in-memory SQLite database to handle the requests and set the MYSQL_HOST environment variable accordingly.
For deployment, the MariaDB container will be spun up as part of the deployment process (see below). The user must still specify the database host in the .env file as follows: `MYSQL_HOST=mysql`

### Mac/Linux
1. Clone the repo via ssh: `git clone git@github.com:MLH-Fellowship/project-team-jungle.git`

2. Create a virtual environment with venv: `python3 -m venv`

3. Activate the virtual environment: `source venv/bin/activate`

4. Install dependencies: `pip3 install -r requirements.txt`

5. Run Flask server: `flask run`

6. Go to `http://127.0.0.1:5000/` in the browser

### Windows
1. Clone the repo via ssh: `git clone git@github.com:MLH-Fellowship/project-team-jungle.git`

2. Create a virtual environment with venv: `python3 -m venv`

3. Activate the virtual environment: `venvName\Scripts\Activate`

4. Install dependencies: `pip3 install -r requirements.txt`

5. Configure flask variables `set FLASK_APP=nameOfAppFile.py` (optional: `set FLASK_ENV=development` for hot reloads)

6. Run Flask server: `flask run`

7. Go to `localhost:5000` in the browser

## Deployment
The docker-composer.prod.yml orchestrates a mariadb container, and the web app container. To get the containers up and running, either:
- Run the redeploy-site.sh Bash script
- Manually run `docker compose -f docker-compose.prod.yml up -d --build`

## Testing
Bash scripts are added to quickly test a running Database and to ensure that the API endpoints are accepting general requests. Run the `curl-test.sh` script when locally testing these features.

Python tests are added to perform unit and integration tests of the web application. Before re-deploying, run the `run_tests.sh` script to test the API endpoints, frontend requests, and backend form validation.
