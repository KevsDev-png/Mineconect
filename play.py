# app.py
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from sqlalchemy import text
from dotenv import load_dotenv
import os
import click # Importar click para los comandos CLI
import logging
from flask_mail import Mail, Message # Importar Flask-Mail
import random # Para generar el código
from datetime import datetime, timedelta, timezone
from flask_migrate import Migrate # Importar Migrate
from extensions import db # Importar 'db' desde extensions.py
from models import Usuario, Emprendedor, TipoPerfil, Empresario, Inversionista, Institucion # Importar todos los modelos


# Configuración básica del logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
 
# Cargar variables del archivo .env
load_dotenv()

# Crear la aplicación Flask
app = Flask(__name__)


# Configuración de la base de datos y secret key
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")  # Ej: postgresql://postgres:tu_contraseña@localhost:5432/mineconect
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", "clave_por_defecto_muy_segura")

# --- Configuración de Flask-Mail ---
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'true').lower() in ['true', '1', 't']
app.config['MAIL_USE_SSL'] = os.getenv('MAIL_USE_SSL', 'false').lower() in ['true', '1', 't']
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = ('Mineconect', os.getenv('MAIL_USERNAME'))

# Inicializar la base de datos con la app
db.init_app(app)
# Inicializar Flask-Mail
mail = Mail(app)
# Configurar Flask-Migrate
migrate = Migrate(app, db)

# ✅ Prueba de conexión a la base de datos
with app.app_context():
    try:
        with db.engine.connect() as connection:
            connection.execute(text("SELECT 1;"))
        app.logger.info("✅ Conexión a la base de datos exitosa")

    except Exception as e:
        app.logger.error(f"❌ Error al conectar con la base de datos: {e}")

@app.route('/') 
def Principal():
    return render_template('Principal.html')

@app.route("/habeasdata")
def habeasdata():
    return render_template("Habeasdata.html")

@app.route('/registro_emprendedor', methods=['GET', 'POST'])
def registro_emprendedor():
    if request.method == 'POST':
        try:
            # 1. Crear el usuario base
            nuevo_usuario = Usuario(
                email=request.form['correo'],
                tipo_perfil=TipoPerfil.EMPRENDEDOR
            )
            nuevo_usuario.set_password(request.form['contrasena'])

            # 2. Crear el perfil específico del emprendedor
            nuevo_emprendedor = Emprendedor(
                nombre_completo=request.form['nombre_completo'],
                tipo_documento=request.form['tipo_documento'],
                numero_documento=request.form['numero_documento'],
                numero_celular=request.form['numero_celular'],
                programa_formacion=request.form['programa_formacion'],
                titulo_proyecto=request.form['titulo_proyecto'],
                descripcion_proyecto=request.form['descripcion_proyecto'],
                relacion_sector=request.form['relacion_sector'],
                tipo_apoyo=request.form['tipo_apoyo']
            )

            # 3. Asociar el perfil al usuario y guardar en la base de datos
            nuevo_usuario.emprendedor = nuevo_emprendedor
            db.session.add(nuevo_usuario)
            db.session.commit()

            # ¡CAMBIO! Usamos la plantilla unificada.
            return render_template(
                'registro_exitoso.html',
                tipo_cuenta='Emprendedor',
                nombre_perfil=nuevo_emprendedor.nombre_completo
            )
        except Exception as e:
            db.session.rollback() # Revertir cambios si hay un error
            app.logger.error(f"Error en registro de emprendedor: {e}")
            flash(f'Hubo un error en el registro: {e}', 'danger')

    return render_template('Registro_emprendedor.html')
  
