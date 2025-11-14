#Nodo de Arbol-B clase:
class NodoArbolB:
    #Constructor
    def __init__(self, es_hoja=True):
        self.claves = []
        self.hijos = []
        self.es_hoja = es_hoja
    
    #Dividor el hijo lleno
    def dividir_hijo(self, indice, hijo):
        """Divide un hijo lleno del nodo"""
        grado_minimo = len(hijo.claves) // 2
        nuevo_nodo = NodoArbolB(es_hoja=hijo.es_hoja)
        
        #Guardar la clave media antes de modificar las listas
        #de no hacerse asi, habra un error
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
            # ncontrar el hijo al que se insertara la clave
            while indice >= 0 and clave < self.claves[indice]:
                indice -= 1
            indice += 1
            
            #verificacion de si el hijo esta lleno
            if len(self.hijos[indice].claves) == 2 * grado - 1:
                self.dividir_hijo(indice, self.hijos[indice])
                if clave > self.claves[indice]:
                    indice += 1
            
            self.hijos[indice].insertar_no_lleno(clave, grado)
    
    # OPERACIÓN DE BÚSQUEDA
    def buscar(self, clave):
        """
        Busca una clave en el nodo actual y sus hijos.
        Retorna (nodo, indice) si encuentra la clave, None si no la encuentra.
        """
        # Buscar en las claves del nodo actual
        indice = 0
        while indice < len(self.claves) and clave > self.claves[indice]:
            indice += 1
        
        # Verificar si encontramos la clave en este nodo
        if indice < len(self.claves) and clave == self.claves[indice]:
            return (self, indice)
        
        # Si es hoja y no encontramos la clave, no existe en el árbol
        if self.es_hoja:
            return None
        
        # Si no es hoja, buscar recursivamente en el hijo apropiado
        return self.hijos[indice].buscar(clave)


class ArbolB:
    def __init__(self, grado=3):
        self.raiz = NodoArbolB(es_hoja=True)
        self.grado = grado
    
    def insertar(self, clave):
        raiz = self.raiz
        
        if len(raiz.claves) == 2 * self.grado - 1:
            nueva_raiz = NodoArbolB(es_hoja=False)
            nueva_raiz.hijos.append(self.raiz)
            nueva_raiz.dividir_hijo(0, self.raiz)
            
            indice = 0
            if nueva_raiz.claves[0] < clave:
                indice += 1
            nueva_raiz.hijos[indice].insertar_no_lleno(clave, self.grado)
            
            self.raiz = nueva_raiz
        else:
            raiz.insertar_no_lleno(clave, self.grado)
    
    # OPERACIÓN DE BÚSQUEDA
    def buscar(self, clave):
        """
        Busca una clave en el árbol B.
        """
        print(f"\nBuscando clave: {clave}")
        resultado = self._buscar_con_ruta(self.raiz, clave, nivel=0)
        
        if resultado:
            print(f"  Clave {clave} ENCONTRADA")
            return True
        else:
            print(f"  Clave {clave} NO ENCONTRADA")
            return False
    
    def _buscar_con_ruta(self, nodo, clave, nivel=0):
        """
        Búsqueda con ruta recorrida.
        """
        indentacion = "  " * nivel
        print(f"{indentacion}Nivel {nivel}: Buscando en {nodo.claves}")
        
        # Buscar en las claves del nodo actual
        indice = 0
        while indice < len(nodo.claves) and clave > nodo.claves[indice]:
            indice += 1
        
        # Verificar si encontramos la clave
        if indice < len(nodo.claves) and clave == nodo.claves[indice]:
            print(f"{indentacion}→ ¡Encontrada en índice {indice}!")
            return True
        
        # Si es hoja y no la encontramos
        if nodo.es_hoja:
            print(f"{indentacion}→ Es hoja, clave no existe")
            return False
        
        # Buscar en el hijo apropiado
        print(f"{indentacion}→ Bajando al hijo {indice}")
        return self._buscar_con_ruta(nodo.hijos[indice], clave, nivel + 1)
    
    def buscar_simple(self, clave):
        """
        Búsqueda simple sin imprimir la ruta.
        """
        resultado = self.raiz.buscar(clave)
        return resultado is not None
    
    def imprimir(self):
        print("\nÁRBOL-B:")
        print(f"Grado: {self.grado}")
        print("-" * 50)
        self._imprimir_nodo(self.raiz, nivel=0)
        print("-" * 50)
    
    def _imprimir_nodo(self, nodo, nivel=0):
        indentacion = "  " * nivel
        tipo_nodo = "hoja" if nodo.es_hoja else "interno"
        print(f"{indentacion}Nivel {nivel} [{tipo_nodo}]: {nodo.claves}")
        
        if not nodo.es_hoja:
            for hijo in nodo.hijos:
                self._imprimir_nodo(hijo, nivel + 1)
    
    def imprimir_recorrido_inorden(self):
        print("\nRecorrido en orden:", end=" ")
        self._recorrido_inorden(self.raiz)
        print()
    
    def _recorrido_inorden(self, nodo):
        if nodo:
            numero_claves = len(nodo.claves)
            for i in range(numero_claves):
                if not nodo.es_hoja:
                    self._recorrido_inorden(nodo.hijos[i])
                print(nodo.claves[i], end=" ")
            
            if not nodo.es_hoja:
                self._recorrido_inorden(nodo.hijos[numero_claves])


def main():

    arbol = ArbolB(grado=3)
    
    #Valores a insertar en arbol grado 3
    valores = [10, 20, 5, 6, 12, 30, 7, 17, 3, 8, 15, 25, 40, 45, 50]
    
    print("Insertando valores:", valores)
    for valor in valores:
        arbol.insertar(valor)
    
    #Imprimir el árbol
    arbol.imprimir()
    
    #Imprimir recorrido inorden
    arbol.imprimir_recorrido_inorden()
 
    print("\n\nPRUEBAS DE BÚSQUEDA")
    
    # Búsquedas de valores que EXISTEN
    print("\nBúsquedas de valores existentes")
    valores_buscar = [10, 25, 50]
    for valor in valores_buscar:
        arbol.buscar(valor)
    
    # Búsquedas de valores que NO EXISTEN
    print("\nBúsquedas de valores NO existentes")
    valores_no_existentes = [13, 35, 100]
    for valor in valores_no_existentes:
        arbol.buscar(valor)
    
    # Ejemplo usando buscar_simple (sin mostrar ruta)
    print("\nBúsqueda sin mostrar ruta")
    print(f"¿Existe 20? {arbol.buscar_simple(20)}")
    print(f"¿Existe 99? {arbol.buscar_simple(99)}")


if __name__ == "__main__":
    main()
