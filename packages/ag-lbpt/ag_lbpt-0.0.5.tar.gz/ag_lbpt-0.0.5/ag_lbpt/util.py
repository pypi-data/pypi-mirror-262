# -*- coding: utf-8 -*-

""" Utilidades de Algoritmo Genético 
Versión   : 1.0
Autor     : Luis Beltran Palma Ttito
Lugar     : Cusco, Perú, 2024.
"""

#--------------------------------------------------------------------------------------------------------------------------------

import math
import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import networkx as nx
import folium
import random

from ag_lbpt.ag import AlgoritmoGenetico

#--------------------------------------------------------------------------------------------------------------------------------

Distancia = []
Costo = 0
Ruta = []
TSP = []
GEO = []
N = 0

Producto = []
ValorPeso = []
ValorProd = []
PesoMochila = 0
Ingreso = 0

MatrizAdyacente = []
Diccionario_SN = {}
Conflictos = 0

#--------------------------------------------------------------------------------------------------------------------------------
# LECTURA DE DATOS
#--------------------------------------------------------------------------------------------------------------------------------

# Lectura de archivo TSP 2D (x, y)
def LeerTSPcsv(ArchivoTSPcsv):
    global Distancia, TSP, N
    # Lee Archivo TSP desde csv
    df = pd.read_csv(ArchivoTSPcsv, sep=',', header=0)
    TSP = df.values
    N = len(df)
    Distancia = np.empty((N,N))
    for i in range(N):
        for j in range(N):
            if i == j:
                Distancia[i, j] = 0.000001 # debiera ser 0, pero 1/0 genera división por cero, pero no sera utilizado
            else:
                Distancia[i, j] = math.sqrt(math.pow(TSP[i,0] - TSP[j,0], 2) + math.pow(TSP[i,1] - TSP[j,1], 2))
    return TSP, Distancia, N

#--------------------------------------------------------------------------------------------------------------------------------

# Lectura de archivo GEO (Ciudad, Latitud, Longitud)
def LeerGEOcsv(ArchivoGEOcsv):
    global Distancia, GEO, N, TSP
    GEO = pd.read_csv(ArchivoGEOcsv, sep=',', header=0)
    df = GEO
    # Quitar atributo 'Ciudad' inecesrio para obtener matriz de distancias
    df = df.drop('Ciudad', axis=1)
    # Convertir a radianes
    df['Latitud'] = math.pi*df['Latitud']/180
    df['Longitud'] = math.pi*df['Longitud']/180
    TSP = df.values
    N = len(TSP)
    Distancia = np.empty((N,N))
    for j in range(N):
        for i in range(N):
            if i == j:
                Distancia[i, j] = 0.000001
            else:
                # distancia Haversina
                a = math.sin((TSP[i,0]-TSP[j,0])/2)**2
                b = math.cos(TSP[i,0])
                c = math.cos(TSP[j,0])
                d = math.sin((TSP[i,1]-TSP[j,1])/2)**2
                Distancia[i, j] = 2*6371*math.asin(math.sqrt(a + b * c * d))
    return GEO, Distancia, N

#--------------------------------------------------------------------------------------------------------------------------------

# Lectura de matriz de distancias: input: matriz de distancias, output: Distancia
def LeerDISTANCIAcsv(ArchivoDISTANCIAcsv):
    global Distancia
    # Leer distancia
    df = pd.read_csv(ArchivoDISTANCIAcsv, sep=',', header=0, index_col=0)
    df_float = df.astype(float)
    Distancia = np.array(df_float.values)
    return Distancia

#--------------------------------------------------------------------------------------------------------------------------------

# Lectura de archivo de productos (Producto, Valor, Peso)
def LeerVALOR_PESOcsv(ArchivoVPcsv):
    global ValorPeso, Producto
    df = pd.read_csv(ArchivoVPcsv, sep=',', header=0)
    Producto = df
    df = df.drop(['Producto'], axis=1)
    ValorPeso = df.astype(float).values
    return ValorPeso

#--------------------------------------------------------------------------------------------------------------------------------

# Lectura de archivo TSP (Producto, Valor)
def LeerVALOR_CANTcsv(ArchivoVCcsv):
    global ValorProd, Producto
    df = pd.read_csv(ArchivoVCcsv, sep=',', header=0)
    Producto = df
    df = df.drop(['Producto'], axis=1)
    ValorProd = df.astype(float).values
    return ValorProd

