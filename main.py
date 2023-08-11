import traceback
import os
import sys

import Funciones as fn

from formArchivos import *
from SistemaArchivos import InfoArchivo
##from EntidadesModulo import Persona

class FrmUsuario(QtWidgets.QDialog):
    
    
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.objPersona = None

        self.ui.setupUi(self)
        self.inicializarControles() #se inicia con una condicion
        
        #iniciar botones con acciones
        self.ui.btn_Crear.clicked.connect(self.guardarArch)
        self.ui.btn_Buscar.clicked.connect(self.buscarArch)
        self.ui.tw_Mostrar.clicked.connect(self.seleccionarArchivo)
        self.ui.tw_Mostrar.clicked.connect(self.cargarArchivo)
        self.ui.btn_Eliminar.clicked.connect(self.eliminarArchivo)
        self.ui.btn_Modificar.clicked.connect(self.modificarArchivo)
        
    #incializa lo nesecesario 
    def inicializarControles(self):
        self.ui.NombreArchivo.clear()
        self.ui.DireccionCarpeta_2.clear()
        self.ui.NombreBuscar.clear()
        self.ui.RutaBuscar.clear()
        self.ui.Formatos.setCurrentIndex(0) 

#########################################################################################
    #Crea el archivo
    def guardarArch(self):
        nombreArch= self.ui.NombreArchivo.text()
        ruta = self.ui.DireccionCarpeta_2.text()
        formato = self.ui.Formatos.currentText()
        
        
        if nombreArch == "": 
            print("campo vacio")
            msg = QtWidgets.QMessageBox(self)  
            msg.setIcon(QtWidgets.QMessageBox.Icon.Warning)      
            msg.setText("El nombre del archivo se encuentra vacio")        
            msg.setWindowTitle("Validacion de campos vacios")        
            msg.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)        
            a = msg.exec()
         
                 
        #Verifica la ruta para guardar en una ruta específica o en la default
        else:
            
            try:
                if (ruta == ''):
                    archivo = open(nombreArch+formato,'a') #no agremos direccion para que se cree donde esta el proyexto   
                    archivo.write(self.ui.txtEscribir.toPlainText()+"\r")  ##lo dejmaos en limpio  
                    archivo.close()
                    self.ui.NombreArchivo.clear()
                    self.ui.txtEscribir.clear()
                else:
                    print("ESTA ES LA RUTA :: =====",ruta)  #C:\Users\AlemanKMS\Documents\Proyecto_Grupo9
                    
                    add= ruta.replace("\\", "\\\\")
                    print (add)

                    archivo = open(os.path.join(add,nombreArch+formato),'a')#no agremos direccion para que se cree donde esta el proyexto   
                    archivo.write("")  ##lo dejmaos en limpio  
                    archivo.close()
                    self.ui.NombreArchivo.clear()
                    
                msg = QtWidgets.QMessageBox(self)  
                msg.setIcon(QtWidgets.QMessageBox.Icon.Warning)      
                msg.setText("El archivo se ha creado exitosamente")        
                msg.setWindowTitle("Archivo Creado")        
                msg.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)        
                a = msg.exec()
                
            except OSError as oE:
                archivo.close()
                print(oE.strerror)
            except BaseException:
                print(traceback.format_exc())
                archivo.close()     
       

        self.inicializarControles() 

#########################################################################################
    #Buscar Archivo
    def buscarArch(self):
        self.limpiarTabla()
        nombreArch= self.ui.NombreBuscar.text()
        ruta = self.ui.RutaBuscar.text()
        lambda:self.ui.tw_Mostrar.setShowGrid(False).clear()
        self.fila = self.ui.tw_Mostrar.rowCount()
        
        
        if (nombreArch):
            if(nombreArch != ''):
                if(ruta == ''):
                    fn.recorrer_directorios(os.getcwd())
                else:
                    fn.recorrer_directorios(ruta) 
            else:
                msg = QtWidgets.QMessageBox(self)  
                msg.setIcon(QtWidgets.QMessageBox.Icon.Warning)      
                msg.setText("Ingrese el nombre del archivo")        
                msg.setWindowTitle("Validacion de campos vacios")        
                msg.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)        
                a = msg.exec()
        listaArchivosEncontrados = fn.buscarArchivoFilter(nombreArch)                    
        if len(listaArchivosEncontrados) > 0:
            etiqueta = "El archivo {0} se encuentra en la ruta {1}"
            for archivo in listaArchivosEncontrados:
                self.ui.tw_Mostrar.insertRow(self.fila)
                celdaArchivo = QtWidgets.QTableWidgetItem(archivo.NomArchivo)
                celdaRuta = QtWidgets.QTableWidgetItem(archivo.Ruta)
                print(etiqueta.format(archivo.NomArchivo,archivo.Ruta))
                self.ui.tw_Mostrar.setItem(self.fila,0,celdaArchivo)
                self.ui.tw_Mostrar.setItem(self.fila,1,celdaRuta)
                
        self.inicializarControles()

