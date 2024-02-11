class Conductores:
    def __init__(self, cedula,nombre,email,telefono,direccion,em_nombre,em_telefono,em_relacion,clave,licencia):
        self.cedula = cedula
        self.nombre = nombre
        self.email = email
        self.telefono = telefono
        self.direccion = direccion
        self.em_nombre = em_nombre
        self.em_telefono = em_telefono
        self.em_relacion = em_relacion
        self.clave = clave
        self.licencia = licencia
        

    def CondDBCollection(self):
        return{
            "cedula":self.cedula,
            "nombre":self.nombre,
            "email":self.email,
            "telefono":self.telefono,
            "direccion":self.direccion,
            "em_nombre":self.em_nombre,
            "em_telefono":self.em_telefono,
            "em_relacion":self.em_relacion,
            "clave":self.clave,
            "licencia":self.licencia,
            
        }