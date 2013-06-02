from random import random
from numpy import log
from collections import deque
from eventos import *

def uniforme():
    return random()
    
def var_exp(taxa):
    return -1 * log(uniforme()) / taxa

def tx_chegada(ro, mi):
    return ro * mi

tx_saida = 0.1
txs_chegadas = [ tx_chegada(0.5, tx_saida), tx_chegada(0.7, tx_saida), tx_chegada(0.9, tx_saida) ]

def inserir_ordenado(eventos, evento):
    eventos.append(evento)
    sorted(eventos, key=lambda evt: evt.quando)


class Simulador:
    tempo = 0.0
    eventos = []
    fila = deque()
    tx_chegada = 0.0
    tx_saida = 0.0
    total_clientes = 0
    servidor_ocupado = False
    
    def __init__(self, tx_chegada, tx_saida):
        self.tx_chegada = tx_chegada
        self.tx_saida = tx_saida
        
    def gerar_proxima_chegada(self, cliente):
        quando = self.tempo + var_exp(self.tx_chegada)
        return EventoChegada(quando, cliente)
    
    def gerar_proxima_saida(self, cliente):
        quando = self.tempo + var_exp(self.tx_saida)
        return EventoSaida(quando, cliente)
        
    def criar_novo_cliente(self):
        self.total_clientes = self.total_clientes + 1
        return Cliente(self.total_clientes)
        
    def imprimir_estado(self):
        print 'Estado do simulador:'
        print '- Tempo Atual: %f', self.tempo
        print '- Total clientes: %d' % self.total_clientes
        print '- Servidor ocupado: %s' % self.servidor_ocupado
        print '- Eventos a processar'
        print map(lambda evt:'%s' % str(evt), self.eventos)
        print '- Fila'
        print map(lambda client:'%s' % str(client), self.fila)
    
    def simular(self):
        print 'Iniciando simulacao'
        
        cliente = self.criar_novo_cliente()
        inserir_ordenado(self.eventos, self.gerar_proxima_chegada(cliente))
        
        while (True):
            evento = self.eventos.pop(0)
            
            if isinstance(evento, EventoChegada):        
                # quem chegou
                cliente = evento.cliente
                cliente.chegou = self.tempo
                
                # inserindo cliente na fila
                self.fila.append(cliente)
                
                # avancando o tempo
                self.tempo = evento.quando
                
                print 'Alguem chegou  %s as %f' % (cliente, evento.quando)
                
                # gerando a proxima chegada
                inserir_ordenado(self.eventos, self.gerar_proxima_chegada(self.criar_novo_cliente()))
                
            elif isinstance(evento, EventoSaida):
                # quem esta saindo
                evento.cliente.saiu = self.tempo
                
                # servidor nao esta mais ocupado
                self.servidor_ocupado = False
                
                print 'Alguem saiu  %s as %f' % (cliente, evento.quando)
            
            if len(self.fila) != 0 and not self.servidor_ocupado:
                cliente = self.fila.popleft()
                
                print 'Servidor atendendo a %s as %f' % (cliente, self.tempo)
                
                cliente.atendido = self.tempo
                inserir_ordenado(self.eventos, self.gerar_proxima_saida(cliente))
            
            self.imprimir_estado()
                        
            try:
                raw_input('Qualquer tecla para a proxima iteracao...')
            except exceptions.EOFError:
                pass
        
Simulador(txs_chegadas[0], tx_saida).simular()