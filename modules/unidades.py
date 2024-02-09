class Unidades:
    def __init__(self, placa,modelo,marca,codigo,kilometraje,observacion,orden,es_codigo,es_tipo,es_fecha):
        self.placa = placa
        self.modelo = modelo
        self.marca = marca
        self.codigo = codigo
        self.kilometraje = kilometraje
        self.observacion = observacion
        self.orden = orden
        self.es_codigo = es_codigo
        self.es_tipo = es_tipo
        self.es_fecha = es_fecha
        
    def UniDBCollection(self):
        return{
            "placa":self.placa,
            "modelo":self.modelo,
            "marca":self.marca,
            "codigo":self.codigo,
            "kilometraje":self.kilometraje,
            "observacion":self.observacion,
            "orden":self.orden,
            "es_codigo":self.es_codigo,
            "es_tipo":self.es_tipo,
            "es_fecha":self.es_fecha,        
        }