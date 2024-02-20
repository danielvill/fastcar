class Guardias:
    def __init__(self,n_conductor,unidad):
        self.n_conductor = n_conductor
        self.unidad = unidad
        

    def GuardDBCollection(self):
        return{
            "n_conductor":self.n_conductor,
            "unidad":self.unidad,
            
        }
