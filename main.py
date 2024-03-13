# Importar métodos de análisis
from utils.imports import *

def mostrar_info(method):
    if (method == 'T2'):
        labelInfo.config(text=textos["T2"])
    if (method == 'T1IR'):
        labelInfo.config(text=textos["T1IR"])
    if (method == 'CTHU'):
        labelInfo.config(text=textos["CTHU"])

def ocultar_info():
    labelInfo.config(text="")

def ejecutar_method(method):
    if (method == 'T2'):
        ruta_al_archivo = 'methods/mri/T2.py'
        subprocess.run(['python', ruta_al_archivo])
    if (method == 'T1IR'):
        ruta_al_archivo = 'methods/mri/T1.py'
        subprocess.run(['python', ruta_al_archivo])
    if (method == 'CTHU'):
        ruta_al_archivo = 'methods/ct/cthu.py'
        subprocess.run(['python', ruta_al_archivo])
        
def cargar_textos(ruta):
    with open(ruta, "r", encoding="utf-8") as archivo:
        return json.load(archivo)

# Crear la ventana
window = tk.Tk()
window.wait_visibility()
window.title("DICOM Image Analyzer")
window.geometry("500x300")
 
# Frames para las dos imágenes
frame1 = tk.Frame(window, width=250, height=300)
frame2 = tk.Frame(window, width=250, height=300)
frame1.pack(side="left")
frame2.pack(side="right", fill="both", expand=True)

# Configuración de los textos en pantalla desde el JSON
textos = cargar_textos("utils/textos.json")

# Elementos para el frame de la izquierda:
label2 = tk.Label(frame2, text="Información", font=("Helvetica", 12, "bold"))
label2.pack(fill="x", expand=False)

labelInfo = tk.Label(frame2, text="", font=("Helvetica", 10))
labelInfo.pack(fill="x", expand=False)

# Elementos para el Frame 1
label1 = tk.Label(frame1, text="Opciones de Análisis", font=("Helvetica", 12, "bold"))
label1.pack()

#Botones MRI:
label2 = tk.Label(frame1, text="MRI", font=("Helvetica", 11))
label2.pack()

cargar_MRI1 = tk.Button(frame1, text="Mapa de T1 (serie IR)", command=lambda: ejecutar_method('T1IR'))
cargar_MRI1.bind("<Enter>", lambda event, m='T1IR': mostrar_info(m))
cargar_MRI1.bind("<Leave>", lambda event: ocultar_info())
cargar_MRI1.pack()

cargar_MRI2 = tk.Button(frame1, text="Mapa de T2", command=lambda: ejecutar_method('T2'))
cargar_MRI2.bind("<Enter>", lambda event, m='T2': mostrar_info(m))
cargar_MRI2.bind("<Leave>", lambda event: ocultar_info())
cargar_MRI2.pack()

#Botones CT:
label2 = tk.Label(frame1, text="\nCT", font=("Helvetica", 11))
label2.pack()

cargar_CT1 = tk.Button(frame1, text="Cálcular HU", command=lambda: ejecutar_method('CTHU'))
cargar_CT1.bind("<Enter>", lambda event, m='CTHU': mostrar_info(m))
cargar_CT1.bind("<Leave>", lambda event: ocultar_info())
cargar_CT1.pack()

# Iniciar la ventana
window.mainloop()