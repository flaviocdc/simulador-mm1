from collections import deque
from eventos import *
from util import var_exp
from exceptions import EOFError

class Simulador:
    tempo = 0.0
    eventos = []
    fila = deque()
    tx_chegada = 0.0
    tx_saida = 0.0
    total_clientes = 0
    servidor_ocupado = False
    debug = False
    
    def __init__(self, tx_chegada, tx_saida):
        self.tx_chegada = tx_chegada
        self.tx_saida = tx_saida
    
    def inserir_ordenado(self, evento):
        self.eventos.append(evento)
        self.eventos = sorted(self.eventos, key=lambda evt: evt.quando)
        
    def gerar_proxima_chegada(self, cliente):
        quando = self.tempo + var_exp(self.tx_chegada)
        return EventoChegada(quando, cliente)
    
    def gerar_proxima_saida(self, cliente):
        quando = self.tempo + var_exp(self.tx_saida)
        return EventoSaida(quando, cliente)
        
    def criar_novo_cliente(self):
        self.total_clientes = self.total_clientes + 1
        print 'Criando novo cliente %d' % self.total_clientes
        return Cliente(self.total_clientes)
        
    def imprimir_estado(self):
        print '###################################'
        print 'Estado do simulador:'
        print '- Tempo Atual: %f' % self.tempo
        print '- Total clientes: %d' % self.total_clientes
        print '- Servidor ocupado: %s' % self.servidor_ocupado
        print '- Eventos a processar'
        print map(lambda evt:'%s' % str(evt), self.eventos)
        print '- Fila'
        print map(lambda client:'%s' % str(client), self.fila)
        print '###################################'
    
    def simular(self):
        if self.debug:
            print '# Iniciando simulacao'
            print '# Taxa de chegadas: %f' % self.tx_chegada
            print '# Taxa de servico: %f' % self.tx_saida
        
        primeiro_cliente = self.criar_novo_cliente()
        self.inserir_ordenado(self.gerar_proxima_chegada(primeiro_cliente))
        
        while (self.tempo <= 10000):
            evento = self.eventos.pop(0)
            
            if isinstance(evento, EventoChegada):
                # avancando o tempo
                self.tempo = evento.quando
                
                # quem chegou
                evento.cliente.chegou = self.tempo
                
                # inserindo cliente na fila
                self.fila.append(evento.cliente)

                if self.debug:
                    print 'Alguem chegou  %s as %f' % (evento.cliente, evento.quando)
                
                # gerando a proxima chegada
                self.inserir_ordenado(self.gerar_proxima_chegada(self.criar_novo_cliente()))
                
            elif isinstance(evento, EventoSaida):
                # avancando o tempo
                self.tempo = evento.quando
                
                # quem esta saindo
                evento.cliente.saiu = self.tempo
                
                # servidor nao esta mais ocupado
                self.servidor_ocupado = False
                
                if self.debug:
                    print 'Alguem saiu  %s as %f' % (evento.cliente, evento.quando)
            
            if len(self.fila) != 0 and not self.servidor_ocupado:
                cliente = self.fila.popleft()
                
                if self.debug:
                    print 'Servidor atendendo a %s as %f' % (cliente, self.tempo)
                
                cliente.atendido = self.tempo
                self.inserir_ordenado(self.gerar_proxima_saida(cliente))
                
                self.servidor_ocupado = True
            
            if self.debug:
                self.imprimir_estado()
                        
            try:
                if self.debug:
                    raw_input('Qualquer tecla para a proxima iteracao...')
            except EOFError:
                pass

        self.imprimir_estado()