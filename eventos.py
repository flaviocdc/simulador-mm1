class EventoChegada:
    quando = 0
    
    def __init__(self, quando):
        self.quando = quando
    
    def __str__(self):
        return 'EventoChegada[quando=%f]' % self.quando
        
class EventoSaida:
    quando = 0
    
    def __init__(self, quando):
        self.quando = quando
    
    def __str__(self):
        return 'EventoSaida[quando=%f]' % self.quando