#########################################################################################
    #Elimina una fila y documento
    def eliminarFila(self):
        filaSeleccionada = self.tabla.selectedItems()

        if filaSeleccionada:
            fila = filaSeleccionada[0].row()
            self.ui.tw_Mostrar.removeRow(fila)

            self.ui.tw_Mostrar.clearSelection()

#########################################################################################
    #Limpia la tabla para volver a ingresar datos       
    def limpiarTabla(self):
        self.ui.tw_Mostrar.clearContents()
        self.ui.tw_Mostrar.setRowCount(0)

#########################################################################################

    #Modificar un archivo
    def  seleccionarArchivo(self):
        posicion = self.ui.tw_Mostrar.selectedItems ()
        return posicion 
        
        
    def cargarArchivo(self):
        posicion = self.ui.tw_Mostrar.selectedItems ()
        fila = posicion[0].row()
        
        nombreArch = self.ui.tw_Mostrar.item(fila,0)
        self.ui.NombreArchivo.setText(nombreArch.text())
        
        nombreRuta = self.ui.tw_Mostrar.item(fila,1)
        self.ui.DireccionCarpeta_2.setText(nombreRuta.text())    
        
    def eliminarArchivo(self):
        filaSelect = self.seleccionarArchivo()
        fila = filaSelect[0].row()
        
        if filaSelect:        
            self.ui.tw_Mostrar.removeRow(fila)
            self.fila -=1
            self.msgProceso()
        else:
            msg = QtWidgets.QMessageBox(self)
            msg.setIcon(QtWidgets.QMessageBox.Icon.Critical)
            msg.setWindowTitle("Eliminar Fila")
            msg.setText("Seleccione una fila. ")
            msg.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
            msg.exec()
        self.inicializarControles()
        
    def modificarArchivo(self):
        filaSelect = self.seleccionarArchivo()
        fila = filaSelect[0].row()
        
        nombreArch = self.ui.NombreArchivo_2.text()
        ruta = self.ui.DireccionCarpeta_2.text()
       
        self.objPersona = None      
        celdaArchivo = QtWidgets.QTableWidgetItem(nombreArch)
        celdaRuta = QtWidgets.QTableWidgetItem(ruta)
        self.ui.tw_Mostrar.setItem(fila,0,celdaArchivo)
        self.ui.tw_Mostrar.setItem(fila,1,celdaRuta)

        self.msgProceso()
        self.inicializarControles()
        
        
    def EscribirFile(self):
        try:
            
            archivo = open(os.path.join(self.ui_path,"ClienteTs.txt"),'a') #append       
            archivo.write(self.textEscribir.toPlainText()+"\r")
            archivo.close()
            self.textEscribir.clear()
            
        except OSError as oE:
            archivo.close()
            print(oE.strerror)
        except BaseException:
            print(traceback.format_exc())
            archivo.close()
    
    def LecturaArchivo(self):
        try:
            archivo = open(os.path.join(self.ui_path,),'r')        
            texto = archivo.read()                        
            self.textLeer.setPlainText(texto)
            archivo.close()
            #print(archivo.read()) 
        except OSError as oE:
            archivo.close()
            print(oE.strerror)
        except BaseException:
            archivo.close()   
            
    def LecturaXLinea(self):
        try:
            archivo = open(os.path.join(self.ui_path,"ClienteTs.txt"),'r')
            # Leer la primera línea del archivo
            linea = archivo.readline()

            # Iterar hasta que la línea leída sea vacía (indicando el final del archivo)
            textoImprimir = ""
            while linea:
                textoImprimir += linea
                # Leer la siguiente línea
                linea = archivo.readline()
                
            self.textLeer.setPlainText(textoImprimir)

        except OSError as oE:
            archivo.close()
            print(oE.strerror)
        except BaseException:
            archivo.close()

    
    
     
   
#########################################################################################
    #Mensaje de decisión al escribir
    def msgProceso(self):        
        msg = QtWidgets.QMessageBox(self)
        msg.setIcon(QtWidgets.QMessageBox.Icon.Information)
        msg.setWindowTitle("Ejecución de proceso")        
        msg.setText("  Proceso Existoso ")
        msg.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
        msg.exec() 
 
    
    

        

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)    
    myapp = FrmUsuario()        
    myapp.show()
    sys.exit(app.exec())
    