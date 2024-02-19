class Guardias:
    def __init__(self,n_conductor,unidad,codigo,estado):
        self.n_conductor = n_conductor
        self.unidad = unidad
        self.codigo = codigo
        self.estado = estado

    def GuardDBCollection(self):
        return{
            "n_conductor":self.n_conductor,
            "unidad":self.unidad,
            "codigo":self.codigo,
            "estado":self.estado   
        }
