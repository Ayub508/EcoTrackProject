from flask import Flask
from config import config
from app.extensions import db, jwt, cors, ma


def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    jwt.init_app(app)
    cors.init_app(app, resources={r"/api/*": {"origins": "*"}})
    ma.init_app(app)

    from app.routes.auth import auth_bp
    from app.routes.activities import activities_bp
    from app.routes.dashboard import dashboard_bp
    from app.routes.goals import goals_bp
    from app.routes.recommendations import recommendations_bp
    from app.routes.emission_factors import emission_factors_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(activities_bp, url_prefix='/api/activities')
    app.register_blueprint(dashboard_bp, url_prefix='/api/dashboard')
    app.register_blueprint(goals_bp, url_prefix='/api/goals')
    app.register_blueprint(recommendations_bp, url_prefix='/api/recommendations')
    app.register_blueprint(emission_factors_bp, url_prefix='/api/emission-factors')

    from app.utils.errors import register_error_handlers
    register_error_handlers(app)

    return app