# --- RUTA DE EMPRESARIO 
@app.route('/registro_empresario', methods=['GET', 'POST'])
def registro_empresario():
    if request.method == 'POST':
        try:
            correo = request.form['correo']
            # Verificar si el correo ya existe
            if db.session.execute(db.select(Usuario).filter_by(email=correo)).first():
                flash('El correo electrónico ya está registrado. Por favor, usa otro.', 'error')
                return redirect(url_for('registro_empresario'))

            # 1. Crear el usuario base
            nuevo_usuario = Usuario(
                email=correo,
                tipo_perfil=TipoPerfil.EMPRESARIO
            )
            nuevo_usuario.set_password(request.form['contrasena'])
            
            # Determinar el tipo de contribuyente para guardar el documento correcto
            tipo_contribuyente = request.form.get('tipo_contribuyente')
            num_doc_contribuyente = request.form.get('numero_documento_contribuyente') if tipo_contribuyente == 'natural' else None
            nit_contribuyente = request.form.get('nit') if tipo_contribuyente == 'juridica' else None

            # 2. Crear el perfil específico del empresario
            nuevo_empresario = Empresario(
                nombre_completo=request.form['nombre_completo'],
                tipo_documento_personal=request.form['tipo_documento_personal'],
                numero_documento_personal=request.form['numero_documento_personal'],
                numero_celular=request.form['numero_celular'],
                nombre_empresa=request.form['nombre_empresa'],
                tipo_contribuyente=tipo_contribuyente,
                numero_documento_contribuyente=num_doc_contribuyente,
                nit=nit_contribuyente,
                tamano=request.form['tamano'],
                etapa=request.form['etapa'],
                sector_produccion=request.form['sector_produccion'],
                sector_transformacion=request.form['sector_transformacion'],
                sector_comercializacion=request.form['sector_comercializacion']
            )
            
            # 3. Asociar el perfil al usuario y guardar
            nuevo_usuario.empresario = nuevo_empresario
            db.session.add(nuevo_usuario)
            db.session.commit()
            
            app.logger.info(f"✅ Usuario y perfil de Empresario creados para {correo}")
           
            return render_template(
                'registro_exitoso.html',
                tipo_cuenta='Empresario',
                nombre_perfil=nuevo_empresario.nombre_empresa
            )

        except Exception as e:
            db.session.rollback()
            app.logger.error(f"❌ Error al registrar empresario: {e}")
            flash(f'Error inesperado en el registro. Por favor, intenta de nuevo.', 'error')
            return redirect(url_for('registro_empresario'))

    return render_template('Registro_empresario.html')

@app.route('/registro_institucion', methods=['GET', 'POST'])
def registro_institucion():
    if request.method == 'POST':
        try:
            # --- PASO 0: VALIDACIÓN PREVIA ---
            correo = request.form['correo']
            nit = request.form['nit']
            errors = {} # Creamos un diccionario para guardar los errores

            # Verificar si el correo ya está registrado en la tabla de usuarios
            if db.session.execute(db.select(Usuario).filter_by(email=correo)).first():
                errors['correo'] = 'El correo electrónico ya está registrado. Por favor, utiliza otro.'

            # Verificar si el NIT ya está registrado en la tabla de instituciones
            if db.session.execute(db.select(Institucion).filter_by(nit=nit)).first():
                errors['nit'] = 'El NIT ya está registrado. Por favor, verifica la información.'

            if errors:
                # Si el diccionario de errores tiene algo, volvemos a mostrar el formulario con los errores
                return render_template('Registro_institucion.html', form_data=request.form, errors=errors)

            # 1. Crear el usuario base
            nuevo_usuario = Usuario(
                email=request.form['correo'],
                tipo_perfil=TipoPerfil.INSTITUCION
            )
            nuevo_usuario.set_password(request.form['contrasena'])

            # 2. Recoger los valores de los checkboxes de participación
            # request.form.getlist() obtiene todos los valores de un campo con el mismo nombre
            participacion = request.form.getlist('participacion_activa')
            # Convertimos la lista en un string separado por comas para guardarlo en la BD
            participacion_str = ','.join(participacion)

            # 3. Crear el perfil específico de la institución
            nueva_institucion = Institucion(
                nombre_completo=request.form['nombre_institucion'],
                nit=request.form['nit'],
                tipo_institucion=request.form['tipo_institucion'],
                municipio=request.form['municipio'],
                descripcion=request.form['descripcion'],
                area_especializacion=request.form['area_especializacion'],
                participacion_activa=participacion_str
            )

            # 4. Asociar el perfil al usuario y guardar en la base de datos
            nuevo_usuario.institucion = nueva_institucion
            db.session.add(nuevo_usuario)
            db.session.commit()

            # Pasamos el nombre de la institución a la plantilla de éxito
        
            return render_template(
                'registro_exitoso.html',
                tipo_cuenta='Institución',
                nombre_perfil=nueva_institucion.nombre_completo
            )

        except Exception as e:
            db.session.rollback()
            app.logger.error(f"Error en registro de institución: {e}")
            # Mantenemos un flash para errores inesperados que no son de validación
            flash('Hubo un error inesperado durante el registro. Por favor, inténtalo de nuevo.', 'danger')

    return render_template('Registro_institucion.html')

