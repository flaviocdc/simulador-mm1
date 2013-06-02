from simulador import *
from util import *


tx_saida = 0.1
txs_chegadas = [ tx_chegada(0.5, tx_saida), tx_chegada(0.7, tx_saida), tx_chegada(0.9, tx_saida) ]

Simulador(txs_chegadas[0], tx_saida).simular()