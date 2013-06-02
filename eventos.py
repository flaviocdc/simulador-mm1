class Evento:
    quando = 0
    tipo = ''
    cliente = None
    
    def __init__(self, quando, cliente):
        self.cliente = cliente
        self.quando = quando

class EventoChegada(Evento):
    def __str__(self):
        return 'EventoChegada[cliente=%s, quando=%f]' % (self.cliente, self.quando)
        
class EventoSaida(Evento):
    def __str__(self):
        return 'EventoSaida[cliente=%s, quando=%f]' % (self.cliente, self.quando)

class EventoAdicionarFila(Evento):    
    def __str__(self):
        return 'EventoAdicionarFila[cliente=%s, quando=%f]' % (self.cliente, self.quando)
        
class EventoSaiuFila(Evento):    
    def __str__(self):
        return 'EventoAdicionarFila[cliente=%s, quando=%f]' % (self.cliente, self.quando)

class Cliente:
    chegou = 0
    atendido = 0
    saiu = 0
    nome = ''
    
    def __init__(self, nome):
        self.nome = 'Cliente-%d' % nome
    
    def __str__(self):
        return self.nome