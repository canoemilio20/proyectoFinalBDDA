class Config:
    SECRET_KEY = 'B1O029@xqieNA!-P45^'

class DevelopmentConfig(Config):
    DEBUG=True
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'usuario'
    MYSQL_PASSWORD = '111'
    MYSQL_DB = 'elatico'


config={
    'development': DevelopmentConfig
}