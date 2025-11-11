# app.py
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from dotenv import load_dotenv
import os
import logging

# --- Imports que necesitamos ---
from flask_bcrypt import Bcrypt
from flask_cors import CORS

# Configuración básica del logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
 
# Cargar variables del archivo .env
load_dotenv()

# Crear la aplicación Flask
app = Flask(__name__)

# --- Configuración ---
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.getenv("SECRET_KEY", "una_llave_secreta_muy_fuerte")

# --- Inicializar extensiones ---
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# ✅ Prueba de conexión a la base de datos
with app.app_context():
    try:
        with db.engine.connect() as connection:
            connection.execute(text("SELECT 1;"))
        app.logger.info("✅ Conexión a la base de datos exitosa")
    except Exception as e:
        app.logger.error(f"❌ Error al conectar con la base de datos: {e}")


# --- MODELOS DE LA BASE DE DATOS ---

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    nombre_completo = db.Column(db.String(100), nullable=False)
    correo = db.Column(db.String(120), unique=True, nullable=False)
    tipo_documento_personal = db.Column(db.String(10), nullable=False) 
    numero_documento_personal = db.Column(db.String(30), unique=True, nullable=False)
    numero_celular = db.Column(db.String(15), nullable=False)
    terminos_aceptados = db.Column(db.Boolean, nullable=False, default=False)
    password_hash = db.Column(db.String(255), nullable=False)
    rol = db.Column(db.String(20), nullable=False) # 'empresario', 'inversionista', etc.
    
    # --- Relaciones ---
    perfil_empresario = db.relationship('PerfilEmpresario', back_populates='user', uselist=False, cascade="all, delete-orphan")
    perfil_inversionista = db.relationship('PerfilInversionista', back_populates='user', uselist=False, cascade="all, delete-orphan")

    def __repr__(self):
        return f'<User {self.correo}>'

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)


class PerfilEmpresario(db.Model):
    __tablename__ = 'perfil_empresario'
    id = db.Column(db.Integer, primary_key=True)
    nombre_empresa = db.Column(db.String(100), nullable=False)
    tipo_contribuyente = db.Column(db.String(20), nullable=False)
    numero_documento_contribuyente = db.Column(db.String(30), nullable=True)
    nit = db.Column(db.String(30), nullable=True)
    tamano = db.Column(db.String(20), nullable=False)
    etapa = db.Column(db.String(30), nullable=False)
    sector_produccion = db.Column(db.String(100), nullable=True)
    sector_transformacion = db.Column(db.String(100), nullable=True)
    sector_comercializacion = db.Column(db.String(100), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False)
    user = db.relationship('User', back_populates='perfil_empresario')

    def __repr__(self):
        return f'<PerfilEmpresario {self.nombre_empresa}>'

# --- ¡ESTA ES LA CLASE QUE FALTABA EN TU ARCHIVO GUARDADO! ---
class PerfilInversionista(db.Model):
    __tablename__ = 'perfil_inversionista'
    id = db.Column(db.Integer, primary_key=True)
    
    # --- Datos del Perfil ---
    nombre_fondo = db.Column(db.String(100), nullable=True)
    tipo_inversion = db.Column(db.String(50), nullable=True) # 'capital', 'angel', 'credito'
    # Guardamos los checkboxes como listas JSON
    etapas_interes = db.Column(db.JSON, nullable=True) 
    areas_interes = db.Column(db.JSON, nullable=True)
    
    # --- Enlace con el Usuario ---
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False)
    user = db.relationship('User', back_populates='perfil_inversionista')

    def __repr__(self):
        return f'<PerfilInversionista {self.nombre_fondo}>'

        
# --- RUTAS DE LA APLICACIÓN ---
@app.route('/') 
def Principal():
    return render_template('Principal.html')

@app.route("/habeasdata")
def habeasdata():
    return render_template("Habeasdata.html")

@app.route('/registro_emprendedor')
def registro_emprendedor():
    return render_template('Registro_emprendedor.html')

