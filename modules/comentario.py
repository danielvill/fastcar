class Comentario:
    def __init__(self,unidad,comentario,fecha,hora):
        
        self.unidad = unidad
        self.comentario = comentario
        self.fecha = fecha
        self.hora = hora
    
    def ComeDBCollection(self):
        return{
            
            "unidad":self.unidad,
            "comentario":self.comentario,
            "fecha":self.fecha,
            "hora":self.hora,
            
        }