#--------------------------------------------------------------------------------------------------------------------------------

# Lectura de GRAFO (grafo como matriz: Fila 1: Nodos; Fila 2...N: Nodos adyacentes)
def LeerGRAFOcsv(ArchivoGRAFOcsv):
    global MatrizAdyacente, Diccionario_SN, N
    df = pd.read_csv(ArchivoGRAFOcsv, sep=',', header=0)
    # Cantidad de paises o cantidad de atributos
    N = df.shape[1]
    # Convertir DataFrame a Diccionario
    Diccionario = df.to_dict(orient='list')
    # Quitar valores negativos del diccionario (negativos representa la no existencia de adyacentes)
    Diccionario_SN = {key: [num for num in value if num >= 0] for key, value in Diccionario.items()}
    # Crear matriz de adyacencia
    MatrizAdyacente = np.zeros((N, N))
    for pais, vecinos in Diccionario_SN.items():
        for vecino in vecinos:
            MatrizAdyacente[int(pais), vecino] = 1
            MatrizAdyacente[vecino, int(pais)] = 1  # Para grafos no dirigidos
    MatrizAdyacente = MatrizAdyacente.astype(int)
    return Diccionario_SN, MatrizAdyacente

#--------------------------------------------------------------------------------------------------------------------------------
# FUNCION DE APTITUD
#--------------------------------------------------------------------------------------------------------------------------------

# Función heurística para TSP: Sumatoria de peso de aristas de la ruta 
def AptitudTSP(Ruta):
    global Distancia
    
    Costo = 0
    N = len(Ruta)
    for k in range(len(Ruta)-1):
        Costo = Costo + Distancia[Ruta[k], Ruta[k+1]]
    Costo = Costo + Distancia[Ruta[N-1], Ruta[0]]
    return Costo

#---------------------------------------------------------------------------------------------------------------------------

# Verifica si 2 reinas se atacan
def HayAtaque(X1,Y1,X2,Y2):
    return int((abs(X1-X2) == abs(Y1-Y2)) or (X1 == X2) or (Y1 == Y2))

# función de aptitud para N-reinas
# suma cantidad de ataques entre par de reinas
def AptitudREINA(Ruta):
    Ataques = 0
    for i in range(len(Ruta)-1):
        for j in range(i+1,len(Ruta)):
             Ataques = Ataques + HayAtaque(Ruta[i],i,Ruta[j],j)
    return Ataques

#--------------------------------------------------------------------------------------------------------------------------------

# Función heurística: 
# Si peso total excede el peso de la mochila --> costo es el peso total
# Si peso total NO excede el peso de la mochila --> proporción de peso que falta por cubir la mochila * peso de la mochila
def AptitudMOCHILA(Ruta):
    global ValorPeso,PesoMochila, Costo
    ValorTotal = 0.0
    PesoTotal = sum(Ruta)
    N = len(Ruta)
    for k in range(len(Ruta)):
        ValorTotal = ValorTotal +  Ruta[k]*ValorPeso[k][0]
    # Planteado por LBPT
    # Penaliza por exceder el peso de la mochila
    Costo = 0.0
    if PesoTotal > PesoMochila:
        Costo=PesoTotal
    else:
        Costo = abs(1-PesoTotal/PesoMochila)*PesoMochila
    # Penaliza por valor muy bajo 
    Costo = Costo + (PesoTotal/ValorTotal)*PesoMochila
    return Costo

#--------------------------------------------------------------------------------------------------------------------------------

# Función heurística:
# Si costo total excede el ingreso --> exceso por coef. de penalización
# Si costo total NO excede el ingreso --> faltante por coef. de penalización
def AptitudUtilidad(Ruta):
    global ValorProd, Ingreso, Costo
    CostoTotal = 0.0
    N = len(Ruta)
    for k in range(len(Ruta)):
        CostoTotal = CostoTotal + Ruta[k] * ValorProd[k][0]
    # Planteado por LBPT
    CoefPenaliza = 2
    Costo = 0.0
    if CostoTotal > Ingreso:
        Costo = (CostoTotal - Ingreso) * CoefPenaliza * CoefPenaliza
    if CostoTotal <= Ingreso:
        Costo  = (Ingreso - CostoTotal) * CoefPenaliza
    return Costo

