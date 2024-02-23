class Unidades:
    def __init__(self, unidad,placa,modelo,marca,color,observacion,orden,es_codigo,es_tipo,es_fecha):
        self.unidad = unidad
        self.placa = placa
        self.modelo = modelo
        self.marca = marca
        self.color = color
        self.observacion = observacion
        self.orden = orden
        self.es_codigo = es_codigo
        self.es_tipo = es_tipo
        self.es_fecha = es_fecha
        
    def UniDBCollection(self):
        return{
            "unidad":self.unidad,
            "placa":self.placa,
            "modelo":self.modelo,
            "marca":self.marca,
            "color":self.color,
            "observacion":self.observacion,
            "orden":self.orden,
            "es_codigo":self.es_codigo,
            "es_tipo":self.es_tipo,
            "es_fecha":self.es_fecha,        
        }