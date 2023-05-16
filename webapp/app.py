from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import LoginManager, login_user, logout_user, login_required

from config import config

# Modelos
from models.ModelUser import ModelUser

# Entidades
from models.entities.User import User #Compañía
#from models.entities.Empleado import Empleado
#from models.entites.Admin import Admin

app = Flask(__name__)
mysql = MySQL(app)
admin = Admin(app, name='Control Panel')
login_manager_app=LoginManager(app)

################## LOGIN ##########################################

@login_manager_app.user_loader
def load_user(idUsuario):
    return ModelUser.get_by_id(mysql, idUsuario)

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = User(0, request.form['usuario'], request.form['password'])
        logged_user = ModelUser.login(mysql,usuario)
        if logged_user!=None:
            if logged_user.password:
                login_user(logged_user)
                return redirect(url_for('inicio'))
            else:
                flash("Contraseña invalida ...")
                return render_template('login.html')
        else:
            flash("Usuario no encontrado ...")
            return render_template('login.html')
    else:
        return render_template('login.html')

@app.route('/logout')
def logout():
    logout_user() 
    return redirect(url_for('login'))

@app.route('/protected')
@login_required 
def protected():
    return "<h1>Vista protegida</h1>"

def status_401(error):
    return redirect(url_for('login'))

def status_404(error):
    return "<h1>Página no encontrada</h1>"

################## EMPLEADOS ##########################################
# Pagina principal de empleado
@app.route('/inventario', methods=['GET','POST'])
def inicio():
    cursor = mysql.connection.cursor()
    cursor.execute('''SELECT * FROM producto''')
    productos = cursor.fetchall()
    return render_template('inventario.html', productos=productos)

# Metodo para agregar productos
@app.route('/agregarProducto', methods=['GET','POST'])
def insertar():
    if request.method == 'GET':
        return render_template('agregarProductos.html')
    if request.method == 'POST':
        nombre = request.form['nombre']
        cantidad = request.form['cantidad']
        cursor = mysql.connection.cursor()
        cursor.execute('''INSERT INTO producto(nombre, cantidad) VALUES(%s, %s)''', (nombre, cantidad))
        cursor.connection.commit()
        cursor.close()
        return inicio()
    
# Metodo para modificar productos. Funciona pero no muestra los valores actuales antes de que se modifiquen
@app.route('/modificarProducto', methods=['GET','POST'])
def modificar():
    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        cursor.execute('''SELECT * FROM producto''')
        productos = cursor.fetchall()
        return render_template('modificarProductos.html', productos=productos)
    if request.method == 'POST':
        idProducto = request.form['producto']
        nombre = request.form['nombre']
        cantidad = request.form['cantidad']
        cursor = mysql.connection.cursor()
        cursor.execute('''UPDATE producto SET nombre=%s, cantidad=%s WHERE idProducto=%s''', (nombre, cantidad, idProducto))
        cursor.connection.commit()
        cursor.close()
        return inicio()

# Metodo para eliminar productos
@app.route('/eliminarProducto', methods=['GET','POST'])
def eliminar():
    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        cursor.execute('''SELECT * FROM producto''')
        productos = cursor.fetchall()
        return render_template('eliminarProductos.html', productos=productos)
    if request.method == 'POST':
        idProducto = request.form['producto']
        cursor = mysql.connection.cursor()
        cursor.execute('''DELETE FROM producto WHERE idProducto=%s''', (idProducto,))
        cursor.connection.commit()
        cursor.close()
        return inicio()
    
# Metodo para consultar ruta y rastreo de paquete
@app.route('/ruta', methods=['GET','POST'])
def ruta():
    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        cursor.execute('''SELECT * FROM producto''')
        return render_template('ruta.html')
    if request.method == 'POST':
        return

#########################################################################
    
if __name__ == "__main__":
    app.config.from_object(config['development'])
    app.register_error_handler(401, status_401)
    app.register_error_handler(404, status_404)
    app.run(debug=True)