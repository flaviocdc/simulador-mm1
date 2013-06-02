class Evento:
    quando = 0
    
    def __init__(self, quando):
        self.quando = quando


class EventoChegada(Evento):
    def __str__(self):
        return 'EventoChegada[quando=%f]' % self.quando
        
class EventoSaida(Evento):
    def __str__(self):
        return 'EventoSaida[quando=%f]' % self.quando
        
class Cliente:
    chegou = 0
    saiu = 0
    nome = ''
    
    def __init__(self, nome):
        self.nome = 'Cliente-%d' % nome