from random import uniform
from numpy import log

def var_exp(taxa):
    return -1 * log(1 - uniform(0, 1)) / taxa

def tx_chegada(ro, mi):
    return ro * mi
