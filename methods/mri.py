import math
import pydicom as dicom;
import pydicom.data as dicomdata;
import matplotlib.pyplot as plt;
import numpy as np;

#Esto se poner en el Main!!
#coreFileLocation = "C:/Users/hdemp/Mi unidad/0. Master Bio/TFM/Experimentos/2023_ICON_89_19102023/DICOM/I00Sjgrn01_I00,_2023-10-16_Raton-01_basal__E10_P1/"
#imageFileName = "MRIm001.dcm"

def calcT2for1px():
    #Cálculo de T2 para un pixel:
    listaIntensidadPixel = [];
    listaTE = [];
    listaValoresT2 = [];

    for i in range(1, 101):
        imageFileName = f"MRIm{i:03d}.dcm"
        img = dicom.dcmread(coreFileLocation+imageFileName);
        imagenReescalada = tuple(img.RescaleSlope * el for el in img.pixel_array);
        
        # Lista con los valores del pixel de interés.
        listaIntensidadPixel.append(imagenReescalada[50][50]);
        listaTE.append(img.EchoTime)

    # Cálculo de T2 con la fórmula exponencial despejada.
    # Por algún extraño motivo, si pones el valor inicial de intensidad tal cual el programa explota, por eso lo redondeo.
    s0 = round(listaIntensidadPixel[0], 4);
    for te, St in zip(listaTE, listaIntensidadPixel):
        T2 = -te / math.log(St / s0)
        listaValoresT2.append(T2);

    valorMedioT2 = np.mean(listaValoresT2)
    print("T2 Medio pixel (50,50): ", valorMedioT2)
    plt.plot(listaIntensidadPixel)
    plt.title('Valores Pixel (50,50)')
    plt.xlabel('Imagen')
    plt.ylabel('Intensidad Media')
    plt.show()

def calcT2ROI9x9():
    #Cálculo de T2 para una ROI cuadrada de 9x9:
    intensidadesPixel1 = [];
    intensidadesPixel2 = [];
    intensidadesPixel3 = [];
    intensidadesPixel4 = [];
    intensidadesPixel5 = [];
    intensidadesPixel6 = [];
    intensidadesPixel7 = [];
    intensidadesPixel8 = [];
    intensidadesPixel9 = [];
    intensidadMediaVoxel = [];
    listaTE = [];
    listaValoresT2 = [];

    for i in range(1, 101):
        imageFileName = f"MRIm{i:03d}.dcm"
        img = dicom.dcmread(coreFileLocation+imageFileName);
        imagenReescalada = tuple(img.RescaleSlope * el for el in img.pixel_array);
        
        # Lista con los valores del pixel de interés.
        intensidadesPixel1.append(imagenReescalada[50][50]);
        intensidadesPixel2.append(imagenReescalada[49][50]);
        intensidadesPixel3.append(imagenReescalada[49][49]);
        intensidadesPixel4.append(imagenReescalada[50][49]);
        intensidadesPixel5.append(imagenReescalada[51][50]);
        intensidadesPixel6.append(imagenReescalada[51][51]);
        intensidadesPixel7.append(imagenReescalada[50][51]);
        intensidadesPixel8.append(imagenReescalada[49][51]);
        intensidadesPixel9.append(imagenReescalada[51][49]);
        listaTE.append(img.EchoTime)

    for i in range(100):
        suma_valores = (
            intensidadesPixel1[i]
            + intensidadesPixel2[i]
            + intensidadesPixel3[i]
            + intensidadesPixel4[i]
            + intensidadesPixel5[i]
            + intensidadesPixel6[i]
            + intensidadesPixel7[i]
            + intensidadesPixel8[i]
            + intensidadesPixel9[i]
        )
        promedioPixel = suma_valores / 9  # Divide por 9 ya que tienes 9 listas
        intensidadMediaVoxel.append(promedioPixel)

    # Cálculo de T2 con la fórmula exponencial despejada.
    # Por algún extraño motivo, si pones el valor inicial de intensidad tal cual el programa explota, por eso lo redondeo.
    s0 = round(intensidadMediaVoxel[0], 4);
    for te, St in zip(listaTE, intensidadMediaVoxel):
        T2 = -te / math.log(St / s0)
        listaValoresT2.append(T2);

    valorMedioT2 = np.mean(listaValoresT2)
    print("T2 Medio pixel (50,50): ", valorMedioT2)
    plt.plot(intensidadMediaVoxel)
    plt.title('Valores ROI 9x9')
    plt.xlabel('Imagen')
    plt.ylabel('Intensidad Media')
    plt.show()

def calcT2SquareROI():
    # Cálculo de T2 para una ROI cuadrada de radio y centro variables
    radio = 5  # Radio del ROI
    no_tomas = 100  # Número de tomas del mapa de T2
    X = 50  # Posición X del centro del ROI
    Y = 50  # Posición Y del centro del ROI
    listaTE = [];
    listaValoresT2 = [];

    # Matriz para almacenar las sumas de intensidades en el ROI a lo largo de 100 imágenes
    sumas_intensidades = np.zeros(no_tomas, dtype=np.float64)

    for i in range(1, no_tomas + 1):
        imageFileName = f"MRIm{i:03d}.dcm"
        img = dicom.dcmread(coreFileLocation + imageFileName)
        imagenReescalada = img.RescaleSlope * img.pixel_array  # Imagen con factor de reescalado

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


    s0 = round(sumas_intensidades[0], 4);

    for te, St in zip(listaTE, sumas_intensidades):
        T2 = -te / math.log(St / s0)
        listaValoresT2.append(T2);
    valorMedioT2 = np.mean(listaValoresT2)

    print(valorMedioT2)

    plt.plot(sumas_intensidades)
    plt.title('Valores ROI cuadrado. \n Radio: '+str(radio)+' Centro del ROI: '+str(X)+','+str(Y));
    plt.xlabel('Imagen')
    plt.ylabel('Intensidad Media')
    plt.show()