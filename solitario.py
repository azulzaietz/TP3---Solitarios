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
        accion, lugar = jugada
        if lugar <= 0 or lugar > len(self.mesa.fundaciones):
            raise SolitarioError("La posicion indicada no es válida")
        elif accion != SALIR:
            self.mesa.fundaciones[int(lugar)-1].apilar(self.mesa.pilas_tablero[int(accion)-1])

    def _carta_a_fundacion(self, pila, fundacion):
        if self.mesa.fundaciones[fundacion].es_vacia() and not self.mesa.pilas_tablero[pila].es_vacia():
            self.mesa.fundaciones[fundacion].apilar(self.mesa.pilas_tablero[pila])
