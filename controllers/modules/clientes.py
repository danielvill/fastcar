class Clientes:
    def __init__(self, nombre,telefono,direccion,coordenadas,cedula,referencia,comentario):
        self.nombre = nombre
        self.telefono = telefono
        self.direccion = direccion
        self.coordenadas = coordenadas
        self.cedula = cedula
        self.referencia = referencia
        self.comentario = comentario
        
        

    def CliDBCollection(self):
        return{
            "nombre":self.nombre,
            "telefono":self.telefono,
            "direccion":self.direccion,
            "coordenadas":self.coordenadas,
            "cedula":self.cedula,
            "referencia":self.referencia,
            "comentario":self.comentario,
            
            
        }