# --- RUTA DE EMPRESARIO (Modificada para redirigir) ---
@app.route('/registro_empresario', methods=['GET', 'POST'])
def registro_empresario():
    if request.method == 'POST':
        try:
            correo = request.form.get('correo')
            user_exists = User.query.filter_by(correo=correo).first()
            if user_exists:
                flash('El correo electrónico ya está registrado. Por favor, usa otro.', 'error')
                return redirect(url_for('registro_empresario'))

            nuevo_usuario = User(
                nombre_completo=request.form.get('nombre_completo'),
                correo=correo,
                tipo_documento_personal=request.form.get('tipo_documento_personal'),
                numero_documento_personal=request.form.get('numero_documento_personal'),
                numero_celular=request.form.get('numero_celular'),
                terminos_aceptados=request.form.get('terminos') == 'on',
                rol='empresario'
            )
            nuevo_usuario.set_password(request.form.get('contrasena'))
            
            tipo_contribuyente = request.form.get('tipo_contribuyente')
            nuevo_perfil = PerfilEmpresario(
                nombre_empresa=request.form.get('nombre_empresa'),
                tipo_contribuyente=tipo_contribuyente,
                numero_documento_contribuyente=request.form.get('numero_documento') if tipo_contribuyente == 'natural' else None,
                nit=request.form.get('nit') if tipo_contribuyente == 'juridica' else None,
                tamano=request.form.get('tamano'),
                etapa=request.form.get('etapa'),
                sector_produccion=request.form.get('sector_produccion'),
                sector_transformacion=request.form.get('sector_transformacion'),
                sector_comercializacion=request.form.get('sector_comercializacion'),
                user=nuevo_usuario
            )
            
            db.session.add(nuevo_usuario)
            db.session.add(nuevo_perfil)
            db.session.commit()
            
            app.logger.info(f"✅ Usuario y Perfil Empresario creados exitosamente para {correo}")
            # --- ¡ÉXITO! Redirigir a la página dinámica ---
            return redirect(url_for('registro_exitoso', tipo_cuenta='empresario'))

        except Exception as e:
            db.session.rollback()
            app.logger.error(f"❌ Error al registrar empresario: {e}")
            flash(f'Error inesperado en el registro. Por favor, intenta de nuevo.', 'error')
            return redirect(url_for('registro_empresario'))

    return render_template('Registro_empresario.html')


@app.route('/registro_institucion')
def registro_institucion():
    return render_template('Registro_institucion.html')

# --- ¡NUEVA LÓGICA PARA INVERSIONISTA! ---
@app.route('/registro_inversionista', methods=['GET', 'POST'])
def registro_inversionista():
    if request.method == 'POST':
        try:
            # --- 1. Recolectar datos del Usuario ---
            # OJO: Los 'name' del HTML de inversionista son diferentes
            correo = request.form.get('correo')
            
            user_exists = User.query.filter_by(correo=correo).first()
            if user_exists:
                flash('El correo electrónico ya está registrado. Por favor, usa otro.', 'error')
                return redirect(url_for('registro_inversionista'))
            
            nuevo_usuario = User(
                nombre_completo=request.form.get('nombreCompleto'), # name="nombreCompleto"
                correo=correo,
                tipo_documento_personal=request.form.get('tipoDocumento'), # name="tipoDocumento"
                numero_documento_personal=request.form.get('numeroDocumento'), # name="numeroDocumento"
                numero_celular=request.form.get('numeroCelular'), # name="numeroCelular"
                terminos_aceptados=request.form.get('terminos') == 'on',
                rol='inversionista' # ¡Rol diferente!
            )
            nuevo_usuario.set_password(request.form.get('contrasena'))

            # --- 2. Recolectar datos del Perfil Inversionista ---
            nuevo_perfil = PerfilInversionista(
                nombre_fondo=request.form.get('nombreFondo'),
                tipo_inversion=request.form.get('tipoInversion'),
                # .getlist() captura TODOS los checkboxes marcados con el mismo name
                etapas_interes=request.form.getlist('etapas'),
                areas_interes=request.form.getlist('areas'),
                user=nuevo_usuario # Enlazar al usuario
            )

            # --- 3. Guardar en la Base de Datos ---
            db.session.add(nuevo_usuario)
            db.session.add(nuevo_perfil)
            db.session.commit()

            app.logger.info(f"✅ Usuario y Perfil Inversionista creados exitosamente para {correo}")
            # --- ¡ÉXITO! Redirigir a la página dinámica ---
            return redirect(url_for('registro_exitoso', tipo_cuenta='inversionista'))

        except Exception as e:
            db.session.rollback()
            app.logger.error(f"❌ Error al registrar inversionista: {e}")
            flash(f'Error inesperado en el registro. Por favor, intenta de nuevo.', 'error')
            return redirect(url_for('registro_inversionista'))

    # Si el método es GET, solo muestra la plantilla
    return render_template('Registro_inversionista.html')

# --- ¡RUTA DE ÉXITO ACTUALIZADA! ---
@app.route('/registro_exitoso')
def registro_exitoso():
    # Capturamos el tipo_cuenta que viene en la URL
    tipo_cuenta = request.args.get('tipo_cuenta', 'usuario') 
    # Se lo pasamos al HTML
    return render_template('registro_exitoso.html', tipo_cuenta=tipo_cuenta)

# --- PUNTO DE ENTRADA ---
if __name__ == '__main__':
    app.run(host='127.0.0.1' ,port=84,debug= True)