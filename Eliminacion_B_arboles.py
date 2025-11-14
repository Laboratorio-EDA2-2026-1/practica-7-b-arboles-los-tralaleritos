#Implementa aquí todos los procesos necesarios para la operación de eliminación. 
#Pueden modificar la extensión del documento para que se ajuste al lenguaje de su elección y comentar estas instrucciones.

#Implementacion del arbol binario:
class NodoArbolB:
    #Constructor
    def __init__(self, es_hoja=True):
        self.claves = []
        self.hijos = []
        self.es_hoja = es_hoja

    #---------------------- MÉTODOS AUXILIARES COMUNES ----------------------#
    def encontrar_indice(self, clave):

        i = 0
        while i < len(self.claves) and self.claves[i] < clave:
            i += 1
        return i

    #---------------------- DIVISIÓN E INSERCIÓN ----------------------#
    #Dividir el hijo lleno
    def dividir_hijo(self, indice, hijo, grado):

        grado_minimo = grado - 1
        nuevo_nodo = NodoArbolB(es_hoja=hijo.es_hoja)
        
        #Guardar la clave media antes de modificar las listas
        clave_media = hijo.claves[grado_minimo]
        
        #Mover la mitad de las claves al nuevo nodo
        nuevo_nodo.claves = hijo.claves[grado_minimo + 1:]
        hijo.claves = hijo.claves[:grado_minimo]
        
        #Si no es hoja, mover también los hijos
        if not hijo.es_hoja:
            nuevo_nodo.hijos = hijo.hijos[grado_minimo + 1:]
            hijo.hijos = hijo.hijos[:grado_minimo + 1]
        
        #Insertar la clave media en este nodo
        self.claves.insert(indice, clave_media)
        self.hijos.insert(indice + 1, nuevo_nodo)
    
    #Insertando clave en un nodo no lleno
    def insertar_no_lleno(self, clave, grado):
        indice = len(self.claves) - 1
        
        if self.es_hoja:
            # Insertar la clave en orden
            self.claves.append(None)
            while indice >= 0 and clave < self.claves[indice]:
                self.claves[indice + 1] = self.claves[indice]
                indice -= 1
            self.claves[indice + 1] = clave
        else:
            # Encontrar el hijo al que se insertará la clave
            while indice >= 0 and clave < self.claves[indice]:
                indice -= 1
            indice += 1
            
            # Verificación de si el hijo está lleno
            if len(self.hijos[indice].claves) == 2 * grado - 1:
                self.dividir_hijo(indice, self.hijos[indice], grado)
                if clave > self.claves[indice]:
                    indice += 1
            
            self.hijos[indice].insertar_no_lleno(clave, grado)

    #---------------------- ELIMINACIÓN ----------------------#
    def eliminar(self, clave, grado):

        idx = self.encontrar_indice(clave)

        # 1) La clave está en este nodo
        if idx < len(self.claves) and self.claves[idx] == clave:
            if self.es_hoja:
                # Caso 1: es hoja, solo la quitamos
                self.eliminar_de_hoja(idx)
            else:
                # Caso 2: está en un nodo interno
                self.eliminar_de_no_hoja(idx, grado)
        else:
            # 2) La clave NO está en este nodo
            if self.es_hoja:
                # La clave no existe en el árbol
                return

            # Indicador para saber si la clave está en el último hijo
            bandera_ultimo_hijo = (idx == len(self.claves))

            # Si el hijo donde debe estar la clave tiene menos de t-1 claves,
            # lo "rellenamos" para garantizar que tenga al menos t-1
            if len(self.hijos[idx].claves) < grado:
                self.rellenar(idx, grado)

            # Después de rellenar, puede haber cambiado la estructura
            if bandera_ultimo_hijo and idx > len(self.claves):
                self.hijos[idx - 1].eliminar(clave, grado)
            else:
                self.hijos[idx].eliminar(clave, grado)

    def eliminar_de_hoja(self, idx):

        self.claves.pop(idx)

    def eliminar_de_no_hoja(self, idx, grado):

        clave = self.claves[idx]

        # Hijo anterior (izquierdo)
        if len(self.hijos[idx].claves) >= grado:
            pred = self.obtener_predecesor(idx)
            self.claves[idx] = pred
            self.hijos[idx].eliminar(pred, grado)

        # Hijo siguiente (derecho)
        elif len(self.hijos[idx + 1].claves) >= grado:
            succ = self.obtener_sucesor(idx)
            self.claves[idx] = succ
            self.hijos[idx + 1].eliminar(succ, grado)

        # Ambos hijos tienen t-1 claves -> fusionar
        else:
            self.unir(idx)
            self.hijos[idx].eliminar(clave, grado)

    def obtener_predecesor(self, idx):

        actual = self.hijos[idx]
        while not actual.es_hoja:
            actual = actual.hijos[-1]
        return actual.claves[-1]

    def obtener_sucesor(self, idx):

        actual = self.hijos[idx + 1]
        while not actual.es_hoja:
            actual = actual.hijos[0]
        return actual.claves[0]

    def rellenar(self, idx, grado):

        if idx != 0 and len(self.hijos[idx - 1].claves) >= grado:
            self.pedir_prestado_anterior(idx)
        elif idx != len(self.hijos) - 1 and len(self.hijos[idx + 1].claves) >= grado:
            self.pedir_prestado_siguiente(idx)
        else:
            # Si no se puede pedir prestado, se fusiona con un hermano
            if idx != len(self.hijos) - 1:
                self.unir(idx)
            else:
                self.unir(idx - 1)

    def pedir_prestado_anterior(self, idx):

        hijo = self.hijos[idx]
        hermano = self.hijos[idx - 1]

        # La clave del padre baja al hijo
        hijo.claves.insert(0, self.claves[idx - 1])

        # Último hijo del hermano pasa a ser primer hijo del actual
        if not hijo.es_hoja:
            hijo.hijos.insert(0, hermano.hijos.pop())

        # Última clave del hermano sube al padre
        self.claves[idx - 1] = hermano.claves.pop()

    def pedir_prestado_siguiente(self, idx):

        hijo = self.hijos[idx]
        hermano = self.hijos[idx + 1]

        # La clave del padre baja al hijo
        hijo.claves.append(self.claves[idx])

        # Primer hijo del hermano pasa a ser último hijo del actual
        if not hijo.es_hoja:
            hijo.hijos.append(hermano.hijos.pop(0))

        # Primera clave del hermano sube al padre
        self.claves[idx] = hermano.claves.pop(0)

    def unir(self, idx):

        hijo = self.hijos[idx]
        hermano = self.hijos[idx + 1]

        # Bajar la clave del padre
        hijo.claves.append(self.claves[idx])

        # Agregar claves e hijos del hermano
        hijo.claves.extend(hermano.claves)
        if not hijo.es_hoja:
            hijo.hijos.extend(hermano.hijos)

        # Eliminar clave y hijo derecho del padre
        self.claves.pop(idx)
        self.hijos.pop(idx + 1)

