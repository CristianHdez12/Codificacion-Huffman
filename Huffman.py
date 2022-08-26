import math
from tkinter import *
from tkinter.scrolledtext import ScrolledText
from tkinter.ttk import *
from tkinter.filedialog import askopenfile
from tabulate import tabulate

class Nodo(object):

    def __init__(self, nombre=None, cantidad=None):
        self.nombre = nombre
        self.cantidad = cantidad
        self.hijoIzquierdo = None
        self.hijoDerecho = None
        self.codigo = None

class Programa:
    
    buffer = list(range(20))
    nodos = []

    def __init__(self) -> None:
        self.root = Tk()
        self.root.title("Programa de análisis de texto")        
        self.miFrame=Frame(self.root, width=1000, height=650)
        self.miFrame.pack()

        self.lblTexto=Label(self.miFrame, text="Texto a analizar: ", font=18)
        self.lblTexto.grid(row=1, column=0, padx=5, pady=5)
        self.txtContenido = ScrolledText(self.miFrame,width=80, height=15, wrap=WORD)
        self.txtContenido.grid(row=2, column=0, columnspan=5, padx=10, pady=10)

        self.lblTabla=Label(self.miFrame, text="Texto analizado: ", font=18)
        self.lblTabla.grid(row=3, column=0, padx=5, pady=5)
        self.txtTabla = ScrolledText(self.miFrame,width=80, height=15)
        self.txtTabla.grid(row=4, column=0,columnspan=5, padx=10, pady=10)

        self.lblResultado = Label(self.miFrame, text = "Resultados", font=18)
        self.lblResultado.grid(row=1, column=5, padx = 5, pady = 5)
        self.txtResultado = ScrolledText(self.miFrame,width=40, height=15)
        self.txtResultado.grid(row=2, column=5,columnspan=5, padx=10, pady=10)
 
        #----------------Botón Seleccionar archivo
        botonArchivo=Button(self.miFrame, text="Seleccionar archivo", command=self.seleccionarArchivo)
        botonArchivo.grid(row=0, column=1, padx=10, pady=10)
        #----------------Botón Analizar------------------------
        botonAnalizar=Button(self.miFrame, text="Analizar", command=self.huffman)
        botonAnalizar.grid(row=0, column=2, padx=10, pady=10)
        #---------------Botón Limpiar texto
        botonLimpiar=Button(self.miFrame, text="Limpiar", command=self.limpiar)
        botonLimpiar.grid(row=0, column=3, padx=10, pady=10)

        self.root.mainloop()

    #---------------------Función para obtener los caracteres del texto-----------------
    def obtenerCaracteres(self):
        texto = self.txtContenido.get("1.0", "end-1c")
        caracteres = []
        cantidad = []
        existe = False

        for i in texto:
            if caracteres:
                for j in caracteres:
                    if(i == j):
                        existe = True
                        break
                    else:
                        existe = False
                if existe == False:
                    caracteres.append(i)
            else:
                caracteres.append(i)

        for i in caracteres:
            c = texto.count(i)
            cantidad.append(c)
            
        return caracteres, cantidad
    
    #------------Función para crear el arbol de nodos---------------------
    def huffman(self):
        caracteres, cantidad = self.obtenerCaracteres()
        arregloNodos = []

        if len(caracteres) != 0:
            #Crear un nodo por cada caracter único
            for i in range(len(caracteres)):
                nodo = Nodo(caracteres[i], cantidad[i])
                arregloNodos.append(nodo)
            

            #Asignar los hijos a cada nodo
            while len(arregloNodos) > 1:
                arregloNodos.sort(key=lambda nodo:nodo.cantidad, reverse=True) #Ordenar el arreglo de mayor a menor tomando la cantidad como referencia
                n = Nodo(cantidad=(arregloNodos[-1].cantidad + arregloNodos[-2].cantidad)) 
                n.hijoIzquierdo = arregloNodos.pop(-1) #Asignar el último elemento del arreglo como hijo izquierdo y eliminarlo
                n.hijoDerecho = arregloNodos.pop(-1)
                arregloNodos.append(n)
            
            inicio = arregloNodos[0]
            self.recorrido(inicio, 0)
            self.mostrarDatos()
    
    #------------Función para recorrer el arbol de nodos y asignar el código---------------------
    def recorrido(self, tree, length):

        node = tree
        if (not node):
            return
        elif node.nombre:
            code = ""
            for i in range(length): 
               code += str(self.buffer[i])
            nodo = Nodo(nombre=node.nombre, cantidad=node.cantidad)
            nodo.codigo = code
            self.nodos.append(nodo)
            return
        
        self.buffer[length] = 0
        self.recorrido(node.hijoIzquierdo, length + 1)
        self.buffer[length] = 1
        self.recorrido(node.hijoDerecho, length + 1)

    #-----------------------------Función para mostrar los datos en forma de tabla--------------
    def mostrarDatos(self):
        caracteres, cantidad = self.obtenerCaracteres()
        self.txtTabla.delete("1.0", "end")
        tablaDatos = [ [0 for columna in range(3)] for fila in range (len(caracteres))]
        codigo = 0

        for i in range(len(caracteres)):
            
            tablaDatos[i][0] = self.nodos[i].nombre
            tablaDatos[i][1] = str(self.nodos[i].cantidad) + "/" + str(sum(cantidad))
            c = len(self.nodos[i].codigo) * self.nodos[i].cantidad
            codigo += c     
            tablaDatos[i][2] = self.nodos[i].codigo

        self.txtTabla.insert("1.0", tabulate(tablaDatos, headers=["Simbolo","Probabilidad", "Código"], tablefmt="pretty"))
        self.calcularResultados(sum(cantidad), codigo)


    #------------------------Función para calcular el porcentaje de compactación-------------------
    def calcularResultados(self, cantidad, codigo):
        self.txtResultado.insert("1.0", "Cantidad de carateres: " + str(cantidad))
        inicioBits = cantidad*8     
        self.txtResultado.insert("end", "\n\nBits al iniciar: " + str(inicioBits) + " bits")
        finalBits = codigo
        self.txtResultado.insert("end", "\n\nBits al compactar: " + str(finalBits) + " bits")
        resultado = round(100-((finalBits*100)/inicioBits),2)
        self.txtResultado.insert("end", "\n\nPorcentaje de compactación: " + str(resultado) + " %")
        

    #-------------Función para abrir un archivo-------------------
    def seleccionarArchivo(self):
        archivo = askopenfile(mode='r', filetypes=[('Archivo de texto', '*.txt')])
        
        if archivo is not None:
            contenido = archivo.read()
            self.txtContenido.insert("1.0", contenido)

    #-------------Función para limpiar los datos------------------
    def limpiar(self):
        self.txtContenido.delete("1.0","end")
        self.txtTabla.delete("1.0", "end")
        self.txtResultado.delete("1.0", "end")
        self.buffer.clear()
        self.buffer = list(range(20))
        self.nodos.clear()

programa = Programa()