#--------------------------------------------------------------------------------------------------------------------------------

# Función heurística: Conteo de par de nodos que usan el mismo color
def AptitudColorGrafo(Ruta):
    global Conflictos, MatrizAdyacente, N
    Conflictos = 0
    N = len(Ruta)
    for i in range(N):
        for j in range(i + 1, N):
            if MatrizAdyacente[i, j] == 1 and Ruta[i] == Ruta[j]:
                Conflictos = Conflictos + 1
    return Conflictos


#--------------------------------------------------------------------------------------------------------------------------------
# SALIDA DE RESULTADOS
#--------------------------------------------------------------------------------------------------------------------------------

# Grafica solución de n-reinas
def GraficaReinas(Solucion, ArchivoSolucion):
    N = len(Solucion)
    rotulo = np.linspace(-0.4, N-0.6, num=N+1)
    matriz = np.ones((N,N), dtype='int')
    i = -1
    for j in Solucion:
        i = i + 1
        matriz[i,j] = 0
    reinas = pd.DataFrame(matriz)
    reinas.to_csv(ArchivoSolucion, index=False,header=False)
    # Graficar disposición de reinas
    fig, ax = plt.subplots(figsize=(N//3, N//3))
    plt.grid(color='gray', linestyle='-', linewidth=0.2)
    plt.imshow(matriz, cmap='gray')
    plt.yticks(ticks=rotulo)
    plt.xticks(ticks=rotulo)
    ax.set_xlabel('', color='white')
    ax.set_ylabel('', color='white')
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')
    plt.show()

#--------------------------------------------------------------------------------------------------------------------------------

# Función que resalta con color verde el valor máximo en columnas específicas
def highlight_max_in_columns(s, columns):
    is_max = s == s.max()
    return ['background-color: green' if v and s.name in columns else '' for v in is_max]


# Muestra Resultado de MOCHILA valor peso
def muestraMOCHILAValorPeso(Producto):
    Producto.to_csv('MOCHILAValorPeso.csv', index=False)
    # Lista de columnas a las cuales quieres aplicar el estilo
    columns_con_estilo = ['Peso', 'Importe']
    # Aplica el estilo usando la función .apply()
    Producto_estilo = Producto.style.apply(highlight_max_in_columns, columns=columns_con_estilo)
    return Producto_estilo
    
#--------------------------------------------------------------------------------------------------------------------------------

# Muestra Resultado de MOCHILA valor peso
def muestraMOCHILAValor(Producto):
    Producto.to_csv('MOCHILAValor.csv', index=False)
    # Lista de columnas a las cuales quieres aplicar el estilo
    columns_con_estilo = ['Importe']
    # Aplica el estilo usando la función .apply()
    Producto_estilo = Producto.style.apply(highlight_max_in_columns, columns=columns_con_estilo)
    return Producto_estilo

#--------------------------------------------------------------------------------------------------------------------------------

# Crear un archivo html con la ruta GEO encontrada
def GraficaMapaGEO(MapaHTML,GEO,Ruta,LatitudCentro=-12.06, LongitudCentro=-75.2,Zoom=5):
    geo = []
    for k in Ruta:
        geo.append([GEO.at[k,'Ciudad'], GEO.at[k,'Latitud'], GEO.at[k,'Longitud']])
    # Centrado del mapa y zoom
    mapa = folium.Map(location=[LatitudCentro, LongitudCentro], zoom_start=Zoom)
    # Trazar ciudades
    for k in range(len(Ruta)):
        folium.Marker([geo[k][1], geo[k][2]], popup= geo[k][0]).add_to(mapa)
    # Trazar lineas de la Ruta
    for k in range(len(Ruta)-1):
        folium.PolyLine([(geo[k][1], geo[k][2]), (geo[k+1][1], geo[k+1][2])],
                    color="blue", weight=0.5, opacity=1).add_to(mapa)
    # Grabar mapa
    mapa.save(MapaHTML)

#--------------------------------------------------------------------------------------------------------------------------------

# Grafica grafo coloreado
def GraficarGrafo(Solucion, Diccionario_SN):
    # Crear un nuevo grafo
    G = nx.Graph()

    norm = plt.Normalize(np.array(Solucion).min(), np.array(Solucion).max())
    cmap = plt.cm.viridis
    colores = cmap(norm(Solucion))
    nombres_colores = [mcolors.rgb2hex(c) for c in colores]

    for clave in Diccionario_SN:
        G.add_node(int(clave))

    for clave, valores in Diccionario_SN.items():
        for valor in valores:
            G.add_edge(int(clave),valor)

    nx.draw(G, node_color=nombres_colores, with_labels=True)
    plt.show()

#--------------------------------------------------------------------------------------------------------------------------------

# Función que ensambla el Genoma 
def EnsamblajeGenoma(ArchivoADNcsv, Solapamiento, Bases, Solucion):

    # Ruta del archivo CSV
    file_path = 'genoma.csv'
    # Lee los trozos de adn
    adn = pd.read_csv(ArchivoADNcsv, sep=',', header=0)

    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
       
        # Muestra los trozos de ADN uno debajo del otro con solapamiento de 4 bases
        j = -1
        for k in Solucion:
            j = j + 1
            if j == 0:
                writer.writerow(''+adn.iloc[k, 1])
                print('',adn.iloc[k, 1])    
            else:
                writer.writerow((' ' * (j*(Bases-Solapamiento))) + adn.iloc[k, 1])
                print((' ' * (j*(Bases-Solapamiento))), adn.iloc[k, 1])

        # Ensambla en Genoma
        genoma = ""
        j = -1
        for k in Solucion:
            j = j + 1
            if j == 0:
                genoma = genoma + (adn.iloc[k, 1])
            else:
                genoma = genoma + (adn.iloc[k, 1])[Solapamiento:Bases]
    
        writer.writerow('' + genoma)
    # Muestra genoma al final
    print('',genoma)
    
    return genoma

#--------------------------------------------------------------------------------------------------------------------------------
# EJECUCIÓN DE ALGRITMO GENÉTICO
#--------------------------------------------------------------------------------------------------------------------------------

# Función ejecuta AG para TSP 
def agTSP(pArchivoTSPcsv, pIteraciones, pGeneraciones, pPoblacion, pProbMutacion, pTipoMutacion, 
           pTipoCruce, pGenUnico, pInicioFijo, pInicioFinFijo, pN, pPobElite):
    
    global Distancia, TSP, N
    TSP, Distancia, N = LeerTSPcsv(pArchivoTSPcsv)
    AG = AlgoritmoGenetico(
        Iteraciones=pIteraciones,         # Cantidad de iteraciones del AG
        Generaciones=pGeneraciones,       # Cantidad de generaciones del AG
        Poblacion=pPoblacion,             # Cantidad de población
        ProbMutacion=pProbMutacion,       # Probabilidad de mutación
        TipoMutacion=pTipoMutacion,       # Tipo de mutación ['Permuta', 'UnPunto']
        TipoCruce=pTipoCruce,             # Tipo de cruce ['Complemento', 'UnPunto']
        GenUnico=pGenUnico,               # True: Los genes no usan valores repetidos
        InicioFijo=pInicioFijo,           # True: El 1er gene siempre es '0'
        InicioFinFijo=pInicioFinFijo,     # True: El 1er gen = '0'; ultimo gen = 'N-1'
        N=pN,                             # Cantidad de ciudades
        PobElite=pPobElite,               # Cantidad de individuos de la élite
        FunAptitud=AptitudTSP             # Función de aptitud implementado externamente
    )

    Solucion, Costo = AG.Ejecutar()
    return AG, Solucion, Costo

#--------------------------------------------------------------------------------------------------------------------------------

# Ejecutar AG para N-Reinas
def agNReinas(pIteraciones, pGeneraciones, pPoblacion, pProbMutacion, pTipoMutacion, 
           pTipoCruce, pGenUnico, pInicioFijo, pInicioFinFijo, pN, pPobElite):
    
    AG = AlgoritmoGenetico(
        Iteraciones=pIteraciones,         # Cantidad de iteraciones del AG
        Generaciones=pGeneraciones,       # Cantidad de generaciones del AG
        Poblacion=pPoblacion,             # Cantidad de población
        ProbMutacion=pProbMutacion,       # Probabilidad de mutación
        TipoMutacion=pTipoMutacion,       # Tipo de mutación ['Permuta', 'UnPunto']
        TipoCruce=pTipoCruce,             # Tipo de cruce ['Complemento', 'UnPunto']
        GenUnico=pGenUnico,               # True: Los genes no usan valores repetidos
        InicioFijo=pInicioFijo,           # True: El 1er gene siempre es '0'
        InicioFinFijo=pInicioFinFijo,     # True: El 1er gen = '0'; ultimo gen = 'N-1'
        N=pN,                             # Cantidad de ciudades
        PobElite=pPobElite,               # Cantidad de individuos de la élite
        FunAptitud=AptitudREINA           # Función de aptitud implementado externamente
    )

    Solucion, Costo = AG.Ejecutar()
    return AG, Solucion, Costo

#--------------------------------------------------------------------------------------------------------------------------------

# Ejecutar AG para problema de mochila clasico
def agMOCHILA(pArchivoVPcsv, pPesoMochila, pIteraciones, pGeneraciones, pPoblacion, pProbMutacion, pTipoMutacion, 
           pTipoCruce, pGenUnico, pInicioFijo, pInicioFinFijo, pN, pMinCromosoma, pMaxCromosoma, pTipoDato, pPobElite):
    
    global ValorPeso, PesoMochila, Costo, Producto
    PesoMochila = pPesoMochila
    ValorPeso = LeerVALOR_PESOcsv(pArchivoVPcsv)
    AG = AlgoritmoGenetico(
        Iteraciones=pIteraciones,         # Cantidad de iteraciones del AG
        Generaciones=pGeneraciones,       # Cantidad de generaciones del AG
        Poblacion=pPoblacion,             # Cantidad de población
        ProbMutacion=pProbMutacion,       # Probabilidad de mutación
        TipoMutacion=pTipoMutacion,       # Tipo de mutación ['Permuta', 'UnPunto']
        TipoCruce=pTipoCruce,             # Tipo de cruce ['Complemento', 'UnPunto']
        GenUnico=pGenUnico,               # True: Los genes no usan valores repetidos
        InicioFijo=pInicioFijo,           # True: El 1er gene siempre es '0'
        InicioFinFijo=pInicioFinFijo,     # True: El 1er gen = '0'; ultimo gen = 'N-1'
        N=pN,                             # Cantidad de ciudades
        MinCromosoma=pMinCromosoma,       # Mínimo valor de genes
        MaxCromosoma=pMaxCromosoma,       # Máximo valor de genes
        TipoDato=pTipoDato,               # Tipo de dato de genes
        PobElite=pPobElite,               # Cantidad de individuos de la élite
        FunAptitud=AptitudMOCHILA         # Función de aptitud implementado externamente
    )

    Solucion, Costo = AG.Ejecutar()
    Producto['Cantidad'] = Solucion
    Producto['Importe'] = Producto['Valor'] * Producto['Cantidad']
    Producto.loc[len(Producto)] = ['PESO E IMPORTE DE LA MOCHILA', None, Producto['Cantidad'].sum(), None,
                                           Producto['Importe'].sum()]

    return AG, Solucion, Costo, Producto

#--------------------------------------------------------------------------------------------------------------------------------

# Ejecutar AG para TSP de coordenadas geográficas
def agTSPgeo(pArchivoGEOcsv, pIteraciones, pGeneraciones, pPoblacion, pProbMutacion, pTipoMutacion, 
           pTipoCruce, pGenUnico, pInicioFijo, pInicioFinFijo, pN, pPobElite):
    
    global Distancia, GEO, N
    GEO, Distancia, N = LeerGEOcsv(pArchivoGEOcsv)
    AG = AlgoritmoGenetico(
        Iteraciones=pIteraciones,         # Cantidad de iteraciones del AG
        Generaciones=pGeneraciones,       # Cantidad de generaciones del AG
        Poblacion=pPoblacion,             # Cantidad de población
        ProbMutacion=pProbMutacion,       # Probabilidad de mutación
        TipoMutacion=pTipoMutacion,       # Tipo de mutación ['Permuta', 'UnPunto']
        TipoCruce=pTipoCruce,             # Tipo de cruce ['Complemento', 'UnPunto']
        GenUnico=pGenUnico,               # True: Los genes no usan valores repetidos
        InicioFijo=pInicioFijo,           # True: El 1er gene siempre es '0'
        InicioFinFijo=pInicioFinFijo,     # True: El 1er gen = '0'; ultimo gen = 'N-1'
        N=pN,                             # Cantidad de ciudades
        PobElite=pPobElite,               # Cantidad de individuos de la élite
        FunAptitud=AptitudTSP             # Función de aptitud implementado externamente
    )

    Solucion, Costo = AG.Ejecutar()
    return AG, Solucion, Costo

#--------------------------------------------------------------------------------------------------------------------------------

# Ejecutar AG para problema de MOCHILA de utilidad de ventas
def agMOCHILAutilidad(pArchivoVCcsv, pIngreso, pIteraciones, pGeneraciones, pPoblacion, pProbMutacion, pTipoMutacion, 
           pTipoCruce, pGenUnico, pInicioFijo, pInicioFinFijo, pN, pMinCromosoma, pMaxCromosoma, pTipoDato, pPobElite):
    
    global ValorProd, Ingreso, Costo, Producto
    Ingreso = pIngreso
    ValorPeso = LeerVALOR_CANTcsv(pArchivoVCcsv)
    AG = AlgoritmoGenetico(
        Iteraciones=pIteraciones,         # Cantidad de iteraciones del AG
        Generaciones=pGeneraciones,       # Cantidad de generaciones del AG
        Poblacion=pPoblacion,             # Cantidad de población
        ProbMutacion=pProbMutacion,       # Probabilidad de mutación
        TipoMutacion=pTipoMutacion,       # Tipo de mutación ['Permuta', 'UnPunto']
        TipoCruce=pTipoCruce,             # Tipo de cruce ['Complemento', 'UnPunto']
        GenUnico=pGenUnico,               # True: Los genes no usan valores repetidos
        InicioFijo=pInicioFijo,           # True: El 1er gene siempre es '0'
        InicioFinFijo=pInicioFinFijo,     # True: El 1er gen = '0'; ultimo gen = 'N-1'
        N=pN,                             # Cantidad de ciudades
        MinCromosoma=pMinCromosoma,       # Mínimo valor de genes
        MaxCromosoma=pMaxCromosoma,       # Máximo valor de genes
        TipoDato=pTipoDato,               # Tipo de dato de genes
        PobElite=pPobElite,               # Cantidad de individuos de la élite
        FunAptitud=AptitudUtilidad        # Función de aptitud implementado externamente
    )

    Solucion, Costo = AG.Ejecutar()
    Producto['Cantidad'] = Solucion
    Producto['Importe'] = Producto['Valor'] * Producto['Cantidad']
    Producto.loc[len(Producto)] = ['CANTIDAD E IMPORTE DE LA MOCHILA', None, None,
                                           Producto['Importe'].sum()]
    

    return AG, Solucion, Costo, Producto

#--------------------------------------------------------------------------------------------------------------------------------

# Ejecutar AG para TSP desde matriz (simetrica o asimétrica) de distancias
def agTSPmd(pArchivoDISTANCIAcsv, pIteraciones, pGeneraciones, pPoblacion, pProbMutacion, pTipoMutacion, 
           pTipoCruce, pGenUnico, pInicioFijo, pInicioFinFijo, pN, pPobElite):
    
    global Distancia
    Distancia = LeerDISTANCIAcsv(pArchivoDISTANCIAcsv)
    AG = AlgoritmoGenetico(
        Iteraciones=pIteraciones,         # Cantidad de iteraciones del AG
        Generaciones=pGeneraciones,       # Cantidad de generaciones del AG
        Poblacion=pPoblacion,             # Cantidad de población
        ProbMutacion=pProbMutacion,       # Probabilidad de mutación
        TipoMutacion=pTipoMutacion,       # Tipo de mutación ['Permuta', 'UnPunto']
        TipoCruce=pTipoCruce,             # Tipo de cruce ['Complemento', 'UnPunto']
        GenUnico=pGenUnico,               # True: Los genes no usan valores repetidos
        InicioFijo=pInicioFijo,           # True: El 1er gene siempre es '0'
        InicioFinFijo=pInicioFinFijo,     # True: El 1er gen = '0'; ultimo gen = 'N-1'
        N=pN,                             # Cantidad de ciudades
        PobElite=pPobElite,               # Cantidad de individuos de la élite
        FunAptitud=AptitudTSP             # Función de aptitud implementado externamente
    )

    Solucion, Costo = AG.Ejecutar()
    return AG, Solucion, Costo

#--------------------------------------------------------------------------------------------------------------------------------

# Ejecutar AG para coloración de grafos
def agColorGrafo(pArchivoGRAFOcsv, pIteraciones, pGeneraciones, pPoblacion, pProbMutacion, pTipoMutacion, 
           pTipoCruce, pGenUnico, pInicioFijo, pInicioFinFijo, pN, pMinCromosoma, pMaxCromosoma, pTipoDato, pPobElite):

    global MatrizAdyacente, Diccionario_SN, N
    Diccionario_SN, MatrizAdyacente = LeerGRAFOcsv(pArchivoGRAFOcsv)
    AG = AlgoritmoGenetico(
        Iteraciones=pIteraciones,         # Cantidad de iteraciones del AG
        Generaciones=pGeneraciones,       # Cantidad de generaciones del AG
        Poblacion=pPoblacion,             # Cantidad de población
        ProbMutacion=pProbMutacion,       # Probabilidad de mutación
        TipoMutacion=pTipoMutacion,       # Tipo de mutación ['Permuta', 'UnPunto']
        TipoCruce=pTipoCruce,             # Tipo de cruce ['Complemento', 'UnPunto']
        GenUnico=pGenUnico,               # True: Los genes no usan valores repetidos
        InicioFijo=pInicioFijo,           # True: El 1er gene siempre es '0'
        InicioFinFijo=pInicioFinFijo,     # True: El 1er gen = '0'; ultimo gen = 'N-1'
        N=pN,                             # Cantidad de ciudades
        MinCromosoma=pMinCromosoma,       # Mínimo valor de genes
        MaxCromosoma=pMaxCromosoma,       # Máximo valor de genes
        TipoDato=pTipoDato,               # Tipo de dato de genes
        PobElite=pPobElite,               # Cantidad de individuos de la élite
        FunAptitud=AptitudColorGrafo      # Función de aptitud implementado externamente
    )

    Solucion, Costo = AG.Ejecutar()
    return AG, Solucion, Costo

#--------------------------------------------------------------------------------------------------------------------------------

# Ejecutar AG para ensamblaje de Genoma
def agTSPadn(pArchivoDISTANCIAcsv, pIteraciones, pGeneraciones, pPoblacion, pProbMutacion, pTipoMutacion, 
           pTipoCruce, pGenUnico, pInicioFijo, pInicioFinFijo, pN, pPobElite):
    
    global Distancia
    Distancia = LeerDISTANCIAcsv(pArchivoDISTANCIAcsv)
    AG = AlgoritmoGenetico(
        Iteraciones=pIteraciones,         # Cantidad de iteraciones del AG
        Generaciones=pGeneraciones,       # Cantidad de generaciones del AG
        Poblacion=pPoblacion,             # Cantidad de población
        ProbMutacion=pProbMutacion,       # Probabilidad de mutación
        TipoMutacion=pTipoMutacion,       # Tipo de mutación ['Permuta', 'UnPunto']
        TipoCruce=pTipoCruce,             # Tipo de cruce ['Complemento', 'UnPunto']
        GenUnico=pGenUnico,               # True: Los genes no usan valores repetidos
        InicioFijo=pInicioFijo,           # True: El 1er gene siempre es '0'
        InicioFinFijo=pInicioFinFijo,     # True: El 1er gen = '0'; ultimo gen = 'N-1'
        N=pN,                             # Cantidad de ciudades
        PobElite=pPobElite,               # Cantidad de individuos de la élite
        FunAptitud=AptitudTSP             # Función de aptitud implementado externamente
    )

    Solucion, Costo = AG.Ejecutar()
    return AG, Solucion, Costo

#--------------------------------------------------------------------------------------------------------------------------------
# FIN
#--------------------------------------------------------------------------------------------------------------------------------
