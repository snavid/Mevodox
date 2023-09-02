from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import secrets

db = SQLAlchemy()
database = "datastore.db"

def create_app():
    app = Flask(__name__, static_url_path='/statics', template_folder="templates", static_folder="statics")
    app.config['SECRET_KEY'] = secrets.token_hex()
    #old sqlite db
    #app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{database}'
    #new mysql db
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:teamalikiba95@localhost/mevodox'
    db.init_app(app) 
    
    from .views import views
    from .auth import auth
    
    app.register_blueprint(views)
    app.register_blueprint(auth)
     
    from .models import User
    with app.app_context():
        db.create_all()
    
    login_manager = LoginManager()
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'
    login_manager.init_app(app)    
   
    return app    

