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
            for j in range(13):
                self.mesa.pilas_tablero[i].apilar(self.mesa.mazo.desapilar(), forzar=True)
            self.mesa.pilas_tablero[i].tope().voltear()

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
        pila1, cual1 = jugada[0]
        pila2, cual2 = jugada[1]
        print(jugada)
        if pila1 == FUNDACION:
            raise SolitarioError("Solo se puede mover cartas del tablero a las fundaciones, una vez en la fundacion no se puede mover mas")
        elif pila1 == PILA_TABLERO and pila2 == FUNDACION:
            if self.mesa.pilas_tablero[cual1].es_vacia():
                raise SolitarioError("La pila está vacía")
            self.mesa.fundaciones[cual2].apilar(self.mesa.pilas_tablero[cual1].tope())
            self.mesa.pilas_tablero[cual1].desapilar()
            if not self.mesa.pilas_tablero[cual1].es_vacia() and self.mesa.pilas_tablero[cual1].tope().boca_abajo:
                self.mesa.pilas_tablero[cual1].tope().voltear()
        else:
            raise SolitarioError("Movimiento invalido")


