import pydicom as dicom
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog
from tkinter import Canvas
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# Importar métodos de análisis
import os

def ejecutar_archivo(archivo):
  path = os.path.abspath("./methods/mri/" + archivo)
  return os.system("python " + path)

# Función para cargar una imagen
def cargar_imagen(frame):
    global imagenReescalada
    global centro_x, centro_y, radio
    global fig1, fig2, canvas_tkagg1, canvas_tkagg2, ax1, ax2
    global img1, img2
    
    file_path = filedialog.askopenfilename()
    img = dicom.dcmread(file_path)
    imagenReescalada = img.RescaleSlope * img.pixel_array
    centro_x, centro_y = imagenReescalada.shape[1] // 2, imagenReescalada.shape[0] // 2

    if frame == 1:
        img1 = img
        ax1.clear()
        ax1.imshow(imagenReescalada, cmap=plt.cm.bone)
        canvas_tkagg1.draw()
        mostrar_botones(img1.Modality, frame)
    else:
        img2 = img
        ax2.clear()
        ax2.imshow(imagenReescalada, cmap=plt.cm.bone)
        canvas_tkagg2.draw()
        mostrar_botones(img2.Modality, frame)

# Función para mostrar botones y etiqueta
def mostrar_botones(buttonType, frame):
    if(frame == 1):
        frameSelector = frame1
    else:
        frameSelector = frame2

    if(buttonType == 'MR'):
        # Botones y etiqueta para mri
        mri_buttons = [
            tk.Button(frameSelector, text="Cálculo de T1"),
            tk.Button(frameSelector, text="Cálculo de T2 \n (Seleccionar carpeta con mapa de T2)", command=lambda: ejecutar_archivo("T2.py")),
            tk.Button(frameSelector, text="Segmentación")
        ]
        imagen_type_label = tk.Label(frameSelector, text=f"Tipo de Imagen {frame}: MRI")

        for button in mri_buttons:
            button.pack()
        imagen_type_label.pack()
    
    if(buttonType == 'CT'):
        # Botones y etiqueta para mri
        ct_buttons = [
            tk.Button(frameSelector, text="Calcular Movida de CT"),
            tk.Button(frameSelector, text="Segmentación")
        ]
        imagen_type_label = tk.Label(frameSelector, text=f"Tipo de Imagen {frame}: CT")

        for button in ct_buttons:
            button.pack()
        imagen_type_label.pack()

# Crear la ventana
window = tk.Tk()
window.title("DICOM Image Analyzer")

# Frames para las dos imágenes
frame1 = tk.Frame(window, width=300, height=300)
frame2 = tk.Frame(window, width=300, height=300)
frame1.pack(side="left")
frame2.pack(side="right")
frame1_image_loaded = tk.BooleanVar()
frame2_image_loaded = tk.BooleanVar()

# Elementos para el Frame 1
label1 = tk.Label(frame1, text="Imagen 1", font=("Helvetica", 12, "bold"))
label1.pack()

cargar_button1 = tk.Button(frame1, text="Cargar Imagen", command=lambda: cargar_imagen(1))
cargar_button1.pack()

canvas1 = Canvas(frame1, width=512, height=512)
canvas1.pack()
fig1, ax1 = plt.subplots()
plt.axis('off')
canvas_tkagg1 = FigureCanvasTkAgg(fig1, master=canvas1)
canvas_tkagg1.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# Elementos para el Frame 2
label2 = tk.Label(frame2, text="Imagen 2", font=("Helvetica", 12, "bold"))
label2.pack()

cargar_button2 = tk.Button(frame2, text="Cargar Imagen", command=lambda: cargar_imagen(2))
cargar_button2.pack()

canvas2 = Canvas(frame2, width=512, height=512)
canvas2.pack()
fig2, ax2 = plt.subplots()
plt.axis('off')
canvas_tkagg2 = FigureCanvasTkAgg(fig2, master=canvas2)
canvas_tkagg2.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# Variable para almacenar la imagen reescalada
imagenReescalada = None

# Iniciar la ventana
window.mainloop()