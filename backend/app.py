from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
CORS(app)
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')

jwt = JWTManager(app)

from routes.auth import auth_bp
from routes.depenses import depenses_bp

app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(depenses_bp, url_prefix='/api/depenses')

@app.route('/')
def index():
    return 'API ExpenseTracker by Yasmine fonctionne !'

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port)