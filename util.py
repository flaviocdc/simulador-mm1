from random import random
from numpy import log

def uniforme():
    return random()
    
def var_exp(taxa):
    return -1 * log(uniforme()) / taxa

def tx_chegada(ro, mi):
    return ro * mi
