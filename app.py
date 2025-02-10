from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token
from dotenv import load_dotenv
import os
import pymysql
import bcrypt

load_dotenv()

db_host = os.getenv('DB_HOST')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'tu_clave_secreta'

CORS(app)

jwt = JWTManager(app)

def obtener_conexion():
    return pymysql.connect(
        host=db_host, 
        user=db_user, 
        password=db_password, 
        database='usuario_db',
        cursorclass=pymysql.cursors.DictCursor
    )

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password').encode('utf-8')

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("SELECT password FROM usuarios WHERE username = %s", (username,))
    usuario = cursor.fetchone()

    conexion.close()

    if usuario and bcrypt.checkpw(password, usuario['password'].encode('utf-8')):
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"msg": "Credenciales inválidas"}), 401

if __name__ == '__main__':
    app.run(port=5000, debug=True)
