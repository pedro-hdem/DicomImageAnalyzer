import pydicom as dicom;
import pydicom.data as dicomdata;
import matplotlib.pyplot as plt;
import numpy as np;
# Para la interfaz gráfica.
import tkinter as tk
from tkinter import filedialog
from tkinter import Canvas
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

coreFileLocation = "C:/Users/hdemp/Mi unidad/0. Master Bio/TFM/Experimentos/2023_ICON_89_19102023/DICOM/I00Sjgrn01_I00,_2023-10-16_Raton-01_basal__E10_P1/"
imageFileName = "MRIm001.dcm"

# Prueba básica para imprimir una imagen:
# filename = dicomdata.data_manager.get_files(coreFileLocation, imageFileName)[0] 
# img = dicom.dcmread(filename);
# print(img)
# print("Factor de reescalado: ",img.RescaleSlope);
# imagenReescalada = tuple(img.RescaleSlope * el for el in img.pixel_array);
# print("Valor del pixel 50, 50: ", imagenReescalada[50][50])
# print(len(img.pixel_array))
# plt.imshow(imagenReescalada, cmap=plt.cm.bone)
# plt.savefig('imagenReescalada.png', dpi=100)

# Función para cargar una imagen
def cargar_imagen():
    global imagenReescalada
    global centro_x, centro_y, radio

    file_path = filedialog.askopenfilename()
    img = dicom.dcmread(file_path)
    imagenReescalada = img.RescaleSlope * img.pixel_array
    centro_x, centro_y = imagenReescalada.shape[1] // 2, imagenReescalada.shape[0] // 2

    # Redibuja la imagen
    canvas.delete("all")
    fig, ax = plt.subplots()
    ax.imshow(imagenReescalada, cmap=plt.cm.bone)
    canvas_tkagg = FigureCanvasTkAgg(fig, master=canvas)
    canvas_tkagg.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# Función para actualizar el centro y radio del ROI
def actualizar_roi():
    global centro_x, centro_y, radio
    centro_x = int(centro_x_entry.get())
    centro_y = int(centro_y_entry.get())
    radio = int(radio_entry.get())

# Crear la ventana
window = tk.Tk()
window.title("DICOM Image Analyzer")

# Crear un lienzo para mostrar una imagen
canvas = Canvas(window, width=512, height=512)
canvas.pack()

# Botón para cargar una imagen
cargar_button = tk.Button(window, text="Cargar Imagen", command=cargar_imagen)
cargar_button.pack()

# Entradas para el centro y radio del ROI
centro_x_label = tk.Label(window, text="Centro X del ROI:")
centro_x_label.pack()
centro_x_entry = tk.Entry(window)
centro_x_entry.pack()

centro_y_label = tk.Label(window, text="Centro Y del ROI:")
centro_y_label.pack()
centro_y_entry = tk.Entry(window)
centro_y_entry.pack()

radio_label = tk.Label(window, text="Radio del ROI:")
radio_label.pack()
radio_entry = tk.Entry(window)
radio_entry.pack()

actualizar_button = tk.Button(window, text="Actualizar ROI", command=actualizar_roi)
actualizar_button.pack()

# Variable para almacenar la imagen reescalada
imagenReescalada = None

# Variables para el centro y radio del ROI
centro_x, centro_y = 0, 0
radio = 5  # Valor predeterminado

# Iniciar la ventana
window.mainloop()
