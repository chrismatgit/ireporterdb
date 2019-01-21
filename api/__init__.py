from api.Views.routes import bp
from flask import Flask
from flask_jwt_extended import JWTManager

app = Flask(__name__)
jwt = JWTManager(app)
app.register_blueprint(bp, url_prefix='/api/v1')
app.config['JWT_SECRET_KEY'] = 'SECretK1ey'