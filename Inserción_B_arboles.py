#Implementa aquí todos los procesos necesarios para la operación de insercion. 
#Pueden modificar la extensión del documento para que se ajuste al lenguaje de su elección y comentar estas instrucciones.

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


#Arbol-B clase:
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
            nueva_raiz.dividir_hijo(0, self.raiz)
            
            #Decidir entre los dos hijos
            indice = 0
            if nueva_raiz.claves[0] < clave:
                indice += 1
            nueva_raiz.hijos[indice].insertar_no_lleno(clave, self.grado)
            
            self.raiz = nueva_raiz
        else:
            raiz.insertar_no_lleno(clave, self.grado)
    
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

#CREANDO UN ARBOL E INSERTANDO DATOS

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
    
    #Imprimir recorrido inorden
    arbol.imprimir_recorrido_inorden()
    
#Llamando a funcion main:
main()
