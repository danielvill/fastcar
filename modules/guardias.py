class Guardias:
    def __init__(self,unidad):
        
        self.unidad = unidad
        

    def GuardDBCollection(self):
        return{
            
            "unidad":self.unidad,
            
        }
