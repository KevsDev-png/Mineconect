from flask import Flask  

# Crear la aplicación Flask
app = Flask(__name__)  

# Definir una ruta básica
@app.route('/')
def home():
    return "¡Hola, Flask está funcionando!"

# Ejecutar la app
if __name__ == '__main__':
    app.run(host='0.0.0.0' ,port=84,debug= True)

