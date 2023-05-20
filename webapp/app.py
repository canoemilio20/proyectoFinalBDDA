from flask import Flask, render_template, request, session, redirect, url_for
from flask_mysqldb import MySQL
from mysql import connector
from werkzeug.security import check_password_hash

app = Flask(__name__)
mysql = MySQL(app)
app.secret_key='HOLA'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'usuario'
app.config['MYSQL_PASSWORD'] = '111'
app.config['MYSQL_DB'] = 'elatico'

################## SISTEMA LOGIN ##########################################
@app.route('/')
def index():
    if 'nombreUsuario' in session:
        nombreUsuario = session['nombreUsuario']
        idTipo = session.get('idTipo')
        
        if idTipo == 1:
            return render_template('admin.html', nombreUsuario=nombreUsuario)
        elif idTipo == 2:
            return render_template('inventario.html', nombreUsuario=nombreUsuario)
        elif idTipo == 3:
            return render_template('index.html', nombreUsuario=nombreUsuario)
        else:
            error = 'Tipo de usuario no válido.'
            return render_template('login.html', error=error)
    else:
        return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Obtener las credenciales ingresadas por el usuario
        nombreUsuario = request.form['nombreUsuario']
        contrasenaUsuario = request.form['contrasenaUsuario']

        # Verificar las credenciales en la base de datos
        conn = connector.connect(
            host='localhost',
            user='usuario',
            password='111',
            database='elatico'
        )
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuario WHERE nombreUsuario = %s AND contrasenaUsuario = %s", (nombreUsuario, contrasenaUsuario))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user:
            session['nombreUsuario'] = user[1]  # Utilizamos el índice 1 para acceder al nombre de usuario en la tupla
            session['idTipo'] = user[6]
            nombreUsuario = session['nombreUsuario']
            idTipo = session['idTipo']

            if idTipo == 1:
                return redirect('/admin')
            elif idTipo == 2:
                return redirect('/inventarioAlmacen')
            elif idTipo == 3:
                return redirect('/index')
            else:
                error = 'Tipo de usuario no válido.'
                return render_template('login.html', error=error)
        
        else:
            error = 'Credenciales inválidas. Intente nuevamente.'
            return render_template('login.html', error=error)
    else:
        # Si es una solicitud GET, mostrar el formulario de inicio de sesión
        return render_template('login.html')