#---------------------- CLASE ÁRBOL-B ----------------------#
class ArbolB:
    #Constructor del arbol-B
    def __init__(self, grado=3):
        self.raiz = NodoArbolB(es_hoja=True)
        self.grado = grado
    
    #Metodo insertar una clave
    def insertar(self, clave):
        raiz = self.raiz
        
        #Si la raíz está llena, se va dividir
        if len(raiz.claves) == 2 * self.grado - 1:
            nueva_raiz = NodoArbolB(es_hoja=False)
            nueva_raiz.hijos.append(self.raiz)
            nueva_raiz.dividir_hijo(0, self.raiz, self.grado)
            
            #Decidir entre los dos hijos
            indice = 0
            if nueva_raiz.claves[0] < clave:
                indice += 1
            nueva_raiz.hijos[indice].insertar_no_lleno(clave, self.grado)
            
            self.raiz = nueva_raiz
        else:
            raiz.insertar_no_lleno(clave, self.grado)

    #--------------- ELIMINAR EN EL ÁRBOL COMPLETO ---------------#
    def eliminar(self, clave):
    
        if not self.raiz:
            return

        self.raiz.eliminar(clave, self.grado)

        # Si la raíz se queda sin claves, hay que reajustarla
        if len(self.raiz.claves) == 0:
            if self.raiz.es_hoja:
                # Árbol vacío
                self.raiz = NodoArbolB(es_hoja=True)
            else:
                # El nuevo root es su único hijo
                self.raiz = self.raiz.hijos[0]

    #Impresion del arbol-B de manera visual
    def imprimir(self):
        print("\nARBOL-B:")
        print(f"Grado: {self.grado}")
        print("-" * 50)
        self._imprimir_nodo(self.raiz, nivel=0)
        print("-" * 50)
    
    #Impresion de un nodo y sus hijos de manera recursiva
    def _imprimir_nodo(self, nodo, nivel=0):
        indentacion = "  " * nivel
        tipo_nodo = "hoja" if nodo.es_hoja else "interno"
        
        print(f"{indentacion}Nivel {nivel} [{tipo_nodo}]: {nodo.claves}")
        
        if not nodo.es_hoja:
            for hijo in nodo.hijos:
                self._imprimir_nodo(hijo, nivel + 1)
    
    #Impresion inorden ASCENDENTE, MENOR A MAYOR
    def imprimir_recorrido_inorden(self):
        print("\nRecorrido en orden:", end=" ")
        self._recorrido_inorden(self.raiz)
        print()
    
    #Funcion recursiva para imprimir en inorden
    def _recorrido_inorden(self, nodo):
        """Recorrido inorden recursivo"""
        if nodo:
            numero_claves = len(nodo.claves)
            for i in range(numero_claves):
                if not nodo.es_hoja:
                    self._recorrido_inorden(nodo.hijos[i])
                print(nodo.claves[i], end=" ")
            
            if not nodo.es_hoja:
                self._recorrido_inorden(nodo.hijos[numero_claves])

#---------------------- PRUEBA ----------------------#
def main():
    #Crear un Árbol B de grado 3
    arbol = ArbolB(grado=3)
    
    #Valores a insertar en arbol grado 3
    valores = [10, 20, 5, 6, 12, 30, 7, 17, 3, 8, 15, 25, 40, 45, 50]
    
    print("Insertando valores:", valores)
    for valor in valores:
        arbol.insertar(valor)
    
    #Imprimir el árbol
    arbol.imprimir()
    arbol.imprimir_recorrido_inorden()

    # Ahora probamos la ELIMINACIÓN
    a_eliminar = [6, 15, 30, 10]
    print("\nEliminando claves:", a_eliminar)
    for x in a_eliminar:
        print(f"\n>>> Eliminando {x}")
        arbol.eliminar(x)
        arbol.imprimir()
        arbol.imprimir_recorrido_inorden()
    
#Llamando a funcion main:
main()

