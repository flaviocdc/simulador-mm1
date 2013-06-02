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
    tempo = 0
    eventos = []
    fila = deque()
    tx_chegada = 0
    tx_saida = 0
    
    def __init__(self, tx_chegada, tx_saida):
        self.tx_chegada = tx_chegada
        self.tx_saida = tx_saida
        
    
    def gerar_proxima_chegada(self):
        quando = self.tempo + var_exp(self.tx_chegada)
        return EventoChegada(quando)
    
    def gerar_proxima_saida(self):
        quando = self.tempo + var_exp(self.tx_saida)
        return EventoSaida(quando)
    
    def simular(self):
        inserir_ordenado(self.eventos, self.gerar_proxima_chegada())
        
        while (True):
            # TODO remover dps
            if len(self.eventos) == 0:
                break
            
            evento = self.eventos.pop(0)
            
            if isinstance(evento, EventoChegada):
                # gerando a proxima chegada
                inserir_ordenado(self.eventos, self.gerar_proxima_chegada())
        
        
Simulador(txs_chegadas[0], tx_saida).simular()