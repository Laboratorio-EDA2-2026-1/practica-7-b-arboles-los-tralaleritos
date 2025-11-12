#Implementa aquí todos los procesos necesarios para la operación de inserción. 
#Pueden modificar la extensión del documento para que se ajuste al lenguaje de su elección y comentar estas instrucciones.

#Implementacion del arbol binario:

#Nodos, que van a ser parte del arbol binario, hojas:
class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.izquierda = None  # Puntero al subárbol izquierdo
        self.derecha = None   # Puntero al subárbol derecho

    def __str__(self):
        return f"Nodo({self.valor})"
        
#Arbol Binario:
class ArbolBinario:
    #Impresion del Arbol Binario
    def recorrido_inorden(self):
        valores = []
        def inorden_recursivo(nodo):
            if nodo:
                inorden_recursivo(nodo.izquierda)
                
                valores.append(nodo.valor)
                
                inorden_recursivo(nodo.derecha)
        
        inorden_recursivo(self.raiz)
        print("Recorrido Inorden, de manera ascendente:", valores)
    
    def __init__(self):
        self.raiz = None
    
    #Funcion para insertar valroes
    def insertar(self, valor):
        nuevo_nodo = Nodo(valor)

        if self.raiz is None:
            self.raiz = nuevo_nodo
            return

        def insertar_recursivo(nodo_actual, nuevo_nodo):
            if nuevo_nodo.valor < nodo_actual.valor:
                if nodo_actual.izquierda is None:
                    nodo_actual.izquierda = nuevo_nodo
                else:
                    insertar_recursivo(nodo_actual.izquierda, nuevo_nodo)
            elif nuevo_nodo.valor > nodo_actual.valor:
                if nodo_actual.derecha is None:
                    nodo_actual.derecha = nuevo_nodo
                else:
                    insertar_recursivo(nodo_actual.derecha, nuevo_nodo)

        insertar_recursivo(self.raiz, nuevo_nodo)
        
#Creando un arbol binario:
arbol_ejemplo = ArbolBinario()

#Insertamos 10 valores al arbol binario:
arbol_ejemplo.insertar(1)
arbol_ejemplo.insertar(2)
arbol_ejemplo.insertar(3)
arbol_ejemplo.insertar(4)
arbol_ejemplo.insertar(7)
arbol_ejemplo.insertar(8)
arbol_ejemplo.insertar(9)
arbol_ejemplo.insertar(10)

#Imprimiendo el arbol binario obtenido
arbol_ejemplo.recorrido_inorden()

#Donde hasta aqui la impresion es: ""Recorrido Inorden, de manera ascendente: [1, 2, 3, 4, 7, 8, 9, 10]"

#Agregando otra hoja al arbol:
arbol_ejemplo.insertar(5)
arbol_ejemplo.insertar(11) #por tanto se deberia insertar 5 despues de 4, y 11 despues de 10

#Imprimiendo el arbol binario actualizado
arbol_ejemplo.recorrido_inorden()

#Imprimiendose de manera correcta: ""Recorrido Inorden, de manera ascendente: [1, 2, 3, 4, 5, 7, 8, 9, 10, 11]""
