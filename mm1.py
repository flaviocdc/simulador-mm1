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

def gerar_proxima_chegada(tx_chegada, tempo):
    quando = tempo + var_exp(tx_chegada)
    return EventoChegada(quando)
    
def gerar_proxima_saida(tx_saida, tempo):
    quando = tempo + var_exp(tx_chegada)
    return EventoSaida(quando)
    
def inserir_ordenado(eventos, evento):
    eventos.append(evento)
    sorted(eventos, key=lambda evt: evt.quando)

def simular(tx_chegada, tx_saida):
    tempo = 0
    eventos = []
    
    inserir_ordenado(eventos, gerar_proxima_chegada(tx_chegada, tempo))
    
    while (True):
        if len(eventos) == 0:
            break
        
        evento = eventos.pop(0)
        
        if isinstance(evento, EventoChegada):
            # gerando a proxima chegada
            inserir_ordenado(eventos, gerar_proxima_chegada(tx_chegada, tempo))
            
            
            

        
        

simular(txs_chegadas[0], tx_saida)