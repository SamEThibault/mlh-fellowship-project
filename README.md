# Production Engineering - Portfolio Site

## Inspiration
With the help of [Luke](https://github.com/lukecheseldine) and [Mustafa](https://github.com/Mustaballer), this portfolio site was born during the first week of our MLH Fellowship's Orientation Hackathon. We wanted to build a website with an intuitive structure to prioritize UX. 

## Installation
The application is currently deployed on a CentOS server [right here!](http://samthibault.live) The Bash redeploy script is included for the user's convenience to re-base and deploy the most recent version of the application with a single command.

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

5. Configure flask variables `set FLASK_APP=nameOfAppFile.py` (optional: `set FLASK_ENV=development` for live refreshes)

6. Run Flask server: `flask run`

7. Go to `localhost:5000` in the browser


## What it does
A portfolio website with a modular design built as a template for others to add their information in JSON format or from a database table, and be able to display it through this application. Multiple scripts are added for convenience such as Database tests, API endpoints tests, frontend tests, and an automatic re-deployment script.

## How we built it
- Flask
- Jinja
- HTML
- CSS
- JavaScript
- Bootstrap V5.0
