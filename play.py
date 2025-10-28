# app.py
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from dotenv import load_dotenv
import os
import logging

# Configuración básica del logging para que los mensajes se muestren en la consola
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
 
# Cargar variables del archivo .env
load_dotenv()

# Crear la aplicación Flask
app = Flask(__name__)

# Configuración de la base de datos y secret key
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")  # Ej: postgresql://postgres:tu_contraseña@localhost:5432/mineconect
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.getenv("SECRET_KEY", "clave_por_defecto")

# Inicializar la base de datos
db = SQLAlchemy(app)

# ✅ Prueba de conexión a la base de datos al iniciar la app
with app.app_context():
    try:
        with db.engine.connect() as connection:
            connection.execute(text("SELECT 1;"))
        app.logger.info("✅ Conexión a la base de datos exitosa")
    except Exception as e:
        app.logger.error(f"❌ Error al conectar con la base de datos: {e}")

        
# Definir una ruta básica, o urls apunta a una funcion que es la de abajo 
@app.route('/') #Relaciona la app con la url (/ Raiz )
def Principal():
    return render_template('Principal.html')


@app.route("/habeasdata")
def habeasdata():
    return render_template("Habeasdata.html")  # relaciona la app con el enlace en el html


@app.route('/registro_emprendedor')
def registro_emprendedor():
    return render_template('Registro_emprendedor.html')

@app.route('/registro_empresario')
def registro_empresario():
    return render_template('Registro_empresario.html')

@app.route('/registro_institucion')
def registro_institucion():
    return render_template('Registro_institucion.html')

@app.route('/registro_inversionista')
def registro_inversionista():
    return render_template('Registro_inversionista.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0' ,port=84,debug= True) # Cualquier direccion puede acceder a la aplicacion 0.0.0.0
