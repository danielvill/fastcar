class Media:
    def __init__(self,unidad):
        
        self.unidad = unidad
        

    def MediaDBCollection(self):
        return{
            
            "unidad":self.unidad,
            
        }