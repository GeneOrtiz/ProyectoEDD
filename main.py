import traceback
import os
import sys


import Funciones as fn

from os import remove
from formArchivos import *
from SistemaArchivos import InfoArchivo
from VentanaProteger import *

nomRuta = ""
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
        self.ui.btn_Proteger.clicked.connect(self.protegerArchivo)
        
    #incializa lo nesecesario 
    def inicializarControles(self):
        self.ui.NombreArchivo.clear()
        self.ui.DireccionCarpeta.clear()
        self.ui.NombreBuscar.clear()
        self.ui.RutaBuscar.clear()
        self.ui.txtEscribir.clear()
        self.ui.txt_clave.clear()
        

#########################################################################################
    #Crea el archivo
    def guardarArch(self):
        nombreArch= self.ui.NombreArchivo.text()
        ruta = self.ui.DireccionCarpeta.text()
        formato = self.ui.Formato.text()
        
        
        
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

                    archivo = open(os.path.join(add,nombreArch+formato),'w')#no agremos direccion para que se cree donde esta el proyexto   
                    archivo.write(self.ui.txtEscribir.toPlainText()+"\r")  ##lo dejmaos en limpio  
                    archivo.close()
                    self.ui.NombreArchivo.clear()
                    self.ui.txtEscribir.clear()
                    
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
        filaSeleccionada = self.ui.tw_Mostrar.selectedItems()

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
        
#########################################################################################        
    def cargarArchivo(self):
        posicion = self.ui.tw_Mostrar.selectedItems ()
        fila = posicion[0].row()
        formato = self.ui.Formato.text()
        nombreArch = self.ui.tw_Mostrar.item(fila,0)
        nombreRuta = self.ui.tw_Mostrar.item(fila,1)
        
        if (self.verificacion() == True):
            self.ui.NombreArchivo.setText(nombreArch.text())
            self.ui.DireccionCarpeta.setText(nombreRuta.text()) 
            
            archivo = open(nombreRuta.text(),"r")
            texto = archivo.read()
            self.ui.txtEscribir.setPlainText(texto)
            archivo.close()
        else:
            msg = QtWidgets.QMessageBox(self)  
            msg.setIcon(QtWidgets.QMessageBox.Icon.Warning)      
            msg.setText("Archivo bloqueado")        
            msg.setWindowTitle("Informativo")        
            msg.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)        
            a = msg.exec()
            
            self.limpiarTabla()
            self.inicializarControles() 
                   
#########################################################################################
#Elimina los archivos        
    def eliminarArchivo(self):
        filaSelect = self.seleccionarArchivo()
        fila = filaSelect[0].row()
        
        #convierto la ruta a txt
        nombreRuta = self.ui.tw_Mostrar.item(fila,1).text() 
       
        if filaSelect:        
            self.ui.tw_Mostrar.removeRow(fila)
            self.fila -=1
            remove(nombreRuta)
            self.msgProceso()
        else:
            msg = QtWidgets.QMessageBox(self)
            msg.setIcon(QtWidgets.QMessageBox.Icon.Critical)
            msg.setWindowTitle("Eliminar Fila")
            msg.setText("Seleccione una fila. ")
            msg.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
            msg.exec()
        self.inicializarControles()
        
#########################################################################################        
   
    def modificarArchivo(self):
        filaSelect = self.seleccionarArchivo()
        fila = filaSelect[0].row()
        formato = self.ui.Formato.text()
        
        nombreArch = self.ui.NombreArchivo.text()
        ruta = self.ui.DireccionCarpeta.text()
 
        archivo = open(ruta,nombreArch + formato,"a")
        texto = archivo.write(self.ui.txtEscribir.toPlainText() + "\r")
        archivo.close()
        self.ui.txtEscribir.clear()
        
        
        self.msgProceso()
        self.inicializarControles()
        
        
##################################################################################################################
#Proteger Archivos
    def protegerArchivo(self):
        nombreArch= self.ui.NombreArchivo.text()
        ruta = self.ui.DireccionCarpeta.text()
        clave = self.ui.txt_clave.text()
        
        
        
        if nombreArch == "" or ruta == "" or clave == "": 
            print("campo vacio")
            msg = QtWidgets.QMessageBox(self)  
            msg.setIcon(QtWidgets.QMessageBox.Icon.Warning)      
            msg.setText("Un campo se encuentra vacio")        
            msg.setWindowTitle("Validacion de campos vacios")        
            msg.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)        
            a = msg.exec()
            
        else: 
            msg = QtWidgets.QMessageBox(self)  
            msg.setIcon(QtWidgets.QMessageBox.Icon.Question)      
            msg.setText("Proteger archivo? ")        
            msg.setWindowTitle("Confirmación ")        
            msg.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)  
            boton_si = msg.button(QtWidgets.QMessageBox.StandardButton.Yes)
            boton_no = msg.button(QtWidgets.QMessageBox.StandardButton.No)
            a = msg.exec()
            
            if msg.clickedButton() == boton_si:
                archivo = open("C:\Archivos\Contrasenas.txt",'a') #no agremos direccion para que se cree donde esta el proyexto   
                archivo.write( self.ui.DireccionCarpeta.text() + ',' +self.ui.txt_clave.text( ) + "\r")  
                archivo.close()
                self.limpiarTabla()
                self.inicializarControles()
            else :   
                self.close()
  
##########################################################################################################

       
        
    def verificacion (self):
        filaSelect = self.seleccionarArchivo()
        fila = filaSelect[0].row()
        nombreRuta = self.ui.tw_Mostrar.item(fila,1).text()
        
        archivo = open("C:\Archivos\Contrasenas.txt", "r")
        linea = archivo.readlines()
        
        if linea == []:
            return True
        else:
            for i in linea:
                rut, password = i.strip().split(',')
                print (rut + " " + nombreRuta)
                if (nombreRuta == rut ):
                    ventana = VentanaProteger(nombreRuta)
                    ventana.exec()
                    
                    if (ventana.desbloquear == True):
                        return True
                    else:
                        return False
                else: 
                    return True
             
        archivo.close()
        
             
        
        

    

##########################################################################################################            
   # Reporte de inventario de documentos y rutas 
    def generar_reporte(documentos):
        try:
            archivo_informe = open("informe_inventario.txt", "w")
            archivo_informe.write("Informe de inventario \n\n")
            
            for documento in documentos:
                nombre, ruta = documento
                archivo_informe.write(f"Nombre del Documento: {nombre}\n")
                archivo_informe.write(f"Ruta del Documento: {ruta}\n\n")
                
            archivo_informe.close()
            print("Informe de inventario generado exitosamente")
        
        except Exception  as e:
            print("Ocurrio un error al generar el informe de inventario ", str(e))

    
    
     
   
#########################################################################################
    #Mensaje de decisión al escribir
    def msgProceso(self):        
        msg = QtWidgets.QMessageBox(self)
        msg.setIcon(QtWidgets.QMessageBox.Icon.Information)
        msg.setWindowTitle("Ejecución de proceso")        
        msg.setText("  Proceso Existoso ")
        msg.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
        msg.exec() 
 
###########################################################################################    

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)    
    myapp = FrmUsuario()        
    myapp.show()
    sys.exit(app.exec())
    