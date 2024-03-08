import math
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import messagebox
from tkinter import filedialog
from tkinter import Canvas
from tkinter import filedialog
import tkinter as tk
import pydicom as dicom
import matplotlib.patches as patches
from scipy.optimize import curve_fit

# Función para cargar y mostrar la imagen DICOM
def cargar_mostrar_imagen(idx):
    global imagenReescalada, file_path
    file_path = dicom_files[idx]
    ds = dicom.dcmread(file_path)
    imagenReescalada = ds.pixel_array

    # Limpia el área del canvas antes de mostrar una nueva imagen
    ax.clear()
    ax.imshow(imagenReescalada, cmap=plt.cm.bone)
    canvas_tkagg1.draw()
    
    # Actualiza el label con el nombre del archivo
    file_name = os.path.basename(file_path)
    label1.config(text=file_name)

# Función para avanzar a la siguiente imagen
def siguiente_imagen():
    global imagen_idx
    imagen_idx = (imagen_idx + 1) % len(dicom_files)  # Asegura ciclar la lista
    cargar_mostrar_imagen(imagen_idx)

# Función para regresar a la imagen anterior
def imagen_anterior():
    global imagen_idx
    imagen_idx = (imagen_idx - 1) % len(dicom_files)  # Asegura ciclar la lista
    cargar_mostrar_imagen(imagen_idx)


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


def modeloT2(TE, ST, T2):
    return -TE / math.log(ST / T2)

# Cálculo de T2 para una ROI cuadrada de radio y centro variables
def calcT2map(X, Y, radio):
    global file_path
    directorio = os.path.dirname(file_path)

    listaTE = [];
    listaValoresT2 = [];
    sumas_intensidades = [];

    img = dicom.dcmread(file_path)
    imagenReescalada = img.RescaleSlope * img.pixel_array
    offsetT2 = imagenReescalada.max();

    for archivo in os.listdir(directorio):
        ruta_completa = os.path.join(directorio, archivo)
        img = dicom.dcmread(ruta_completa)
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
        sumas_intensidades.append(np.mean(roi))
        # Guardamos los tiempos de Eco para calcular T2.
        listaTE.append(img.EchoTime)

    for te, St in zip(listaTE, sumas_intensidades):
        T2 = -te / math.log(St / offsetT2)
        listaValoresT2.append(T2);
    valorMedioT2 = round(np.mean(listaValoresT2), 3)

    ax2.clear()    
    ax2.plot(sumas_intensidades)
    plt.title('Valores ROI cuadrado.\nT2: '+str(valorMedioT2)+'ms');
    plt.xlabel('Imagen')
    plt.ylabel('Intensidad Media')
    canvas_tkagg2.draw()

# Ventana para métodos
ventanaMetodos = tk.Tk()
ventanaMetodos.wait_visibility()
ventanaMetodos.title("Análisis T2")
ventanaMetodos.geometry("1200x800")

file_path = os.path.abspath(filedialog.askopenfilename())
dir_path = os.path.dirname(file_path)

# Lista todos los archivos DICOM en el directorio
dicom_files = [os.path.join(dir_path, f) for f in os.listdir(dir_path) if f.endswith('.dcm')]
imagen_idx = dicom_files.index(file_path)  # Index del archivo seleccionado inicialmente

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

# Botones para navegar entre imágenes
btn_anterior = tk.Button(frame1, text="<", command=imagen_anterior)
btn_anterior.pack(side=tk.LEFT)
btn_siguiente = tk.Button(frame1, text=">", command=siguiente_imagen)
btn_siguiente.pack(side=tk.RIGHT)

# Carga la primera imagen
cargar_mostrar_imagen(imagen_idx)

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
addDatos = tk.Button(frame1, text="Confirmar", command=lambda: calcT2map(int(centro_x_entry.get()), int(centro_y_entry.get()), int(radio_entry.get())))
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
