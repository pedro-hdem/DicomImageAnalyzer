from tkinter import filedialog
import pydicom as dicom
import os

file_path = filedialog.askopenfilename()
# img = dicom.dcmread(file_path)
# imagenReescalada = img.RescaleSlope * img.pixel_array

file_name = os.path.basename(file_path)
directorio = os.path.dirname(file_path)
firstNum = int(file_name[4:7])

for i in range(0, 100):
    imageFileName = f"/MRIm{(i+firstNum):03d}.dcm"
    img = dicom.dcmread(directorio + imageFileName)
    print(img)