# Production Engineering - Week 1 - Portfolio Site

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
A portfolio website showcasing our team's profiles, hobbies, work experiences, and projects. We also have a cool map to show call the unique locations we have visited all over the globe! Our priority was for the site to be modular so that anyone could add their own information and showcase their profiles using this template. Therefore, all personal information is extracted from a JSON file where end users could fill out the required fields. 

## How we built it
- Flask
- Jinja
- Folium
- HTML
- CSS
- JavaScript
- Bootstrap V5.0

## Challenges we ran into
- Setting up flask server 
- Folium not insertable with Jinja templates

## Accomplishments that we're proud of
- Sticking completely to the theme
- Being comfortable with branches, and merge conflicts
- Following good practices for naming and reviewing PRs

## What we learned
-  Using Flask and Jinja templating when working on this project
-  How to use Folium for our map framework
- Customizing Bootstrap elements for a cohesive theme

## What's next for Team Jungle
Connect to a database, and automate the process for making updates to hobbies, experiences, and locations visited so that users can add information to the site through a graphical user interface.
