# CITS3403-Web-Project 2

**Warning this app uses shell scripts and requires root access**

YeetCode is inspired LeetCode - The World's Leading Online Programming
Learning Platform

Our goal was to provide a platform for practicing and sharpening your skills, when
preparing for technical interviews. 

LeetCode provides an inclusive and nurturing environment. It caters to every programmer.
Whether you are young competitive programming prodigy William Lin Or a student cramming for 
your for the upcoming CITS2200 exam. LeetCode is platform for you.

At YeetCode, our mission is to help you improve yourself and land your dream
job. We have a sizable repository of interview resources for a wide variety of users.
In the past few years, our users have landed jobs at top companies around the
world.

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
Install Python dependencies
	- pip install -r requirements.txt
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

### Testing the app

Run unit tests via the command `python -m tests.unit`

To run system tests, ensure Geckodriver for Firefox is installed in the dir tests\, then change the app to run in 
TestConfig by adjusting yeetcode.py:

	app = create_app()

to:

	app = create_app(TestConfig)

Then make sure the app is running in the background before running `python -m tests.system`
