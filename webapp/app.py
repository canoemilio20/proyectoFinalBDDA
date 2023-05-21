from flask import Flask, render_template, request, session, redirect, url_for
from flask_mysqldb import MySQL
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
            return render_template('pedidos.html', nombreUsuario=nombreUsuario)
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
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM usuario WHERE nombreUsuario = %s AND contrasenaUsuario = %s", (nombreUsuario, contrasenaUsuario))
        user = cursor.fetchone()
        cursor.close()

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
                return redirect('/pedidos')
            else:
                error = 'Tipo de usuario no válido.'
                return render_template('login.html', error=error)
        
        else:
            error = 'Credenciales inválidas. Intente nuevamente.'
            return render_template('login.html', error=error)
    else:
        # Si es una solicitud GET, mostrar el formulario de inicio de sesión
        return render_template('login.html')

@app.route('/registro', methods=['POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellidoPaterno = request.form['apellidoPaterno']
        apellidoMaterno = request.form['apellidoMaterno']
        nombreUsuario = request.form['nombreUsuario']
        contrasenaUsuario = request.form['contrasenaUsuario']
        idTipo = request.form['idTipo']
        cursor = mysql.connection.cursor()
        cursor.execute('''INSERT INTO usuario(nombre, apellidoPaterno, apellidoMaterno, nombreUsuario, contrasenaUsuario, idTipo) VALUES(%s, %s, %s, %s, %s, %s)''', (nombre, apellidoPaterno, apellidoMaterno, nombreUsuario, contrasenaUsuario, idTipo))
        cursor.close()
        return login()

@app.route('/logout')
def logout():
    # Cerrar la sesión del usuario y redirigirlo al formulario de inicio de sesión
    session.pop('nombreUsuario', None)
    session.pop('idTipo', None)
    return redirect('/login')

################## ADMIN ########################################
@app.route('/admin')
def administrador():
    if 'idTipo' in session and session['idTipo'] == 1:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT idUsuario, nombreUsuario, contrasenaUsuario, nombre, apellidoPaterno, apellidoMaterno, idTipo FROM usuario WHERE idTipo <> 1")
        usuarios = cursor.fetchall()
        cursor.close()
        return render_template('admin.html', usuarios=usuarios)
    else:
        return 'Acceso no autorizado'

@app.route('/agregarUsuario', methods=['GET', 'POST'])
def agregarUsuario():
    if 'idTipo' in session and session['idTipo'] == 1:
        if request.method == 'GET':
            return render_template('agregarUsuarios.html')
        if request.method == 'POST':
            nombreUsuario = request.form['nombreUsuario']
            contrasenaUsuario = request.form['contrasenaUsuario']
            nombre = request.form['nombre']
            apellidoPaterno = request.form['apellidoPaterno']
            apellidoMaterno = request.form['apellidoMaterno']
            idTipo = request.form['idTipo']
            cursor = mysql.connection.cursor()
            cursor.execute("INSERT INTO usuario(nombreUsuario, contrasenaUsuario, nombre, apellidoPaterno, apellidoMaterno, idTipo) VALUES(%s,%s,%s,%s,%s,%s)", (nombreUsuario, contrasenaUsuario, nombre, apellidoPaterno, apellidoMaterno, idTipo))
            cursor.connection.commit()
            cursor.close()
            return administrador()
    else:
        return 'Acceso no autorizado'

@app.route('/eliminarUsuario/<int:idUsuario>', methods=['GET'])
def eliminarUsuario(idUsuario):
    if 'idTipo' in session and session['idTipo'] == 1:
        if request.method == 'GET':
            cursor = mysql.connection.cursor()
            cursor.execute("DELETE FROM usuario WHERE idUsuario = %s", (idUsuario,))
            mysql.connection.commit()
            cursor.close()
            return administrador()
    else:
        return 'Acceso no autorizado'


################## ALMACEN (nosotros) ##########################################
# Pagina principal del almacen
@app.route('/inventarioAlmacen')
def inicio():
    if 'idTipo' in session and session['idTipo'] == 2:
        cursor = mysql.connection.cursor()
        cursor.execute('''SELECT p.nombreProducto, c.cantidadProducto FROM producto p JOIN contiene c ON p.idProducto = c.idProducto ''')
        productos = cursor.fetchall()
        cursor.close()
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
            nombre = request.form['nombreProducto']
            cantidad = request.form['cantidadProducto']
            cursor = mysql.connection.cursor()
            cursor.execute('''INSERT INTO producto(nombreProducto) VALUES (%s)''', (nombre,))
            cursor.execute('''INSERT INTO contiene(idProducto, cantidadProducto) SELECT idProducto, %s FROM producto WHERE nombreProducto = %s''', (cantidad, nombre,))
            cursor.connection.commit()
            cursor.close()
            return inicio()
    else:
        return 'Acceso no autorizado'
    
# Metodo para modificar productos
@app.route('/modificarProducto', methods=['GET','POST'])
def modificar():
    if 'idTipo' in session and session['idTipo'] == 2:
        if request.method == 'GET':
            cursor = mysql.connection.cursor()
            cursor.execute('''SELECT * FROM producto''')
            productos = cursor.fetchall()
            cursor.close()
            return render_template('modificarProductos.html', productos=productos)
        if request.method == 'POST':
            idProducto = request.form['producto']
            nombre = request.form['nombre']
            cantidad = request.form['cantidad']
            cursor = mysql.connection.cursor()
            cursor.execute('''UPDATE producto SET nombreProducto=%s WHERE idProducto=%s''', (nombre, idProducto))
            cursor.execute('''UPDATE contiene SET cantidadProducto=%s WHERE idProducto=%s''', (cantidad, idProducto,))
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
            cursor.execute('''SELECT * FROM producto''')
            productos = cursor.fetchall()
            cursor.close()
            return render_template('eliminarProductos.html', productos=productos)
        if request.method == 'POST':
            idProducto = request.form['producto']
            cursor = mysql.connection.cursor()
            cursor.execute('''DELETE FROM producto WHERE idProducto=%s''', (idProducto,))
            cursor.connection.commit()
            cursor.close()
            return inicio()
    else:
        return 'Acceso no autorizado'
    
# Metodo para consultar ruta y rastreo de paquete
@app.route('/rutaAlmacen')
def rutaAlmacen():
    if 'idTipo' in session and session['idTipo'] == 2:
        return render_template('rutaAlmacen.html')
    else:
        return 'Acceso no autorizado'
        
@app.route('/rastreoAlmacen', methods=['GET'])
def rastreoAlmacen():
    if 'idTipo' in session and session['idTipo'] == 2:
        return render_template('rastreoAlmacen.html')
    else:
        return 'Acceso no autorizado'

########################################################################################

################## TIENDA ##########################################
@app.route('/pedidos')
def pedidos():
    if 'idTipo' in session and session['idTipo'] == 3:
        cursor = mysql.connection.cursor()
        cursor.execute('''SELECT p.idPedido, t.nombreTienda, pr.nombreProducto, p.cantidadPedido, p.fechaPedido, p.fechaEntrega, p.status FROM pedido p JOIN tienda t ON p.idTienda = t.idTienda JOIN producto pr ON p.idProducto = pr.idProducto''')
        pedidos = cursor.fetchall()
        cursor.close()
        return render_template('pedidos.html', pedidos=pedidos)
    else:
        return 'Acceso no autorizado'
    
@app.route('/cambiarStatus/<int:idPedido>', methods=['GET'])
def status(idPedido):
    if 'idTipo' in session and session['idTipo'] == 3:
        if request.method == 'GET':
            cursor = mysql.connection.cursor()
            cursor.execute("UPDATE pedido SET fechaEntrega=CURDATE() WHERE idPedido = %s", (idPedido,))
            cursor.execute("UPDATE pedido SET status='Entregado' WHERE idPedido = %s", (idPedido,))
            mysql.connection.commit()
            cursor.close()
            return pedidos()
    else:
        return 'Acceso no autorizado'

@app.route('/hacerPedido', methods=['GET','POST'])
def pedido():
    if 'idTipo' in session and session['idTipo'] == 3:
        if request.method == 'GET':
            cursor = mysql.connection.cursor()
            cursor.execute('''SELECT * FROM tienda''')
            tiendas = cursor.fetchall()
            cursor.execute('''SELECT * FROM producto''')
            productos = cursor.fetchall()
            cursor.close()
            return render_template('hacerPedido.html', tiendas=tiendas, productos=productos)
        if request.method == 'POST':
            tienda = request.form['tienda']
            producto = request.form['producto']
            cantidad = request.form['cantidad']
            cursor = mysql.connection.cursor()
            cursor.execute('''SELECT a.idAlmacen FROM accede AS a INNER JOIN tienda AS t ON a.idTienda = t.idTienda WHERE t.nombreTienda = %s''', (tienda))
            idAlmacen = cursor.fetchone()
            cursor.execute('''SELECT idTienda FROM tienda WHERE nombreTienda = %s''', (tienda))
            idTienda = cursor.fetchone()
            cursor.execute('''SELECT idProducto FROM producto WHERE nombreProducto = %s''', (producto))
            idProducto = cursor.fetchone()
            cursor.execute('''INSERT INTO pedido(idAlmacen, idTienda, idProducto, cantidadPedido, fechaPedido) VALUES (%s,%s,%s,%s,CURDATE())''', (idAlmacen, idTienda, idProducto, cantidad))
            cursor.connection.commit()
            cursor.close()
            return pedidos()
    else:
        return 'Acceso no autorizado'

@app.route('/rutaTienda')
def rutaTienda():
    if 'idTipo' in session and session['idTipo'] == 3:
        return render_template('rutaTienda.html')
    else:
        return 'Acceso no autorizado'
        
@app.route('/rastreoTienda', methods=['GET'])
def rastreoTienda():
    if 'idTipo' in session and session['idTipo'] == 3:
        return render_template('rastreoTienda.html')
    else:
        return 'Acceso no autorizado'
####################################################3####################################
    
if __name__ == "__main__":
    app.run(debug=True)