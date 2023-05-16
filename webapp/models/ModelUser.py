from .entities.User import User

class ModelUser():
    @classmethod
    def login(self, mysql, User):
        try:
            cursor=mysql.connection.cursor()
            sql="""SELECT idUsuario, usuario, password FROM login 
                WHERE usuario = '{}'""". format(User.usuario) # consulta a la tabla 
            cursor.execute(sql)
            row=cursor.fetchone()
            if row != None:
                User=User(row[0], row[1],User.check_password(row[2], User.password))
                return User
            else:
                return None
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_by_id(self, mysql, idUsuario):
        try:
            cursor=mysql.connection.cursor()
            sql="SELECT idUsuario, nombreU FROM Usuarios WHERE id = {}". format(idUsuario)
            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:
                return User(row[0], row[1], row[2])
            else:
                return None
        except Exception as ex:
            raise Exception(ex)