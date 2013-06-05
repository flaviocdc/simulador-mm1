from collections import deque
from eventos import *
from util import var_exp
from exceptions import EOFError

class Simulador:
    
    def __init__(self, tx_chegada, tx_saida):
        self.tx_chegada = tx_chegada
        self.tx_saida = tx_saida

        self.tempo = 0.0

        self.eventos = []
        self.fila = deque()
        self.total_clientes = 0
        self.servidor_ocupado = False
        self.debug = False

        self.todos_clientes_atendidos = []

        self.amostras = []
        self.clientes_atendidos_rodada = []
        self.rodada = 0

    def inserir_ordenado(self, evento):
        self.eventos.append(evento)
        self.eventos = sorted(self.eventos, key=lambda evt: evt.quando)
        
    def gerar_proxima_chegada(self, cliente):
        quando = self.tempo + var_exp(self.tx_chegada)
        return EventoChegada(quando, cliente, self.rodada)
    
    def gerar_proxima_saida(self, cliente):
        quando = self.tempo + var_exp(self.tx_saida)
        return EventoSaida(quando, cliente, self.rodada)
        
    def criar_novo_cliente(self):
        self.total_clientes = self.total_clientes + 1

        if self.debug:
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
        print '- Amostras %s' % self.amostras
        print '- Rodada %d' % self.rodada
        print '- Todos clientes atendidos: %d' % len(self.todos_clientes_atendidos)
        print '###################################'
    
    def simular(self):
        if self.debug:
            print '# Iniciando simulacao'
            print '# Taxa de chegadas: %f' % self.tx_chegada
            print '# Taxa de servico: %f' % self.tx_saida
        
        primeiro_cliente = self.criar_novo_cliente()
        self.inserir_ordenado(self.gerar_proxima_chegada(primeiro_cliente))
        
        while (self.tempo <= 100000):
            evento = self.eventos.pop(0)
            
            self.rodada = self.rodada + 1
            
            if self.rodada % 100 == 0:
                amostra = (reduce(lambda x, cliente: x + cliente.tempo_espera(), self.clientes_atendidos_rodada, 0)) / len(self.clientes_atendidos_rodada)
                
                # guardando a amostra
                self.amostras.append(amostra)
                
                # limpando os clientes atendidos nesta rodada
                self.clientes_atendidos_rodada = []

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
                
                # adicionando a lista de clientes atendidos
                self.todos_clientes_atendidos.append(evento.cliente)
                
                # adicionando a lista de clientes atendidos nesta rodada
                self.clientes_atendidos_rodada.append(evento.cliente)

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

    def tempo_medio_espera(self):
        soma = reduce(lambda x, cliente: x + cliente.tempo_espera(), self.todos_clientes_atendidos, 0)
        return soma / len(self.todos_clientes_atendidos)
        
    def tempo_medio_amostral(self):
        return sum(self.amostras) / len(self.amostras)
        
    def desvio_padrao_amostral(self):
        media = self.tempo_medio_amostral()
        v = 0
        
        for amostra in self.amostras:
            temp = amostra - media
            temp = pow(temp, 2)
            v = v + temp
            
        desvio = v / (len(self.amostras) - 1)
        
        return desvio
        