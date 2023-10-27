coreFileLocation = "C:/Users/hdemp/Mi unidad/0. Master Bio/TFM/Experimentos/2023_ICON_89_19102023/DICOM/I00Sjgrn01_I00,_2023-10-16_Raton-01_basal__E10_P1/"
imageFileName = "MRIm001.dcm"

# Prueba básica para imprimir una imagen:
filename = dicomdata.data_manager.get_files(coreFileLocation, imageFileName)[0] 
img = dicom.dcmread(filename);
print(img)
print("Factor de reescalado: ",img.RescaleSlope);
imagenReescalada = tuple(img.RescaleSlope * el for el in img.pixel_array);
print("Valor del pixel 50, 50: ", imagenReescalada[50][50])
print(len(img.pixel_array))
plt.imshow(imagenReescalada, cmap=plt.cm.bone)
plt.savefig('imagenReescalada.png', dpi=100)

# Función para actualizar el centro y radio del ROI
def actualizar_roi():
    global centro_x, centro_y, radio
    centro_x = int(centro_x_entry.get())
    centro_y = int(centro_y_entry.get())
    radio = int(radio_entry.get())

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

# Variables para el centro y radio del ROI
centro_x, centro_y = 0, 0
radio = 5  # Valor predeterminado