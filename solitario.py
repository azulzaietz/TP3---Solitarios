from mesa import Mesa
from mazo import crear_mazo
from carta import criterio, CONSECUTIVA, ASCENDENTE, MISMO_PALO, DESCENDENTE, DISTINTO_COLOR
from mesa import SALIR, FUNDACION, PILA_TABLERO, MAZO, DESCARTE
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
                carta = self.mesa.mazo.desapilar()
                carta.boca_abajo = False
                self.mesa.pilas_tablero[i].apilar(carta, forzar=True)

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
        pila2, cual2 = jugada[1] if len(jugada) == 2 else (SALIR, 0)

        if len(jugada) == 1 and pila1 == MAZO:
            raise SolitarioError("No puede sacar cartas del maso")

        if len(jugada) == 1 and pila1 == PILA_TABLERO:
            for fundacion in self.mesa.fundaciones:
                try:
                    fundacion.apilar(self.mesa.pilas_tablero[cual1].tope())
                    self.mesa.pilas_tablero[cual1].desapilar()
                    return
                except SolitarioError:
                    pass
            #raise SolitarioError("No puede moverse esa carta a ninguna fundación")

        if pila1 == FUNDACION:
            raise SolitarioError("Solo se pueden mover cartas del tablero a las fundaciones. \nUna vez en la fundacion, la carta no se puede mover mas")
        elif pila1 == PILA_TABLERO and pila2 == FUNDACION:
            if self.mesa.pilas_tablero[cual1].es_vacia():
                raise SolitarioError("La pila está vacía")
            self.mesa.fundaciones[cual2].apilar(self.mesa.pilas_tablero[cual1].tope())
            self.mesa.pilas_tablero[cual1].desapilar()
            #if not self.mesa.pilas_tablero[cual1].es_vacia() and self.mesa.pilas_tablero[cual1].tope().boca_abajo:
             #   self.mesa.pilas_tablero[cual1].tope().voltear()
        else:
            raise SolitarioError("Movimiento invalido")

class SolitarioClasico:
    """Interfaz para implementar un solitario."""

    def __init__(self, mesa):
        """Inicializa con una mesa creada y vacía."""
        self.mesa = mesa

    def armar(self):
        """Arma el tablero con la configuración inicial."""
        self.mesa.mazo = crear_mazo(mazos=1, palos=4)
        self.mesa.descarte = PilaCartas()

        for i in range(4):
            self.mesa.fundaciones.append(PilaCartas(criterio_apilar=criterio(palo=MISMO_PALO, orden=DESCENDENTE), valor_inicial=1))

        for i in range(4):
            self.mesa.pilas_tablero.append(PilaCartas(pila_visible=True, criterio_apilar=criterio(palo=DISTINTO_COLOR, orden=ASCENDENTE), criterio_mover=0))
            self.mesa.pilas_tablero[i].apilar(self.mesa.mazo.desapilar(), forzar=True)
            self.mesa.pilas_tablero[i].tope().voltear()

    def termino(self):
        """Avisa si el juego se terminó."""
        total = 0
        for f in self.mesa.fundaciones:
            total += len(f.items)
        if total == 52:
            return True
        else:
            return False

    def jugar(self, jugada):
        """Efectúa una movida.
            La jugada es una lista de pares (PILA, numero). (Ver mesa.)
            Si no puede realizarse la jugada se levanta una excepción SolitarioError *descriptiva*."""

        if len(jugada) == 1 and jugada[0][0] == PILA_TABLERO:
            for fundacion in self.mesa.fundaciones:
                try:
                    fundacion.apilar(self.mesa.pilas_tablero[jugada[0][1]].tope())
                    self.mesa.pilas_tablero[jugada[0][1]].desapilar()
                    return
                except SolitarioError:
                    pass
            #raise SolitarioError("No puede moverse esa carta a la fundación")

        elif len(jugada) == 1 and jugada[0][0] == MAZO and not self.mesa.mazo.es_vacia():
            self.mesa.descarte.apilar(self.mesa.mazo.desapilar(), forzar=True)
            self.mesa.descarte.tope().voltear()

        elif len(jugada) == 2:
            origen, en = jugada[0]
            destino, hasta = jugada[1]

            if origen == PILA_TABLERO and destino == FUNDACION: #AGREGAR TEMA MOVER:
                if self.mesa.pilas_tablero[en].es_vacia():
                    raise SolitarioError("La pila esta vacia, no hay elementos para mover")
                else:
                    self.mesa.fundaciones[hasta].apilar(self.mesa.pilas_tablero[en].tope())
                    self.mesa.pilas_tablero[en].desapilar()
            if origen == PILA_TABLERO and destino == PILA_TABLERO:
                if self.mesa.pilas_tablero[en].es_vacia():
                    raise SolitarioError("La pila esta vacia, no hay elementos para mover")

                else:
                    self.mesa.pilas_tablero[hasta].apilar(self.mesa.pilas_tablero[en].tope())
                    self.mesa.pilas_tablero[en].desapilar()
            if origen == FUNDACION and destino == PILA_TABLERO:
                if self.mesa.fundaciones[en].es_vacia():
                    raise SolitarioError("La pila esta vacia, no hay elementos para mover")
                else:
                    self.mesa.pilas_tablero[hasta].apilar(self.mesa.fundaciones[en].tope())
                    self.mesa.fundaciones[en].desapilar()
            if origen == DESCARTE and (destino == FUNDACION or destino == PILA_TABLERO):
                if self.mesa.descarte.es_vacia():
                    raise SolitarioError("La pila esta vacia, no hay elementos para mover")
                else:
                    if destino == FUNDACION:
                        self.mesa.fundaciones[hasta].apilar(self.mesa.descarte.tope())
                    else:
                        self.mesa.pilas_tablero[hasta].apilar(self.mesa.descarte.tope())
                    self.mesa.descarte.desapilar()
        elif len(jugada) > 2:
            origen, en = jugada[0]
            if origen == PILA_TABLERO:
                for i in range(1,len(jugada)-1):
                    if jugada[i] == jugada[0]:
                        self.mesa.pilas_tablero[en].criterio_mover += 1
                    else:
                        raise SolitarioError("Movimiento incorrecto")

