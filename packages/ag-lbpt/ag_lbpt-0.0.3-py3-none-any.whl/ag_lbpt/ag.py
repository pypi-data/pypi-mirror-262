# -*- coding: utf-8 -*-

""" Algoritmo Genético 

Versión   : 1.5
Autor     : Luis Beltran Palma Ttito
Lugar     : Cusco, Perú, 2024.
Proposito : Algoritmos Genético 

"""

import random
import math
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
import folium

#-------------------------------------------------------------------------------------------------------------------------------------

class AlgoritmoGenetico:
    """ Resumen de la clase.
    Args:
    ----------
        Iteraciones : int
            Número de iteraciones que repite la ejecución del algoritmo genético, almacenando la mejor solución.
        Generaciones : int
            Número de generaciones que itera el algoritmo genético.
        Poblacion : int
            Cantidad de individuos de la población.
        ProbMutacion :float
            Probabilidad de mutacion [0 ... 1].
        TipoMutacion : category
            'UnPunto' Mutación en 1 atributo; 'Permuta' Mutación swap o permutación (entre 2 atributos).
        TipoCruce : category
            'Complemento' asigna del primer ancestro los primeros atributos, y el restante
            complementa con genes faltantes en el orden que esten en el segundo ancestro,
            Si TipoCruce = 'Complemento', GenUnico debe ser siempre True.
            'UnPunto' Crea un cruce en un atributo.
        GenUnico : boolean
            True Los valores de los genes son únicos (sin repetidos); False lo contrario.
        InicioFijo : boolean
            True El primer gen siempre es '1', InicioFinFijo debe falso.
        InicioFinFijo : boolean
            True El primer gen siempre es '1', el ultimo siempre es 'N'. InicioFijo debe falso.
        N :int
            Cantidad de genes del cromosoma.
        PobElite :int
            Cantidad de individuos de la élite (valores pequeños [1 ... 5]).
        MinCromosoma : list[int/float]
            Mínimo valor de los genes del cromosoma, unicamente si GenUnico=False.
        MaxCromosoma : list[int/float]
            Máximo valor de los genes del cromosoma, unicamente si GenUnico=False.
        TipoDato : list[category]
            Tipo de dato de los genes del cromosoma, 'int' número entero; 'float' número real.
        FunAptitud : def
            Función heurística, que recibe siempre un cromosoma y retorna el costo de la solución.
    """
    #-------------------------------------------------------------------------------------------------------------------------------------

    def __init__(self, Iteraciones = 10, Generaciones = 100, Poblacion = 250,
                 ProbMutacion = 0.05, TipoMutacion = 'UnPunto', GenUnico = True,
                 N = 10, PobElite = 2, TipoCruce = 'Complemento',
                 InicioFijo=False, InicioFinFijo=False,
                 MinCromosoma = [0,0,0,0,0,0,0,0,0,0],
                 MaxCromosoma = [9,9,9,9,9,9,9,9,9,9],
                 TipoDato = ['int','int','int','int','int','int','int','int','int','int'],
                 FunAptitud = None):

        self.Iteraciones = Iteraciones          # Cantidad de iteraciones de todo el proceso, para encontrar el mejor
        self.Generaciones = Generaciones        # Cantidad de generaciones
        self.P = Poblacion                      # población
        self.ProbMutacion = ProbMutacion        # Probabilidad de mutación
        self.TipoMutacion = TipoMutacion        # Tipo de mutacion 'UnPunto', 'Permuta'
        self.TipoCruce = TipoCruce              # Tipo cruce: 'UnPunto', 'Complemento'
        self.PoElite = PobElite                 # Cantidad de individuos de la élite
        self.GenUnico = GenUnico                # Los genes tiene valores enteros sin repetidos y de GenUnico valores
        self.InicioFijo = InicioFijo            # True: La ruta siempre inicia y termina en el primer nodo '0'
        self.InicioFinFijo = InicioFinFijo      # True: La ruta siempre inicia y termina en el primer y ultimo nodo '0', 'N-1'
        self.N = N                              # Cantidad de nodos o ciudades
        self.MinCromosoma = MinCromosoma        # Mínimo valor del atributos de cromosoma
        self.MaxCromosoma = MaxCromosoma        # Maximo valor del atributo de cromosomas
        self.TipoDato = TipoDato                # Tipo de dato de cada atributo 'int', 'float'
        self.FunAptitud = FunAptitud            # Función de aptitud

        self.HistCosto = []                     # Historial de costo
        self.Ruta = []                          # Ruta solución
        self.Costo = 0.0                        # Costo de la ruta solucion

    #-------------------------------------------------------------------------------------------------------------------------------------

    # Muestra evolución de costo
    def GraficaCosto(self):
        plt.figure()
        plt.plot(self.HistCosto)
        plt.title('Evolución de costo')
        plt.grid(True)
        plt.show

    #-------------------------------------------------------------------------------------------------------------------------------------

    # Muestra evolución de costo de datos externos
    def GraficaCostoExterno(self, Historico):
        plt.figure()
        plt.plot(Historico)
        plt.title('Evolución de costo')
        plt.grid(True)
        plt.show

    #-------------------------------------------------------------------------------------------------------------------------------------

    # Grafica Ruta externa con TSP
    def GraficaRutaExternaTSP(self, TSP, Ruta):
        plt.figure()
        X = []
        Y = []
        for i in range(len(Ruta)):
            X.append(TSP[Ruta[i], 0])
            Y.append(TSP[Ruta[i], 1])
        plt.plot(X,Y,'-o')
        for i in range(len(Ruta)):
            plt.annotate(str(Ruta[i]), (X[i],Y[i]))
        plt.title("Ruta solución")
        plt.show()

    #-------------------------------------------------------------------------------------------------------------------------------------

    # Genera población inicial con P individuos
    def GeneraPoblacionInicial(self, P):
        self.Poblacion = []
        self.P = P
        for i in range(self.P):
            Cromosoma = []
            if (self.GenUnico == True): # Los genes no se repiten
                if (self.InicioFijo == True): # El primer gen siempre es '0'
                    Cromosoma = random.sample(list(range(1,self.N)),self.N-1)
                    Cromosoma.insert(0,0) # Colocar '0' al inicio
                elif (self.InicioFijo == False): # El primer es siempre es '0'
                    if (self.InicioFinFijo == True): # El primer gen es siempre es '0' y el ultimo 'N-1'
                        Cromosoma = random.sample(list(range(1,self.N-1)),self.N-2)
                        Cromosoma.insert(0,0) # Colocar '0' al inicio
                        Cromosoma.append(self.N-1) # Insertar 'N-1' al final
                    elif(self.InicioFinFijo == False): #
                        Cromosoma = random.sample(list(range(0,self.N)),self.N)
            elif (self.GenUnico == False): # Los genes se puede repetir o ser reales
                for k in range(self.N):
                    # Asumimos que son reales
                    Val = random.uniform(self.MinCromosoma[k], self.MaxCromosoma[k])
                    if (self.TipoDato[k] == 'int'):
                        Val = (random.sample(range(self.MinCromosoma[k], self.MaxCromosoma[k]+1),1))[0]
                    Cromosoma.append(Val)
            self.Poblacion.append([self.FunAptitud(Cromosoma),Cromosoma])
        return self.Poblacion

    #-------------------------------------------------------------------------------------------------------------------------------------

    # Seleccion de padre y madre por metodo de la ruleta
    def Seleccion(self):

        # ordenar población por el valor fitness
        self.Poblacion = sorted(self.Poblacion)

        # Hallar sumatoria de fitness para crear ruleta
        SumaF = 0
        for P in self.Poblacion:
            SumaF = SumaF + P[0]

        # Crea ruleta
        Ruleta = []
        SumaAcu = 0
        for Individuo in self.Poblacion:
            SumaAcu = SumaAcu + Individuo[0]/SumaF
            Ruleta.append([Individuo[0], Individuo[1], SumaAcu])

        # Seleccionar padre
        RandPadre = random.random()
        k = 0
        for k in Ruleta:
            if (k[2] >= RandPadre):
                break
        Padre = k

        # Selecciona madre
        RandMadre = random.random()
        for k in Ruleta:
            if (k[2] >= RandMadre):
                break
        Madre = k

        return Padre, Madre

    #-------------------------------------------------------------------------------------------------------------------------------------

    def Cruce(self, Padre, Madre):
        # Solo seleccionar el vector
        papa = Padre[1]
        mama = Madre[1]
        hijo1 = []
        hijo2 = []

        if (self.TipoCruce == 'Complemento'):

            # Generar punto de cruce al azar entre 1 y 8
            # El primer y ultimo siempre se quedan en su lugar
            # si InicioFijo o InicioFinFijo son TRUEs funciona ok
            r = random.randint(1, self.N - 2)

            # Crear hijo 1
            for k in range(r):
                hijo1.append(papa[k])
            for k in range(self.N):
                if (mama[k] not in hijo1):
                    hijo1.append(mama[k])
            # Crear hijo 2
            for k in range(r):
                hijo2.append(mama[k])
            for k in range(self.N):
                if (papa[k] not in hijo2):
                    hijo2.append(papa[k])
        elif (self.TipoCruce == 'UnPunto'):
            # Generar punto de cruce al azar
            r = random.randint(1, self.N - 2)

            # Crear hijo 1
            for k in range(r):
                hijo1.append(papa[k])
            for k in range(r, self.N):
                hijo1.append(mama[k])
            # Crear hijo 2
            for k in range(r):
                hijo2.append(mama[k])
            for k in range(r, self.N):
                hijo2.append(papa[k])

        return hijo1, hijo2

    #-------------------------------------------------------------------------------------------------------------------------------------

    # mutacion en un punto o permutación
    def Mutacion(self, Hijo, Prob):
        if (self.TipoMutacion == 'Permuta'):
            hijo = Hijo.copy()
            r1 = 0
            r2 = 0
            if (random.random() <= Prob):
                #Determinar puntos de mutación
                r1 = 1
                r2 = 1
                if (self.InicioFijo == True):
                    r1 = random.randint(1, self.N-1)
                    r2 = random.randint(1, self.N-1)
                elif (self.InicioFijo == False):
                    if (self.InicioFinFijo == True):
                        r1 = random.randint(1, self.N-2)
                        r2 = random.randint(1, self.N-2)
                    elif (self.InicioFinFijo == False):
                        r1 = random.randint(0, self.N-1)
                        r2 = random.randint(0, self.N-1)
                Aux = hijo[r1]
                hijo[r1] = hijo[r2]
                hijo[r2] = Aux
            return hijo
        elif (self.TipoMutacion == 'UnPunto'):
            hijo = Hijo.copy()
            r = 0
            if (random.random() <= Prob):
                r = random.randint(0, self.N-1)
                Val = random.uniform(self.MinCromosoma[r], self.MaxCromosoma[r])
                if (self.TipoDato[r] == 'int'):
                    Val = (random.sample(range(self.MinCromosoma[r], self.MaxCromosoma[r]+1),1))[0]
                hijo[r] = Val
            return hijo

    #-------------------------------------------------------------------------------------------------------------------------------------

    # Seleccionar N individuos de la elite
    def Elite(self, N):
        # ordenar población por el valor fitnnes
        self.Poblacion = sorted(self.Poblacion)
        PoblacionElite = []
        for k in range(N):
            PoblacionElite.append(self.Poblacion[k])
        return PoblacionElite

    #-------------------------------------------------------------------------------------------------------------------------------------

    def Ejecutar(self):

        # Inicializar variables que registen lo mejor
        MejorCosto = 10000000000 #Iniciar con un valor muy alto (muy costoso)
        MejorRuta = []
        MejorHistorico = []
        for k in range(self.Iteraciones):
            # Inicializar poblacion inicial con P individuos
            self.Poblacion = self.GeneraPoblacionInicial(self.P)
            # Guardar costo de la población inicial
            self.HistCosto = []
            self.Poblacion = sorted(self.Poblacion)
            Mejor = self.Poblacion[0]
            self.HistCosto.append(Mejor[0])

            # repetir por generaciones
            for k in range(self.Generaciones):
                NuevaPoblacion = []
                # Obtener indididuos de la elite
                Pe = self.Elite(self.PoElite)

                # obtener padre y madre por la mitad de la población y generar hijo1 e hijo2
                for i in range(self.P // 2):
                    Padre, Madre = self.Seleccion()
                    Hijo1, Hijo2 = self.Cruce(Padre, Madre)
                    Hijo1 = self.Mutacion(Hijo1, self.ProbMutacion)
                    Hijo2 = self.Mutacion(Hijo2, self.ProbMutacion)
                    NuevaPoblacion.append([self.FunAptitud(Hijo1), Hijo1])
                    NuevaPoblacion.append([self.FunAptitud(Hijo2), Hijo2])

                # Reemplazar a la población actual
                self.Poblacion = NuevaPoblacion

                # adicionar los individuos de la elite
                for p in Pe:
                    self.Poblacion.append(p)

                # Elegir el mejor individuo de la población
                self.Poblacion = sorted(self.Poblacion)
                Mejor = self.Poblacion[0]
                self.HistCosto.append(Mejor[0])

                self.Costo = Mejor[0]
                self.Ruta = Mejor[1]

            # Actualizar si se encuentra un mejor costo
            if(self.Costo < MejorCosto):
                MejorCosto = self.Costo
                MejorRuta = self.Ruta
                MejorHistorico = self.HistCosto

            # Al final almacenar el la clase AG los mejores
            self.Costo = MejorCosto
            self.Ruta = MejorRuta
            self.HistCosto = MejorHistorico

        return self.Ruta, self.Costo

#-------------------------------------------------------------------------------------------------------------------------------------
