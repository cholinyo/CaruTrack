from flask import Blueprint

grant_routes = Blueprint('grant_routes', __name__)

@grant_routes.route('/grants')
def get_grants():
    from controllers.grant_controller import GrantController  # Importación local para evitar dependencia circular
    controller = GrantController()
    return controller.get_grants()