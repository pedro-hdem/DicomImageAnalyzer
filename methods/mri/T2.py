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
import matplotlib.patches as patches

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

    addDatos.pack_forget()
    logitudText.pack_forget()
    longitudEntry.pack_forget()

    T2cuadradoButton = tk.Button(frame1, text="Calcular T2\nROI cuadrado", command=lambda: ajusteROI(longitud))
    T2cuadradoButton.pack()

def tryRoi(X, Y, radio):
    # Recargamos la imagen para limpiar el ROI.
    ax.clear()
    ax.imshow(imagenReescalada, cmap=plt.cm.bone)
    canvas_tkagg1.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    # Crea un rectángulo que representa el cuadrado
    rect = patches.Rectangle(
        (X - radio, Y - radio),
        2 * radio, 2 * radio,
        linewidth=2, edgecolor='yellow', facecolor='none'
    )
    ax.add_patch(rect)
    canvas_tkagg1.draw()

def ajusteROI(longitud):
# Limpiamos y reajustamos la interfaz.
    T2cuadradoButton.pack_forget()

    # Entradas para el centro y radio del ROI
    centro_x_label = tk.Label(frame1, text="Centro X del ROI:")
    centro_x_label.pack()
    centro_x_entry = tk.Entry(frame1)
    centro_x_entry.pack()

    centro_y_label = tk.Label(frame1, text="Centro Y del ROI:")
    centro_y_label.pack()
    centro_y_entry = tk.Entry(frame1)
    centro_y_entry.pack()

    radio_label = tk.Label(frame1, text="Radio del ROI:")
    radio_label.pack()
    radio_entry = tk.Entry(frame1)
    radio_entry.pack()

    tryROI = tk.Button(frame1, text="Previsualizar ROI", command=lambda: tryRoi(int(centro_x_entry.get()), int(centro_y_entry.get()), int(radio_entry.get())))
    tryROI.pack()
    
    # Botón para confirmar ROI:
    addDatos = tk.Button(frame1, text="Confirmar", command=lambda: calcT2SquareROI(longitud, int(centro_x_entry.get()),
                                                                                            int(centro_y_entry.get()), int(radio_entry.get())))
    addDatos.pack()

# Cálculo de T2 para una ROI cuadrada de radio y centro variables
def calcT2SquareROI(no_tomas, X, Y, radio):
    global file_path
    
    file_name = os.path.basename(path_name)
    directorio = os.path.dirname(path_name)
    firstNum = int(file_name[4:7])
    listaTE = [];
    listaValoresT2 = [];
    offsetT2 = 0.1;

    # Matriz para almacenar las sumas de intensidades en el ROI a lo largo de 100 imágenes
    sumas_intensidades = np.zeros(no_tomas, dtype=np.float64)    

    for i in range(0, no_tomas):
        imageFileName = f"/MRIm{(i+firstNum):03d}.dcm"
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
        sumas_intensidades[i] = np.mean(roi)

        # Guardamos los tiempos de Eco para calcular T2.
        listaTE.append(img.EchoTime)

    for te, St in zip(listaTE, sumas_intensidades):
        T2 = -te / math.log(St / offsetT2)
        listaValoresT2.append(T2);
    valorMedioT2 = round(np.mean(listaValoresT2), 3)

    ax2.clear()    
    ax2.plot(sumas_intensidades)
    plt.title('Valores ROI cuadrado.\nT2 calculado: '+str(valorMedioT2)+'ms');
    plt.xlabel('Imagen')
    plt.ylabel('Intensidad Media')
    canvas_tkagg2.draw()

def main(file_path):
    global canvas_tkagg2, path_name, fig2, ax2, imagenReescalada, fig, ax, frame1, frame2, canvas_tkagg1, pathText, longitudEntry, logitudText, addDatos, ventanaMetodos

    path_name = file_path

    # Ventana para métodos
    ventanaMetodos = tk.Tk()
    ventanaMetodos.title("Análisis T2")
    ventanaMetodos.geometry("1200x800")
    
    frame1 = tk.Frame(ventanaMetodos)
    frame2 = tk.Frame(ventanaMetodos)
    frame1.pack(side="left")
    frame2.pack(side="right")

    file_name = os.path.basename(file_path)
    img = dicom.dcmread(file_path)
    imagenReescalada = img.RescaleSlope * img.pixel_array

    # Elementos para el Frame 1
    label1 = tk.Label(frame1, text= file_name, font=("Helvetica", 12, "bold"))
    label1.pack()

    canvas1 = Canvas(frame1)
    canvas1.pack()
    fig, ax = plt.subplots()
    ax.imshow(imagenReescalada, cmap=plt.cm.bone)
    canvas_tkagg1 = FigureCanvasTkAgg(fig, master=canvas1)
    canvas_tkagg1.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    logitudText = tk.Label(frame1, text="Longitud de la serie de T2:")
    logitudText.pack()
    longitudEntry = tk.Entry(frame1)
    longitudEntry.pack()

    addDatos = tk.Button(frame1, text="Añadir", command=lambda: verificarDatos(int(longitudEntry.get())))
    addDatos.pack()

    # Elementos para frame 2
    label2 = tk.Label(frame2, text="Análisis", font=("Helvetica", 12, "bold"))
    label2.pack()

    canvas2 = Canvas(frame2, width=512, height=512)
    canvas2.pack()
    fig2, ax2 = plt.subplots()
    canvas_tkagg2 = FigureCanvasTkAgg(fig2, master=canvas2)
    canvas_tkagg2.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    # Iniciar la ventana
    ventanaMetodos.mainloop()
