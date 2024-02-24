#!/bin/env python3

import os
import shutil
from random import sample

def dividir_archivos(directorio_origen, directorio_destino_1, directorio_destino_2, k):
    # Lista para almacenar los nombres de los archivos (sin extensión)
    archivos_txt = [os.path.splitext(archivo)[0] for archivo in os.listdir(directorio_origen) if archivo.endswith('.txt')]
    
    # Calcular la cantidad de archivos a copiar a cada directorio
    cantidad_k = int(len(archivos_txt) * (k / 100))
    
    # Seleccionar archivos aleatorios para cada conjunto
    seleccion_k = set(sample(archivos_txt, cantidad_k))
    seleccion_restante = set(archivos_txt) - seleccion_k
    
    # Función para copiar archivos
    def copiar_archivos(seleccion, directorio_destino):
        for nombre in seleccion:
            for extension in ['.txt', '.png']:
                archivo_origen = os.path.join(directorio_origen, nombre + extension)
                archivo_destino = os.path.join(directorio_destino, nombre + extension)
                if os.path.exists(archivo_origen):
                    shutil.copy(archivo_origen, archivo_destino)
    
    # Copiar los archivos seleccionados a los directorios destino
    copiar_archivos(seleccion_k, directorio_destino_1)
    copiar_archivos(seleccion_restante, directorio_destino_2)

#-------------------------------------------------------------------------------
def vaciar_directorio(directorio):
    for nombre in os.listdir(directorio):
        ruta_completa = os.path.join(directorio, nombre)
        try:
            if os.path.isfile(ruta_completa) or os.path.islink(ruta_completa):
                os.remove(ruta_completa)  # Eliminar archivos y enlaces
            elif os.path.isdir(ruta_completa):
                shutil.rmtree(ruta_completa)  # Eliminar directorios
        except Exception as e:
            print(f'Error al eliminar {ruta_completa}. Razón: {e}')
            
#===============================================================================
if __name__=="__main__":

   import os;
   
   SOURCE="../data"
   TARGET="../tmp"

   # Configuración de los directorios y el porcentaje k
   directorio_origen = os.path.join(SOURCE);
   directorio_train  = os.path.join(TARGET,"train");
   directorio_test   = os.path.join(TARGET,"test");
   
   os.makedirs(directorio_train, exist_ok=True);
   os.makedirs(directorio_test,  exist_ok=True);
   
   vaciar_directorio(directorio_train);
   vaciar_directorio(directorio_test );
   
   k = 80 

   dividir_archivos(directorio_origen, directorio_train, directorio_test, k);
   
