from simulador import *
from util import *


tx_saida = 0.1
txs_chegadas = [ tx_chegada(0.5, tx_saida), tx_chegada(0.7, tx_saida), tx_chegada(0.9, tx_saida) ]
#txs_chegadas = [ tx_chegada(0.9, tx_saida) ]

for tx_chegada in txs_chegadas:
    print '#####################################'
    
    print 'Executando simulador para os seguintes parametros:'
    print '- taxa de chegada %f' % tx_chegada
    print '- taxa de saida %f' % tx_saida
    
    sim = Simulador(tx_chegada, tx_saida)
    sim.simular()
    
    print 'Tempo medio de espera (somando o tempo de espera de todos os clientes): %f' % sim.tempo_medio_espera()
    print 'Tempo medio de espera (calculado a partir de amostras): %f' % sim.tempo_medio_amostral()
    print 'Desvio-padrao amostral %f' % sim.desvio_padrao_amostral()
    
    formula = (sim.tx_chegada / (sim.tx_saida * (sim.tx_saida - sim.tx_chegada)))
    
    print 'Tempo medio de espera (calculado a partir da formula (lambda / (mi * (mi - lambda))) ): %f' % formula

    print '#####################################'