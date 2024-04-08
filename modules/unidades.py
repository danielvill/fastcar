class Unidades:
    def __init__(self, unidad,placa,modelo,marca,color,observacion,es_fecha):
        self.unidad = unidad
        self.placa = placa
        self.modelo = modelo
        self.marca = marca
        self.color = color
        self.observacion = observacion
        self.es_fecha = es_fecha
        
    def UniDBCollection(self):
        return{
            "unidad":self.unidad,
            "placa":self.placa,
            "modelo":self.modelo,
            "marca":self.marca,
            "color":self.color,
            "observacion":self.observacion,
            "es_fecha":self.es_fecha,        
        }