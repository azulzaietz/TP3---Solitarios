from carta import PICAS, DIAMANTES, CORAZONES, TREBOLES
from pila_cartas import PilaCartas
import random
from carta import Carta

def crear_mazo(mazos=1, palos=4):
    """Devuelve una PilaCartas con las cartas boca abajo y mezcladas.
    Cada mazo de los mazos tiene 52 cartas, y puede ser completado con 1, 2 o 4 palos.
    En caso de que estén los 4 palos el mazo se conformará con la serie del 1 al 13
    para cada uno de ellos, en caso de ser sólo 2 palos serán 2 veces la serie 1 al 13
    para dos palos del mismo color y en caso de ser 1 sólo palo será 4 veces la serie 1 al 13
    para ese palo."""
    
    mazo = PilaCartas()
    lista_mazo = []
    palos = (PICAS, CORAZONES, DIAMANTES, TREBOLES)
    for p in palos:
        for i in range (1, 14):
            lista_mazo.append(Carta(i,p))
    random.shuffle(lista_mazo) #PREGUNTAR POR RANDOM P OBJETOS #Era asi enzo, pero poniendo directo random. sin nada antes
    for carta in lista_mazo:
        mazo.apilar(carta, forzar=True)
    return mazo

#prueba para actualizar desde pycharm