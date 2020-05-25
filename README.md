# CITS3403-Web-Project 2

**Warning this app uses shell scripts and requires root access**

## Getting Started

### Requirements
- GCC, the GNU Compiler Collection
- Python 3.8 or newer
- Redis Server
    - sudo apt install redis-server
    - brew install redis
    - sudo pacman -S redis


### Installing
Install Python 3.8 or newer
Install flask: `pip install flask`
Install sqlite
Install GCC
Install Redis Server
    - sudo apt install redis-server
    - brew install redis
    - sudo pacman -S redis


### Running the app

#### Shell Script

The hard work has been done in a script called 'yeetcode.sh'

	chmod +x yeetcode.sh
	sudo ./yeetcode.sh [start/stop]

*Note that root access is needed for the redis server system daemon*

#### Manually

##### Set flask variables

.flaskenv should already exist. If it doesn't

- On Windows `set FLASK_APP=app`
- On Linux/Mac `export FLASK_APP=app`
- Alteratively create a .flaskenv (pip install flask-dotenv && echo 'export FLASK_APP=yeetcode.py' > .flaskenv)

##### Start the redis server

	Linux 'sudo systemctl start redis.service'
	Mac 'brew services start redis'

##### Start the rq worker

	chmod +x worker.py
	./worker.py
	./worker.py & (to run in the backgroud)


##### Start the Flask app

	flask run


