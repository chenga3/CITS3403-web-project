# CITS3403-Web-Project 2

## Getting Started

### Requirements
- GCC, the GNU Compiler Collection
- Python 3.8 or newer
- Redis Server 
    - sudo apt install redis-server
    - brew install redis 
    - sudo pacman -S redis


### Installing
Install flask: `pip install flask`

Install sqlite

### Files needed
Copy 'app' folder into your CITS3403-web-project folder.

Copy 'tests' folder into your CITS3403-web-project folder (currently empty).

### Running the app
Navigate to CITS3403-web-project folder containing app folder.

Set flask variables:
- On Windows `set FLASK_APP=app`
- On Linux/Mac `export FLASK_APP=app`
- Alteratively create a .flaskenv (pip install flask-dotenv && echo 'export FLASK_APP=yeetcode.py')

Start the redis server 
- Linux 'sudo systemctl start redis.service'
- Mac 'brew services start redis'

Run the application (ensure you are in /CITS3403-web-project not /CITS3403-web-project/app): `flask run`
