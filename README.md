# CITS3403-web-project
Group project for Agile Web Development (CITS3403) developing an IQ test based web application.

## Competitive Programming Website

Example comp programming website https://pcs.org.au/

### Website Structure / Features
- one promoting the theme (and explaining how the quiz works) to users; 
- Question sets/problem list; 
- Individual problem / submit page / results; 
- Statistics page (rankings, global stats etc)
- Admin add / remove question sets / users

### Ideas / Things to work on if time permits
- Manual feedback. Allows admins to assess responses. 

|         | Week 1                  | Week 2                    | Week 3 | Week 4 | Week 5 | Week 6 |
|---------|-------------------------|---------------------------|--------|--------|--------|--------|
| Guohuan | Make page               | Make register and homepage|        |        |        |        |
| Jeremy  | Make html for each page | Add in CSS and javascript |        |        |        |        |
| Alan    | Learn Flask             |                           |        |        |        |        |
| Brandon | Learn Back end          |                           |        |        |        |        |

## Getting Started
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
