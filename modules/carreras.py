class Carreras:
    def __init__(self, cliente,unidad,estado):
        self.cliente = cliente
        self.unidad = unidad
        self.estado = estado
        

    def CareDBCollection(self):
        return{
            "cliente":self.cliente,
            "unidad":self.unidad,
            "estado":self.estado,
            
        }