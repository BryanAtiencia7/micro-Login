from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token
import bcrypt


app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'tu_clave_secreta'

CORS(app)

jwt = JWTManager(app)

usuarios = {
    "usuario1": bcrypt.hashpw("password123".encode('utf-8'), bcrypt.gensalt())
}

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password').encode('utf-8')

    if username in usuarios and bcrypt.checkpw(password, usuarios[username]):
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"msg": "Credenciales inválidas"}), 401

if __name__ == '__main__':
    app.run(port=5000, debug=True)