from app.api import bp

@bp.route('/problems/<urltitle>', methods=['GET'])
def get_problem(urltitle):
    pass

@bp.route('/problems', methods=['GET'])
def get_problems():
    pass

@bp.route('/problems', methods=['POST'])
def create_problem():
    pass

@bp.route('/problem/<urltitle>', methods=['PUT'])
def update_problem(urltitle):
    pass