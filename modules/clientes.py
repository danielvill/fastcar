class Clientes:
    def __init__(self, nombre,telefono,direccion,provincia,canton,referencia,comentario):
        self.nombre = nombre
        self.telefono = telefono
        self.direccion = direccion
        self.provincia = provincia
        self.canton = canton
        self.referencia = referencia
        self.comentario = comentario
        
        

    def CliDBCollection(self):
        return{
            "nombre":self.nombre,
            "telefono":self.telefono,
            "direccion":self.direccion,
            "provincia":self.provincia,
            "canton":self.canton,
            "referencia":self.referencia,
            "comentario":self.comentario,
            
            
        }