@app.route('/logout')
def logout():
    # Cerrar la sesión del usuario y redirigirlo al formulario de inicio de sesión
    session.pop('nombreUsuario', None)
    session.pop('idTipo', None)
    return redirect('/login')

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellidoPaterno = request.form['apellidoPaterno']
        apellidoMaterno = request.form['apellidoMaterno']
        nombreUsuario = request.form['nombreUsuario']
        contrasenaUsuario = request.form['contrasenaUsuario']
        idTipo = request.form['idTipo']
        
        conn = mysql.connector.connect(host='localhost', user='usuario', password='contraseña', database='basededatos')
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO usuario(nombre, apellidoPaterno, apellidoMaterno, nombreUsuario, contrasenaUsuario, idTipo) VALUES(%s, %s, %s, %s, %s, %s)''', (nombre, apellidoPaterno, apellidoMaterno, nombreUsuario, contrasenaUsuario, idTipo))

################## ADMIN ########################################
@app.route('/admin')
def admin():
    if 'idTipo' in session and session['idTipo'] == 1:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT idUsuario, nombreUsuario, nombre, apellidoPaterno, apellidoMaterno, idTipo FROM usuario")
        usuarios = cursor.fetchall()
        cursor.close()

        return render_template('admin.html', usuarios=usuarios)

@app.route('/usuarios/<int:idUsuario>/modificar', methods=['GET', 'POST'])
def modificar_usuario(idUsuario):
    if 'idTipo' in session and session['idTipo'] == 1:
        if request.method == 'POST':
            # Obtener los datos modificados del formulario
            nombre = request.form['nombre']
            apellidoPaterno = request.form['apellidoPaterno']
            apellidoMaterno = request.form['apellidoMaterno']
            idTipo = request.form['idTipo']
            
            cursor = mysql.connection.cursor()
            cursor.execute("UPDATE usuarios SET nombre = %s, apellidoPaterno = %s, apellidoMaterno = %s, idTipo = %s WHERE idUsuario = %s",(nombre, apellidoPaterno, apellidoMaterno, idTipo, idUsuario))
            mysql.connection.commit()
            cursor.close()

            return redirect(url_for('usuarios'))
        else:
            cursor = mysql.connection.cursor()
            cursor.execute("SELECT * FROM usuario WHERE idUsuario = %s", (idUsuario,))
            usuario = cursor.fetchone()
            cursor.close()

            return render_template('modificarUsuarios.html', usuario=usuario)
        
@app.route('/usuarios/<int:idUsuario>/borrar', methods=['POST'])
def borrar_usuario(idUsuario):
    
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM usuario WHERE idUsuario = %s", (idUsuario,))
    mysql.connection.commit()
    cursor.close()

    return redirect(url_for('usuarios'))
        

################## ALMACEN (nosotros) ##########################################
# Pagina principal del almacen
@app.route('/inventarioAlmacen', methods=['GET'])
def inicio():
    if 'idTipo' in session and session['idTipo'] == 2:
        if request.method == 'GET':
            cursor = mysql.connection.cursor()
            cursor.execute('''SELECT * FROM productos''') # corregir consulta
            productos = cursor.fetchall()
            return render_template('inventario.html', productos=productos)
    else:
        return 'Acceso no autorizado'

# Metodo para agregar productos en el inventario del almacen
@app.route('/agregarProducto', methods=['GET','POST'])
def insertar():
    if 'idTipo' in session and session['idTipo'] == 2:
        if request.method == 'GET':
            return render_template('agregarProductos.html')
        if request.method == 'POST':
            nombre = request.form['nombre']
            cantidad = request.form['cantidad']
            cursor = mysql.connection.cursor()
            cursor.execute('''INSERT INTO productos(nombre, cantidad) VALUES(%s, %s)''', (nombre, cantidad))
            cursor.connection.commit()
            cursor.close()
            return inicio()
    else:
        return 'Acceso no autorizado'
    
# Metodo para modificar productos. Funciona pero no muestra los valores actuales antes de que se modifiquen
@app.route('/modificarProducto', methods=['GET','POST'])
def modificar():
    if 'idTipo' in session and session['idTipo'] == 2:
        if request.method == 'GET':
            cursor = mysql.connection.cursor()
            cursor.execute('''SELECT * FROM productos''')
            productos = cursor.fetchall()
            return render_template('modificarProductos.html', productos=productos)
        if request.method == 'POST':
            idProducto = request.form['producto']
            nombre = request.form['nombre']
            cantidad = request.form['cantidad']
            cursor = mysql.connection.cursor()
            cursor.execute('''UPDATE productos SET nombre=%s, cantidad=%s WHERE idProducto=%s''', (nombre, cantidad, idProducto))
            cursor.connection.commit()
            cursor.close()
            return inicio()
    else:
        return 'Acceso no autorizado'

# Metodo para eliminar productos
@app.route('/eliminarProducto', methods=['GET','POST'])
def eliminar():
    if 'idTipo' in session and session['idTipo'] == 2:
        if request.method == 'GET':
            cursor = mysql.connection.cursor()
            cursor.execute('''SELECT * FROM productos''')
            productos = cursor.fetchall()
            return render_template('eliminarProductos.html', productos=productos)
        if request.method == 'POST':
            idProducto = request.form['producto']
            cursor = mysql.connection.cursor()
            cursor.execute('''DELETE FROM productos WHERE idProducto=%s''', (idProducto,))
            cursor.connection.commit()
            cursor.close()
            return inicio()
    else:
        return 'Acceso no autorizado'
    
# Metodo para consultar ruta y rastreo de paquete
@app.route('/rutaAlmacen', methods=['GET','POST'])
def ruta():
    if 'idTipo' in session and session['idTipo'] == 2:
        if request.method == 'GET': # consultar posicion
            cursor = mysql.connection.cursor()
            cursor.execute('''SELECT * FROM productos''')
            return render_template('ruta.html')
        if request.method == 'POST': # mostrar ruta con posicion de consulta
            return
    else:
        return 'Acceso no autorizado'
        
@app.route('/rastreoAlmacen', methods=['GET'])
def rastreo():
    if 'idTipo' in session and session['idTipo'] == 2:
        if request.method == 'GET': # consultar posicion
            cursor = mysql.connection.cursor()
            cursor.execute('''SELECT * FROM productos''')
            return render_template('rastreo.html')
        if request.method == 'POST': # mostrar rastreo con posicion de consulta
            return
    else:
        return 'Acceso no autorizado'
          
########################################################################################

################## TIENDA ##########################################
"""
# Pagina principal de la tienda
@app.route('/inventarioTienda', methods=['GET','POST'])
def inicio():
    if 'idTipo' in session and session['idTipo'] == 3:
        cursor = mysql.connection.cursor()
        cursor.execute('''SELECT * FROM productos''') # corregir consulta
        productos = cursor.fetchall()
        return render_template('inventario.html', productos=productos)
    else :
        return 'Acceso no autorizado'

# Metodo para consultar ruta y rastreo de paquete
@app.route('/rutaTienda', methods=['GET','POST'])
def ruta():
    if 'idTipo' in session and session['idTipo'] == 3:
        if request.method == 'GET':
            cursor = mysql.connection.cursor()
            cursor.execute('''SELECT * FROM productos''')
            return render_template('ruta.html')
        if request.method == 'POST':
            return 
    else :
        return 'Acceso no autoriza"""
        
########################################################################################
    
if __name__ == "__main__":
    app.run(debug=True)