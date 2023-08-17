import os
from SistemaArchivos import InfoArchivo

listaRutaArchivo = []

def obtener_nombre_archivo(ruta):
    nombre_archivo_con_extension = os.path.basename(ruta)
    nombre_archivo, extension = os.path.splitext(nombre_archivo_con_extension)
    return nombre_archivo

def recorrer_directorios(ruta):
    try:
        # Lista los contenidos del directorio
        contenidos = os.listdir(ruta) 

        for contenido in contenidos:
            
            ruta_completa = os.path.join(ruta, contenido)

            if os.path.isdir(ruta_completa): # Si es un directorio, recurrir de manera recursiva
                recorrer_directorios(ruta_completa)
            else:
                # Si es un archivo, puedes realizar alguna acción con él
                nombreArchivo = obtener_nombre_archivo(ruta_completa)
                oFile = InfoArchivo(ruta_completa,nombreArchivo)
                listaRutaArchivo.append(oFile)               
   
    except Exception as e:
        print(f"Error al acceder a: {ruta}. Error: {e}")


def buscarArchivoFilter(nombreArchivo):
    return list(filter(lambda objeto : objeto.NomArchivo == nombreArchivo,listaRutaArchivo))


def obtener_nombre_archivo2(ruta):
    nombre_archivo_con_extension = os.path.basename(ruta)    
    return nombre_archivo_con_extension

def recorrer_directorios2(ruta):
    try:
        # Lista los contenidos del directorio
        contenidos = os.listdir(ruta)

        for contenido in contenidos:
            
            ruta_completa = os.path.join(ruta, contenido)

            if os.path.isdir(ruta_completa): # Si es un directorio, recurrir de manera recursiva
                recorrer_directorios2(ruta_completa)
            else:
                # Si es un archivo, puedes realizar alguna acción con él
                nombreArchivo = obtener_nombre_archivo2(ruta_completa)
                oFile = InfoArchivo(ruta_completa,nombreArchivo)
                listaRutaArchivo.append(oFile)               
   
    except Exception as e:
        print(f"Error al acceder a: {ruta}. Error: {e}")


