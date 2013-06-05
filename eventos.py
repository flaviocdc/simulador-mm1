class Evento:
    
    def __init__(self, quando, cliente, rodada):
        self.cliente = cliente
        self.quando = quando
        self.rodada = rodada

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
    def __init__(self, nome):
        self.nome = 'Cliente-%d' % nome
        self.chegou = 0
        self.atendido = 0
        self.saiu = 0

    def __str__(self):
        return self.nome

    def tempo_espera(self):
        return self.atendido - self.chegou

    def tempo_servico(self):
        return self.saiu - self.atendido