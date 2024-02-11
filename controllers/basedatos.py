from pymongo import MongoClient

MONGO_URI = 'mongodb://localhost:27017'

def Conexion():
    try:
        client = MongoClient(MONGO_URI)
        db = client["fastcar"]
        print("Conexión  exitosa.")
    except ConnectionError:
        print('Error de conexión con la bdd')
    return db
