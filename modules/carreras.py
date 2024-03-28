class Carreras:
    def __init__(self, cliente,unidad,comentario,fecha,hora):
        self.cliente = cliente
        self.unidad = unidad
        self.comentario = comentario
        self.fecha = fecha
        self.hora = hora
        

    def CareDBCollection(self):
        return{
            "cliente":self.cliente,
            "unidad":self.unidad,
            "comentario":self.comentario,
            "fecha":self.fecha,
            "hora":self.hora,
            
        }