class Usuario:
    def __init__(self, cedula,nombre,rol,email,clave):
        self.cedula = cedula
        self.nombre = nombre
        self.rol = rol
        self.email = email
        self.clave = clave
        

    def UsuDBCollection(self):
        return{
            "cedula":self.cedula,
            "nombre":self.nombre,
            "rol":self.rol,
            "email":self.email,
            "clave":self.clave,
            
        }