# RUTA DE INVERSIONISTA

@app.route('/registro_inversionista', methods=['GET', 'POST'])
def registro_inversionista():
    if request.method == 'POST':
        try:
            correo = request.form['correo']
            # Verificar si el correo ya existe
            if db.session.execute(db.select(Usuario).filter_by(email=correo)).first():
                flash('El correo electrónico ya está registrado. Por favor, usa otro.', 'error')
                return redirect(url_for('registro_inversionista'))
            
            # 1. Crear el usuario base
            nuevo_usuario = Usuario(
                email=correo,
                tipo_perfil=TipoPerfil.INVERSIONISTA
            )
            nuevo_usuario.set_password(request.form['contrasena'])

            # 2. Recolectar datos del Perfil Inversionista
            # Convertir listas de checkboxes a strings separados por comas
            etapas_str = ','.join(request.form.getlist('etapas'))
            areas_str = ','.join(request.form.getlist('areas'))

            nuevo_inversionista = Inversionista(
                nombre_completo=request.form['nombreCompleto'],
                tipo_documento=request.form['tipoDocumento'],
                numero_documento=request.form['numeroDocumento'],
                numero_celular=request.form['numeroCelular'],
                nombre_fondo=request.form['nombreFondo'],
                tipo_inversion=request.form['tipoInversion'],
                etapas_interes=etapas_str,
                areas_interes=areas_str
            )

            # 3. Asociar el perfil al usuario y guardar
            nuevo_usuario.inversionista = nuevo_inversionista
            db.session.add(nuevo_usuario)
            db.session.commit()

            app.logger.info(f"✅ Usuario y Perfil Inversionista creados exitosamente para {correo}")
            # ¡CAMBIO! Usamos la plantilla unificada.
            return render_template(
                'registro_exitoso.html',
                tipo_cuenta='Inversionista',
                nombre_perfil=nuevo_inversionista.nombre_completo
            )

        except Exception as e:
            db.session.rollback()
            app.logger.error(f"❌ Error al registrar inversionista: {e}")
            flash(f'Error inesperado en el registro. Por favor, intenta de nuevo.', 'error')
            return redirect(url_for('registro_inversionista'))

    return render_template('Registro_inversionista.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            data = request.get_json()
            email = data.get('email')
            password = data.get('password')
            profile_type_str = data.get('profile')

            if not email or not password or not profile_type_str:
                return jsonify({'success': False, 'message': 'Por favor, completa todos los campos.'}), 400

            # Convertir el string del formulario al tipo Enum
            profile_type = TipoPerfil(profile_type_str)
        except ValueError:
            return jsonify({'success': False, 'message': 'El perfil seleccionado no es válido.'}), 400
        except Exception:
            return jsonify({'success': False, 'message': 'Formato de solicitud incorrecto.'}), 400

        usuario = db.session.execute(db.select(Usuario).filter_by(email=email, tipo_perfil=profile_type)).scalar_one_or_none()

        if usuario and usuario.check_password(password):
            # --- Lógica de envío de código ---
            verification_code = f"{random.randint(100000, 999999)}"
            expiration_time = datetime.now(timezone.utc) + timedelta(minutes=10) # Código válido por 10 minutos

            # Guardar en la sesión
            session['verification_code'] = verification_code
            session['code_expiration'] = expiration_time.isoformat()
            session['user_to_verify'] = usuario.id

            try:
                # Enviar correo
                msg = Message(
                    subject="Tu código de verificación de Mineconect",
                    recipients=[usuario.email]
                )
                msg.html = render_template('Email/verificacion-codigo.html', code=verification_code)
                mail.send(msg)
                app.logger.info(f"✅ Código de verificación enviado a {usuario.email}")

                # Ofuscar correo para mostrar en el frontend
                user_part, domain_part = usuario.email.split('@')
                masked_user = user_part[:2] + '****' + user_part[-2:]
                masked_email = f"{masked_user}@{domain_part}"

                return jsonify({'success': True, 'message': 'Código enviado.', 'email': masked_email})

            except Exception as e:
                app.logger.error(f"❌ Error al enviar correo de verificación: {e}")
                return jsonify({'success': False, 'message': 'No se pudo enviar el código. Intenta más tarde.'}), 500
        else:
            return jsonify({'success': False, 'message': 'Correo, contraseña o perfil incorrectos.'}), 401

    # Si es una petición GET, simplemente redirige a la principal
    return redirect(url_for('Principal'))

@app.route('/verify_code', methods=['POST'])
def verify_code():
    data = request.get_json()
    user_code = data.get('code')

    stored_code = session.get('verification_code')
    expiration_str = session.get('code_expiration')
    user_id = session.get('user_to_verify')

    if not all([user_code, stored_code, expiration_str, user_id]):
        return jsonify({'success': False, 'message': 'Sesión inválida o expirada. Por favor, inicia sesión de nuevo.'}), 400

    expiration_time = datetime.fromisoformat(expiration_str)

    if datetime.now(timezone.utc) > expiration_time:
        return jsonify({'success': False, 'message': 'El código ha expirado. Por favor, solicita uno nuevo.'}), 400

    if user_code == stored_code:
        usuario = db.session.get(Usuario, user_id)
        # Limpiar sesión de verificación
        session.pop('verification_code', None)
        session.pop('code_expiration', None)
        session.pop('user_to_verify', None)

        # Iniciar sesión de verdad
        session['user_id'] = usuario.id
        session['user_email'] = usuario.email
        session['user_profile'] = usuario.tipo_perfil.value
        
        return jsonify({'success': True, 'message': f'¡Bienvenido de nuevo, {usuario.get_perfil().nombre_completo}!'})
    else:
        return jsonify({'success': False, 'message': 'El código de verificación es incorrecto.'}), 400

# --- Comandos CLI para administración ---

@app.cli.command("create-superuser")
@click.argument("email")
@click.argument("password")
def create_superuser(email, password):
    """Crea un usuario administrador."""
    if db.session.execute(db.select(Usuario).filter_by(email=email)).first():
        print(f"El usuario con el correo '{email}' ya existe.")
        return

    try:
        # Crear el usuario base
        admin_user = Usuario(
            email=email,
            tipo_perfil=TipoPerfil.ADMIN,
            is_admin=True,
            activo=True
        )
        admin_user.set_password(password)

        # Los administradores no necesitan un perfil detallado, pero si lo necesitaran,
        # se crearía y asociaría aquí.

        db.session.add(admin_user)
        db.session.commit()
        print(f"✅ Superusuario '{email}' creado exitosamente.")

    except Exception as e:
        db.session.rollback()
        print(f"❌ Error al crear el superusuario: {e}")

@app.cli.command("delete-user")
@click.argument("email")
def delete_user(email):
    """Elimina un usuario de la base de datos por su email."""
    # Buscar al usuario por su email
    usuario = db.session.execute(db.select(Usuario).filter_by(email=email)).scalar_one_or_none()

    if not usuario:
        print(f"No se encontró ningún usuario con el correo '{email}'.")
        return

    try:
        # La configuración 'cascade' en el modelo Usuario se encargará
        # de borrar automáticamente el perfil asociado si existe.
        db.session.delete(usuario)
        db.session.commit()
        print(f"✅ Usuario '{email}' y su perfil asociado han sido eliminados exitosamente.")

    except Exception as e:
        db.session.rollback()
        print(f"❌ Error al eliminar el usuario: {e}")


if __name__ == '__main__':
    app.run(host='0.0.0.0' ,port=84,debug= True)