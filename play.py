from flask import Flask 

# Crear la aplicación Flask
app = Flask(__name__)  #variable app, va a recibir el parametro name que es elnombre del archivo que estamos parados 

# Definir una ruta básica, o urls apunta a una funcion que es la de abajo 
@app.route('/') #Relaciona la app con la url (/ Raiz )
def Principal():
    return "¡Hola, Flask está funcionando!"

# Ejecutar la app
if __name__ == '__main__':
    app.run(host='0.0.0.0' ,port=84,debug= True) # Cualquier direccion puede acceder a la aplicacion 0.0.0.0


