# app.py
from flask import Flask, render_template, request, redirect, url_for, flash, session
from sqlalchemy import text
from dotenv import load_dotenv
import os
import click # Importar click para los comandos CLI
import logging
from flask_migrate import Migrate # Importar Migrate
from extensions import db # Importar 'db' desde extensions.py
from models import Usuario, Emprendedor, TipoPerfil, Empresario, Inversionista, Institucion # Importar todos los modelos

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

# Inicializar la base de datos con la app
db.init_app(app)

# Configurar Flask-Migrate
migrate = Migrate(app, db)

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

            # Renderiza la página de éxito en lugar de usar flash y redirect
            return render_template('alerta_reg_exitoso_emprendedor.html')
        except Exception as e:
            db.session.rollback() # Revertir cambios si hay un error
            app.logger.error(f"Error en registro de emprendedor: {e}")
            flash(f'Hubo un error en el registro: {e}', 'danger')

    return render_template('Registro_emprendedor.html')

@app.route('/registro_empresario', methods=['GET', 'POST'])
def registro_empresario():
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
            if Usuario.query.filter_by(email=correo).first():
                errors['correo'] = 'El correo electrónico ya está registrado. Por favor, utiliza otro.'

            # Verificar si el NIT ya está registrado en la tabla de instituciones
            if Institucion.query.filter_by(nit=nit).first():
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
                nombre_institucion=request.form['nombre_institucion'],
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
            nombre_institucion = nueva_institucion.nombre_institucion
            return render_template('alerta_reg_exitoso_institucion.html', nombre_perfil=nombre_institucion)

        except Exception as e:
            db.session.rollback()
            app.logger.error(f"Error en registro de institución: {e}")
            # Mantenemos un flash para errores inesperados que no son de validación
            flash('Hubo un error inesperado durante el registro. Por favor, inténtalo de nuevo.', 'danger')

    return render_template('Registro_institucion.html')

@app.route('/registro_inversionista', methods=['GET', 'POST'])
def registro_inversionista():
    return render_template('Registro_inversionista.html')

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        profile_type_str = request.form.get('profile')

        if not email or not password or not profile_type_str:
            flash('Por favor, completa todos los campos.', 'warning')
            return redirect(url_for('Principal'))

        try:
            # Convertir el string del formulario al tipo Enum
            profile_type = TipoPerfil(profile_type_str)
        except ValueError:
            flash('El perfil seleccionado no es válido.', 'danger')
            return redirect(url_for('Principal'))

        # Buscar al usuario por su email
        usuario = Usuario.query.filter_by(email=email).first()

        # Verificar si el usuario existe, si la contraseña es correcta Y si el perfil coincide
        if usuario and usuario.check_password(password) and usuario.tipo_perfil == profile_type:
            # Guardar información del usuario en la sesión
            session['user_id'] = usuario.id
            session['user_email'] = usuario.email
            session['user_profile'] = usuario.tipo_perfil.value
            
            flash(f'¡Bienvenido de nuevo, {usuario.get_perfil().nombre_completo}!', 'success')
            # Redirigir a un dashboard o página principal del usuario
            return redirect(url_for('Principal')) # Cambia 'Principal' por tu ruta de dashboard cuando la tengas
        else:
            flash('Correo, contraseña o perfil incorrectos. Por favor, inténtalo de nuevo.', 'danger')
            return redirect(url_for('Principal'))

# --- Comandos CLI para administración ---

@app.cli.command("create-superuser")
@click.argument("email")
@click.argument("password")
def create_superuser(email, password):
    """Crea un usuario administrador."""
    if Usuario.query.filter_by(email=email).first():
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
    usuario = Usuario.query.filter_by(email=email).first()

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
    app.run(host='0.0.0.0' ,port=84,debug= True) # Cualquier direccion puede acceder a la aplicacion 0.0.0.0
