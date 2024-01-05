import gzip #modulo de tratamiento de archivos .gz
import pandas as pd #pandas para trabajar sobre DataFrames
import matplotlib.pyplot as plt #herramienta de ploteo para python
import seaborn as sns #sofisticacion de plt
import json
import os
import ast
import re
from datetime import datetime
from textblob import TextBlob

# funcion de descompresion

def gz_a_DataFrame(ruta): #como input tenemos la ruta del archivo a descomprimir
    try: #probamos normalmente

        with gzip.open(ruta,'rt') as file: #descomprimiendo los archivos    
            datos = [json.loads(linea) for linea in file.readlines()] #leemos cada linea en formato json y lo guardamos en una lista "datos"
        
        df = pd.DataFrame(datos) #pasamos la lista a DataFrames
        
        return df #devolvemos el dataframe
    
    except UnicodeDecodeError: #como tenemos dos jsons con comillas simples, tenemos que adaptar la funcion si tiene error

        filas_items = [] #lista vacia
        with gzip.open(ruta) as file: #leemos el archivo
            for line in file.readlines(): #navegamos por linea
                cadena_texto = line.decode('utf-8') #decodificamos con utf-8
                filas_items.append(ast.literal_eval(cadena_texto)) #leemos el valor literal del diccionario con sintaxis python

        df = pd.DataFrame(filas_items) # a dataframe

        return df #devolvemos el dataframe
    
# funcion de obtencion de nombres de archivos iniciales y finales
    
def get_names(ruta): #como input la ruta A LA CARPETA
    lista_inicial = os.listdir(ruta) #listemos las direcciones
    lista_limpia = [] #inicializamos lista de nombres actuales
    lista_final = [] #inicializamos lista de nombres parquet
    nombres = []
    for i in lista_inicial:
        if '.json.gz' in i: #si es .json.gz
            lista_limpia.append('Datasets/'+i) #llenamos la lista con el nombre de carpeta al inicio
            lista_final.append('Datasets/parquet/'+i.replace('.json.gz','.parquet')) #llenamos la lista final con el cambio a csv
            nombres.append(i.replace('.json.gz',''))
  
    nom = dict(zip(nombres,list(zip(lista_limpia,lista_final))))
    return nom #output

def tipo_datos(df): #verifica el tipo de datos y devuelve todos los tipos de datos por cada columna y nulos
    dic = {'Columna': [], 'Tipo_datos': [], '%_nulos': [], 'Nulos': []}
    for column in df.columns: #itera sobre columnas
        tipos_de_datos = df[column].apply(lambda x: type(x).__name__).unique() #nos devuelve sobre la columna los tipos de datos sin repeticion
        isnap = df[column].isna().sum()/df[column].count()*100 # calcula el porcentaje de nans 
        isna = df[column].isna().sum() #calcula la cantidad de nans
        dic['Columna'].append(column) # adjunta datos
        dic['Tipo_datos'].append(tipos_de_datos)
        dic['%_nulos'].append(isnap)
        dic['Nulos'].append(isna)
    
    datf = pd.DataFrame(dic) #genera dataframe para devolver

    return datf

def col_price(valor): #arreglar la columna price, que tiene str y valores
    if isinstance(valor,str): #verifica que sea una string
        numeros_encontrados = re.findall(r'\d+', valor) #extrae todos los numeros de la cadena

    if isinstance(valor, float): # si el valor es float
        if pd.isna(valor): #si es nan
            return 0.0 #devuelve 0
        else:
            return valor #si no es nan devuelve el valor float inicial
    elif numeros_encontrados: # si no es float devuelve el float del primer numero encontrado
        return float(numeros_encontrados[0])
    else: # si no encuentra numeros devuelve 0
        return 0.0

def release(valor): # devuelve el anio de lanzamiento segun la fecha, limpiando las strings
    try: 
        fecha_objeto = datetime.strptime(valor, '%Y-%m-%d') # intenta pasar el valor a fecha con el formato mas comun
        return fecha_objeto.year #devuelve el anio
    except:
        return 0 #si encuentra un error con el formato, devuelve 0

def indentificar_duplicados(df,columna): #identifica los duplicados y los muestra
    duplicados = df[df.duplicated(subset=columna,keep=False)]
    return duplicados

def sentimientos(valor): #analisis de sentimientos usando Textblob, simple pero eficaz.
    if valor is None: # si no ha review, el valor es 1
        return 1
    analisis = TextBlob(str(valor)) # genera un objeto text blob
    polarizacion = analisis.sentiment.polarity # analiza la polarizacion segun la libreria
    if polarizacion <= -0.2: # tipicos valores de polarizacion negativa, dando un margen para el neutro equidistante entre positivo y negativo
        return 0
    elif polarizacion >= 0.2:
        return 2
    else:
        return 1
    