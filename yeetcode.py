from app import create_app, db
from app.models import User, Problem, ProblemTestCases
from config import TestConfig

#create the app
app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Problem': Problem, 'ProblemTestCases': ProblemTestCases}
        