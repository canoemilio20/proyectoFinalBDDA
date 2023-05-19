from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
from werkzeug.security import check_password_hash

from config import config

app = Flask(__name__)
mysql = MySQL(app)
login_manager_app = LoginManager(app)

class Usuario(UserMixin):
    def __init__(self, idUsuario, correo, contrasena, idTipo,):
        self.idUsuario = idUsuario
        self.correo = correo 
        self.contrasena = contrasena
        self.idTipo = idTipo
        
    @classmethod
    def check_password(self, hashed_password, contrasena):
        return check_password_hash(hashed_password, contrasena)
    
class Administrador(Usuario):
    def __init__(self, idUsuario, correo, contrasena, idTipo):
        super().__init__(idUsuario, correo, contrasena, idTipo)
    
class Compania(Usuario):
    def __init__(self, idUsuario, correo, contrasena, idTipo):
        super().__init__(idUsuario, correo, contrasena, idTipo)

class Empleado(Usuario):
    def __init__(self, idUsuario, correo, contrasena, idTipo):
        super().__init__(idUsuario, correo, contrasena, idTipo)


################## LOGIN ##########################################

@login_manager_app.user_loader
def load_user(idUsuario):
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT idUsuario, correo, contrasena, idTipo FROM Usuarios WHERE idUsuario = %s', (idUsuario))
    row = cursor.fetchone()
    if row is not None:
        idUsuario, correo, contrasena, idTipo = row
        if idTipo == 1:
            return Administrador(idUsuario, correo, contrasena, idTipo)
        elif idTipo == 2:
            return Compania(idUsuario, correo, contrasena, idTipo)
        elif idTipo == 3:
            return Empleado(idUsuario, correo, contrasena, idTipo)
    return None


@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        correo = request.form['correo']
        contrasena = request.form['contrasena']
        cursor = mysql.connection.cursor()
        cursor.execute('''SELECT idUsuario, correo, contrasena, idTipo FROM Usuarios WHERE correo AND contrasena = %s, %s''', (correo, contrasena))
        row = cursor.fetchone()
        if row is not None:
            idUsuario, correo, db_contrasena, idTipo = row
            if contrasena == db_contrasena:
                if idTipo == 1:
                    user = Administrador(idUsuario, correo, db_contrasena, idTipo)
                elif idTipo == 2:
                    user = Compania(idUsuario, correo, db_contrasena, idTipo)
                elif idTipo == 3:
                    user = Empleado(idUsuario, correo, db_contrasena, idTipo)
                login_user(user)
                return redirect(url_for('protected'))
            else:
                flash('Contraseña incorrecta')
        else:
            flash('Usuario no encontrado')
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/protected')
@login_required
def protected():
    return '<h1>Vista protegida</h1>'


def status_401(error):
    return redirect(url_for('login'))


def status_404(error):
    return "<h1>Página no encontrada</h1>"

################# REGISTRO ################################
@app.route('/register', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellidoP = request.form['apellidoP']
        apellidoM = request.form['apellidoM']
        correo = request.form['correo']
        telefono = request.form['telefono']
        contrasena = request.form['contrasena']
        
        # Insertar los datos en la base de datos
        cursor = mysql.connection.cursor()
        cursor.execute('''INSERT INTO Usuarios (nombre, apellidoP, apellidoM, correo, telefono, contrasena) VALUES (%s, %s, %s, %s, %s, %s)''', (nombre, apellidoP, apellidoM, correo, telefono, contrasena))
        mysql.connection.commit()
        cursor.close()
        
        flash('Registro exitoso. Por favor inicia sesión.')
        return render_template('login')
    
    return render_template('registro.html')

################## ADMIN ############################
@app.route('/admin', methods=['GET','POST'])
@login_required
def admin():
    if isinstance(load_user, Administrador):
        if request.method == 'GET':
            return flash('No tienes acceso a este dashboard')
        if request.method == 'POST':
            return render_template('admin.html')

@app.route('/admin/usuarios', methods=['GET'])
@login_required
def usuarios():
    if isinstance(login_user, Administrador):
        cursor = mysql.connection.cursor()
        cursor.execute('''SELECT idUsuario, nombre, apellidoP, apellidoM, correo, telefono, idTipo FROM Usuarios''')
        correo = cursor.fetchall()
        cursor.close()
        return render_template('usuarios.html', correo = correo)
    else:
        return "Acceso denegado"

@app.route('admin/usuarios/modificar/<int:idUsuario>', methods=['GET', 'POST'])
@login_required
def modificar_usuario(idUsuario):
    if isinstance(login_user, Administrador):
        if request.method == 'GET':
            cursor = mysql.connection.cursor()
            cursor.execute('SELECT idUsuario, correo, idTipo FROM Usuarios WHERE idUsuario = %s', (idUsuario,))
            correo = cursor.fetchone()
            cursor.close()
            if usuario:
                return render_template('modificarUsuario.html', correo=correo)
            else:
                return "Usuario no encontrado"
        
        if request.method == 'POST':
            usuario = request.form['usuario']
            idTipo = request.form['idTipo']
            
            cursor = mysql.connection.cursor()
            cursor.execute('UPDATE Usuarios SET usuario = %s, idTipo = %s WHERE idUsuario = %s', (usuario, idTipo, idUsuario))
            mysql.connection.commit()
            cursor.close()
            
            flash('Usuario modificado correctamente.')
            return redirect(url_for('usuarios'))
    else:
        return "Acceso denegado"


@app.route('admin/usuarios/eliminar/<int:idUsuario>', methods=['GET'])
@login_required
def eliminar_usuario(idUsuario):
    if isinstance(login_user, Administrador):
        cursor = mysql.connection.cursor()
        cursor.execute('DELETE FROM Usuarios WHERE idUsuario = %s', (idUsuario,))
        mysql.connection.commit()
        cursor.close()
        
        flash('Usuario eliminado correctamente.')
        return redirect(url_for('usuarios'))
    else:
        return "Acceso denegado"     


################## EMPLEADOS ##########################################
# Pagina principal de empleado
@app.route('/inventario', methods=['GET','POST'])
@login_required
def inicio():
    if isinstance(load_user, Empleado):
        cursor = mysql.connection.cursor()
        cursor.execute('''SELECT * FROM producto''')
        productos = cursor.fetchall()
        return render_template('inventario.html', productos=productos)

# Metodo para agregar productos
@app.route('/agregarProducto', methods=['GET','POST'])
@login_required
def insertar():
    if isinstance(load_user, Empleado):
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
@login_required
def modificar():
    if isinstance(load_user, Empleado):
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
@login_required
def eliminar():
    if isinstance(load_user, Empleado):
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
@login_required
def ruta():
    if isinstance(load_user, Compania):
        if request.method == 'GET':
            cursor = mysql.connection.cursor()
            cursor.execute('''SELECT * FROM producto''')
            return render_template('ruta.html')
        if request.method == 'POST':
            return
    
    
if __name__ == "__main__":
    app.config.from_object(config['development'])
    app.register_error_handler(401, status_401)
    app.register_error_handler(404, status_404)
    app.run(debug=True)
