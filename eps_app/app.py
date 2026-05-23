from flask import Flask, redirect, url_for

from config import Config
from data.database import close_connection, init_db
from presentation.controllers.affiliation_controller import affiliation_bp
from presentation.controllers.appointment_controller import appointment_bp
from presentation.controllers.auth_controller import auth_bp
from presentation.controllers.authorization_controller import authorization_bp
from presentation.controllers.plan_controller import plan_bp


def create_app():
    app = Flask(__name__, template_folder="presentation/templates")
    app.config.from_object(Config)
    app.secret_key = app.config["SECRET_KEY"]

    with app.app_context():
        init_db()

    app.teardown_appcontext(close_connection)

    app.register_blueprint(auth_bp)
    app.register_blueprint(authorization_bp, url_prefix="/autorizaciones")
    app.register_blueprint(affiliation_bp, url_prefix="/afiliaciones")
    app.register_blueprint(appointment_bp, url_prefix="/citas")
    app.register_blueprint(plan_bp, url_prefix="/planes")

    @app.route("/")
    def index():
        return redirect(url_for('auth.login'))

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)