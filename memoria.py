

class NodoMemoria:
    """
    Nodo de la lista enlazada de memoria.
    Representa un bloque de memoria libre.
    """
    def __init__(self, direccion, tamanio):
        self.direccion  = direccion   # dónde empieza el bloque
        self.tamanio    = tamanio     # cuántos bytes tiene
        self.siguiente  = None        # puntero al siguiente bloque libre


class SimuladorMemoria:
    """
    Simula la gestión de memoria de un sistema operativo.
    Mantiene una lista enlazada de bloques libres ordenada
    por dirección de memoria.

    Operaciones:
        solicitar_memoria()  →  asigna un bloque a un programa
        liberar_memoria()    →  devuelve un bloque a la lista libre
        _fusionar()          →  combina bloques contiguos
    """

    TAMANIO_TOTAL = 1024   # memoria total simulada en bytes

    def __init__(self):
        # Al inicio toda la memoria está libre — un solo bloque
        self.cabeza     = NodoMemoria(0, self.TAMANIO_TOTAL)
        self.asignados  = []   # lista de bloques ocupados (dir, tamaño, nombre)

    # ── Solicitar memoria ─────────────────────────────────────
    def solicitar_memoria(self, tamanio, nombre="Programa", estrategia="primer"):
        """
        Busca un bloque libre suficientemente grande.
        Estrategias:
            'primer' → primer ajuste (el primero que sirva)
            'mejor'  → mejor ajuste (el que deje menos desperdicio)
        Retorna (direccion, tamaño) si hay espacio, None si no.
        """
        if estrategia == "primer":
            return self._primer_ajuste(tamanio, nombre)
        else:
            return self._mejor_ajuste(tamanio, nombre)

    def _primer_ajuste(self, tamanio, nombre):
        """Toma el primer bloque libre que sea suficientemente grande."""
        actual = self.cabeza
        previo = None
        while actual:
            if actual.tamanio >= tamanio:
                return self._asignar(actual, previo, tamanio, nombre)
            previo = actual
            actual = actual.siguiente
        return None   # no hay espacio

    def _mejor_ajuste(self, tamanio, nombre):
        """Busca el bloque libre que deje el menor desperdicio."""
        mejor   = None
        previo_mejor = None
        actual  = self.cabeza
        previo  = None
        while actual:
            if actual.tamanio >= tamanio:
                if mejor is None or actual.tamanio < mejor.tamanio:
                    mejor        = actual
                    previo_mejor = previo
            previo = actual
            actual = actual.siguiente
        if mejor:
            return self._asignar(mejor, previo_mejor, tamanio, nombre)
        return None

    def _asignar(self, nodo, previo, tamanio, nombre):
        """
        Extrae el bloque del nodo libre y lo marca como ocupado.
        Si sobra espacio, deja un bloque libre con el resto.
        """
        direccion = nodo.direccion
        resto     = nodo.tamanio - tamanio

        if resto > 0:
            # Quedan bytes libres — actualiza el nodo existente
            nodo.direccion += tamanio
            nodo.tamanio    = resto
        else:
            # Bloque exacto — elimina el nodo de la lista libre
            if previo:
                previo.siguiente = nodo.siguiente
            else:
                self.cabeza = nodo.siguiente

        self.asignados.append({
            "direccion": direccion,
            "tamanio"  : tamanio,
            "nombre"   : nombre
        })
        return direccion, tamanio

    # ── Liberar memoria ───────────────────────────────────────
    def liberar_memoria(self, direccion):
        """
        Devuelve un bloque ocupado a la lista libre.
        Luego intenta fusionar bloques contiguos para evitar
        fragmentación.
        Retorna True si liberó correctamente, False si no encontró.
        """
        # Buscar en asignados
        bloque = None
        for b in self.asignados:
            if b["direccion"] == direccion:
                bloque = b
                break
        if not bloque:
            return False

        self.asignados.remove(bloque)
        self._insertar_libre(bloque["direccion"], bloque["tamanio"])
        self._fusionar()
        return True

    def _insertar_libre(self, direccion, tamanio):
        """Inserta un bloque libre en orden por dirección."""
        nuevo = NodoMemoria(direccion, tamanio)
        if not self.cabeza or direccion < self.cabeza.direccion:
            nuevo.siguiente = self.cabeza
            self.cabeza     = nuevo
            return
        actual = self.cabeza
        while actual.siguiente and actual.siguiente.direccion < direccion:
            actual = actual.siguiente
        nuevo.siguiente  = actual.siguiente
        actual.siguiente = nuevo

    def _fusionar(self):
        """
        Recorre la lista libre y fusiona bloques contiguos.
        Dos bloques son contiguos si:
            bloque1.direccion + bloque1.tamaño == bloque2.direccion
        """
        actual = self.cabeza
        while actual and actual.siguiente:
            if actual.direccion + actual.tamanio == actual.siguiente.direccion:
                # Son contiguos — fusionar
                actual.tamanio  += actual.siguiente.tamanio
                actual.siguiente = actual.siguiente.siguiente
            else:
                actual = actual.siguiente

    # ── Información del estado ────────────────────────────────
    def bloques_libres(self):
        """Retorna lista de bloques libres como (direccion, tamaño)."""
        resultado = []
        actual = self.cabeza
        while actual:
            resultado.append((actual.direccion, actual.tamanio))
            actual = actual.siguiente
        return resultado

    def memoria_libre_total(self):
        return sum(t for _, t in self.bloques_libres())

    def memoria_ocupada_total(self):
        return sum(b["tamanio"] for b in self.asignados)

    def fragmentacion(self):
        """
        Porcentaje de fragmentación.
        Alta fragmentación = mucha memoria libre pero en bloques pequeños.
        """
        libres = self.bloques_libres()
        if not libres:
            return 0
        libre_total = self.memoria_libre_total()
        if libre_total == 0:
            return 0
        bloque_max = max(t for _, t in libres)
        return round((1 - bloque_max / libre_total) * 100, 1)

    def nodos_polinomio(self, polinomio):
        """
        Simula la memoria que ocuparía un polinomio.
        Cada NodoTermino ocupa aproximadamente 56 bytes en Python.
        Retorna lista de (direccion_simulada, tamaño, término).
        """
        BYTES_POR_NODO = 56
        resultado = []
        actual    = polinomio.cabeza if polinomio else None
        direccion = 2000   # dirección base simulada para el polinomio
        while actual:
            termino = f"{actual.coeficiente}x^{actual.exponente}"
            resultado.append((direccion, BYTES_POR_NODO, termino))
            direccion += BYTES_POR_NODO + 8   # 8 bytes de overhead
            actual     = actual.siguiente
        return resultado

    def reset(self):
        """Reinicia la memoria al estado inicial."""
        self.cabeza    = NodoMemoria(0, self.TAMANIO_TOTAL)
        self.asignados = []