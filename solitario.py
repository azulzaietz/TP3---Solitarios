from mesa import Mesa
from mazo import crear_mazo
from carta import criterio, CONSECUTIVA
from mesa import SALIR, FUNDACION, PILA_TABLERO
from pila_cartas import PilaCartas, SolitarioError

class SolitarioEliminador:
    """Interfaz para implementar un solitario."""

    def __init__(self, mesa):
        """Inicializa con una mesa creada y vacía."""
        self.mesa = mesa

    def armar(self):
        """Arma el tablero con la configuración inicial."""
        self.mesa.mazo = crear_mazo()

        for i in range(6):
            self.mesa.fundaciones.append(PilaCartas(criterio_apilar=criterio(orden=CONSECUTIVA)))

        for i in range(4):
            self.mesa.pilas_tablero.append(PilaCartas(pila_visible=True))
            #e = 0
            #while not mazo.es_vacia():
             #   self.mesa.pilas_tablero[e % len(self.mesa.pilas_tablero)].apilar(mazo.desapilar())
              #  e +=1

            while not self.mesa.mazo.es_vacia():
                for pila in self.mesa.pilas_tablero:
                    pila.apilar(self.mesa.mazo.desapilar())

    def termino(self):
        """Avisa si el juego se terminó."""
        for pila in self.mesa.pilas_tablero:
            if not pila.es_vacia():
                return False
        return True

    def jugar(self, jugada):
        """Efectúa una movida.
            La jugada es una lista de pares (PILA, numero). (Ver mesa.)
            Si no puede realizarse la jugada se levanta una excepción SolitarioError *descriptiva*."""
        accion, lugar = jugada
        if lugar == 0:
            raise SolitarioError("La posicion indicada no es válida")
