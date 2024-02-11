class Carreras:
    def __init__(self, cliente,provincia,canton,lugar,referencia,tipo,fecha_inicio,comentario,fecha_fin,estado,operador):
        self.cliente = cliente
        self.provincia = provincia
        self.canton = canton
        self.lugar = lugar
        self.referencia = referencia
        self.tipo = tipo
        self.fecha_inicio = fecha_inicio
        self.comentario = comentario
        self.fecha_fin = fecha_fin
        self.estado = estado
        self.operador = operador
        

    def CareDBCollection(self):
        return{
            "cliente":self.cliente,
            "provincia":self.provincia,
            "canton":self.canton,
            "lugar":self.lugar,
            "referencia":self.referencia,
            "tipo":self.tipo,
            "fecha_inicio":self.fecha_inicio,
            "comentario":self.comentario,
            "fecha_fin":self.fecha_fin,
            "estado":self.estado,
            "operador":self.operador,
        }