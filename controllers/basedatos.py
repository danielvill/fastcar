from pymongo import MongoClient

MONGO_URI = 'mongodb://localhost:27017'


def Conexion():
    try:
        client = MongoClient(MONGO_URI)
        db = client["fastcar"]
        collection = db['carreras']  # Usamos la colección 'carreras'

        # Agregación para contar el número de veces que aparece cada cliente
        pipeline = [
            {"$group": {"_id": "$cliente", "count": {"$sum": 1}}}
        ]
        results = list(collection.aggregate(pipeline))

        print("Conexión y agregación exitosas.")
    except ConnectionError:
        print('Error de conexión con la bdd')
    return db, results  # Devolvemos los resultados de la agregación