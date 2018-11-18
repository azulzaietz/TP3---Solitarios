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

    nombresPalos = [PICAS, CORAZONES, DIAMANTES, TREBOLES]

    if mazos == 1 and palos == 4:
        mazo = PilaCartas()
        lista_mazo = []
        for p in nombresPalos:
            for i in range(1, 14):
                lista_mazo.append(Carta(i, p))
        random.shuffle(lista_mazo)
        for carta in lista_mazo:
            mazo.apilar(carta, forzar=True)
        return mazo
    if mazos == 2 and palos == 1:
        mazo = PilaCartas()
        l_mazo1 = []
        l_mazo2 = []
        palo = random.choice(nombresPalos)
        for j in range(4):
            for i in range(1, 14):
                l_mazo1.append(Carta(i, palo))
                l_mazo2.append(Carta(i, palo))
        random.shuffle(l_mazo1)
        random.shuffle(l_mazo2)
        for carta in l_mazo1:
            mazo.apilar(carta, forzar=True)
        for carta in l_mazo2:
            mazo.apilar(carta, forzar=True)
        return mazo

