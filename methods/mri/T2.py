import math
from tkinter import messagebox
import pydicom as dicom
import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
from tkinter import filedialog
import os
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import Canvas

# Herramienta para abrir imagen y guardar su directorio
def openImg():
    global file_path, directorio

    file_path = filedialog.askopenfilename()
    # Obtiene el directorio del archivo.
    directorio = os.path.dirname(file_path)
    file_name = os.path.basename(file_path)

    if(file_path):
        pathText.config(text="Archivo: " + file_name)
    else:
        pathText.config(text="¡Seleccione un archivo válido!")

def verificarDatos(longitud):
    global T2cuadradoButton 

    abrirImagen.pack_forget()
    logitudText.pack_forget()
    longitudEntry.pack_forget()

    T2cuadradoButton = tk.Button(ventanaMetodos, text="Calcular T2/nROI cuadrado", command=lambda: ajusteROI(longitud))
    T2cuadradoButton.pack()

def ajusteROI(longitud):
# Limpiamos y reajustamos la interfaz.
    T2cuadradoButton.pack_forget()
    ventanaMetodos.geometry("300x500")

    # Entradas para el centro y radio del ROI
    centro_x_label = tk.Label(ventanaMetodos, text="Centro X del ROI:")
    centro_x_label.pack()
    centro_x_entry = tk.Entry(ventanaMetodos)
    centro_x_entry.pack()

    centro_y_label = tk.Label(ventanaMetodos, text="Centro Y del ROI:")
    centro_y_label.pack()
    centro_y_entry = tk.Entry(ventanaMetodos)
    centro_y_entry.pack()

    radio_label = tk.Label(ventanaMetodos, text="Radio del ROI:")
    radio_label.pack()
    radio_entry = tk.Entry(ventanaMetodos)
    radio_entry.pack()

    # Botón para confirmar ROI:
    addDatos = tk.Button(ventanaMetodos, text="Confirmar", command=lambda: calcT2SquareROI(longitud, int(centro_x_entry.get()),
                                                                                            int(centro_y_entry.get()), int(radio_entry.get())))
    addDatos.pack()

# Cálculo de T2 para una ROI cuadrada de radio y centro variables
def calcT2SquareROI(no_tomas, X, Y, radio):
    listaTE = [];
    listaValoresT2 = [];
    offsetT2 = 0.1;

    # Matriz para almacenar las sumas de intensidades en el ROI a lo largo de 100 imágenes
    sumas_intensidades = np.zeros(no_tomas, dtype=np.float64)    

    for i in range(1, no_tomas + 1):
        imageFileName = f"/MRIm{i:03d}.dcm"
        img = dicom.dcmread(directorio + imageFileName)
        imagenReescalada = img.RescaleSlope * img.pixel_array  # Imagen con factor de reescalado

        #  Obtenemos el valor más alto para el cálculo de T2
        max_valor = imagenReescalada.max()
        if (max_valor > offsetT2):
            offsetT2 = max_valor;
        
        # Extraer la ROI
        x_start = max(0, X - radio)
        x_end = min(imagenReescalada.shape[1], X + radio)
        y_start = max(0, Y - radio)
        y_end = min(imagenReescalada.shape[0], Y + radio)

        roi = imagenReescalada[y_start:y_end, x_start:x_end]

        # Calcular la suma de intensidades en la ROI y almacenarla en el array sumas_intensidades
        sumas_intensidades[i - 1] = np.mean(roi)

        # Guardamos los tiempos de Eco para calcular T2.
        listaTE.append(img.EchoTime)

    for te, St in zip(listaTE, sumas_intensidades):
        T2 = -te / math.log(St / offsetT2)
        listaValoresT2.append(T2);
    valorMedioT2 = round(np.mean(listaValoresT2), 3)
    
    plt.plot(sumas_intensidades)
    plt.title('Valores ROI cuadrado. \n Radio: '+str(radio)+', Centro del ROI: '
              +str(X)+','+str(Y)+'\nT2 calculado: '+str(valorMedioT2)+'ms', fontsize=10);
    plt.xlabel('Imagen')
    plt.ylabel('Intensidad Media')
    plt.show()

# Ventana para métodos
ventanaMetodos = tk.Tk()
ventanaMetodos.title("Análisis T2")
ventanaMetodos.geometry("250x150")

file_path = ''  

abrirImagen = tk.Button(ventanaMetodos, text="Cargar Primera imagen", command=openImg)
abrirImagen.pack()

# Etiqueta para mostrar la ruta del archivo
pathText = tk.Label(ventanaMetodos, text="")
pathText.pack()

logitudText = tk.Label(ventanaMetodos, text="Longitud de la serie de T2:")
logitudText.pack()
longitudEntry = tk.Entry(ventanaMetodos)
longitudEntry.pack()

addDatos = tk.Button(ventanaMetodos, text="Añadir", command=lambda: verificarDatos(int(longitudEntry.get())))
addDatos.pack()

# Iniciar la ventana
ventanaMetodos.mainloop()
