# CITS3403-Web-Project 2

## Getting Started

### Requirements
- GCC, the GNU Compiler Collection
- Python 3.8 or newer
- Redis Server 
    - sudo apt install redis-server
    - brew install redis 


### Installing
Install flask: `pip install flask`

Install sqlite

### Files needed
Copy 'app' folder into your CITS3403-web-project folder.

Copy 'tests' folder into your CITS3403-web-project folder (currently empty).

### Running the app
Navigate to CITS3403-web-project folder containing app folder.

Set flask variables:
- On Windows `set FLASK_APP=app` and `set FLASK_ENV=development`
- On Linux/Mac `export FLASK_APP=app` and `export FLASK_ENV=development`

Initialise database: `flask init-db`

Run the application (ensure you are in /CITS3403-web-project not /CITS3403-web-project/app): `flask run`

Navigate to login page: http://localhost:5000/auth/login