class SolitarioSpider:
    """Interfaz para implementar un solitario."""

    def __init__(self, mesa):
        """Inicializa con una mesa creada y vacía."""
        self.mesa = mesa

    def armar(self):
        """Arma el tablero con la configuración inicial."""
        self.mesa.mazo = crear_mazo(mazos=2, palos=1)
        print(len(self.mesa.mazo.items))

        for i in range(8):
            self.mesa.fundaciones.append(PilaCartas(criterio_apilar=criterio(orden=CONSECUTIVA), valor_inicial=13))

        for i in range(10):
            self.mesa.pilas_tablero.append(PilaCartas(pila_visible=True, criterio_apilar=criterio(orden=ASCENDENTE)))
            for j in range(5):
                self.mesa.pilas_tablero[i].apilar(self.mesa.mazo.desapilar(), forzar=True)
            if i in (1, 4, 7, 10):
                self.mesa.pilas_tablero[i].apilar(self.mesa.mazo.desapilar(), forzar=True)
            self.mesa.pilas_tablero[i].tope().voltear()


    def termino(self):
        """Avisa si el juego se terminó."""
        total = 0
        for f in self.mesa.fundaciones:
            total += len(f.items)
        if total == 104:
            return True
        else:
            return False

    def jugar(self, jugada):
        """Efectúa una movida.
            La jugada es una lista de pares (PILA, numero). (Ver mesa.)
            Si no puede realizarse la jugada se levanta una excepción SolitarioError *descriptiva*."""

        if len(jugada) == 1 and jugada[0][0] == PILA_TABLERO:
            for fundacion in self.mesa.fundaciones:
                try:
                    fundacion.apilar(self.mesa.pilas_tablero[jugada[0][1]].tope())
                    self.mesa.pilas_tablero[jugada[0][1]].desapilar()
                    return
                except SolitarioError:
                    pass
            #raise SolitarioError("No puede moverse esa carta a la fundación")

        elif len(jugada) == 1 and jugada[0][0] == MAZO and not self.mesa.mazo.es_vacia():
            for i in range(10):
                self.mesa.pilas_tablero[i].apilar(self.mesa.mazo.desapilar(), forzar=True)
                self.mesa.pilas_tablero[i].tope().voltear()






