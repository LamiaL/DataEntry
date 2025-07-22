from flask import Flask
from flask_cors import CORS
from app.dataBases import create_users_table,setup_db_lst

def create_app():
    app = Flask(__name__)
    app.secret_key = "\x83\xe8G\x1f\xfd\xba\xfa\x9c\x10\xe4|\x01l?\xee\xa4\xf5\xf8b_\x13&\xe9"
    create_users_table()
    setup_db_lst()

    # Import Blueprints
    from app.auth_login import auth_login_bp
    from app.dashboard import dashboard_bp
    from app.users import users
    from app.data import data_bp
    from app.dataenv import dataenv
    from app.dataenvrh import dataenvrh
    from app.dataenvfin import dataenvfin
    from app.dataenvm import dataenvm
    from app.dataenvd import dataenvd
    from app.form import form_bp
    from app.index import index_bp
    from app.indexrh import indexrh_bp
    from app.indexfin import indexfin_bp
    from app.indexenv import indexenv_bp
    from app.indexenvd import indexenvd_bp
    from app.edit_data import edit_data_bp
    from app.services.data_function import  app_bp
    from app.services.parameters import parameters_bp


    # Register Blueprints
    CORS(auth_login_bp)
    app.register_blueprint(auth_login_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(users)
    app.register_blueprint(form_bp)
    app.register_blueprint(index_bp)
    app.register_blueprint(indexenv_bp)
    app.register_blueprint(indexenvd_bp)
    app.register_blueprint(indexrh_bp)
    app.register_blueprint(indexfin_bp)
    app.register_blueprint(data_bp)
    app.register_blueprint(dataenv)
    app.register_blueprint(dataenvrh)
    app.register_blueprint(dataenvfin)
    app.register_blueprint(dataenvm)
    app.register_blueprint(dataenvd)
    app.register_blueprint(edit_data_bp)
    app.register_blueprint(app_bp)
    app.register_blueprint(parameters_bp)

    return app
