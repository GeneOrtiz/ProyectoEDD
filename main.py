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
        self.ui.btn_Reporte.clicked.connect(self.generar_reporte)
        
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
        formato = '.txt'
        
 
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
                    add= ruta.replace("\\", "\\\\")

                    archivo = open(os.path.join(add,nombreArch+formato),'a')#no agremos direccion para que se cree donde esta el proyexto   
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
            for archivo in listaArchivosEncontrados:
                self.ui.tw_Mostrar.insertRow(self.fila)
                celdaArchivo = QtWidgets.QTableWidgetItem(archivo.NomArchivo)
                celdaRuta = QtWidgets.QTableWidgetItem(archivo.Ruta)
                self.ui.tw_Mostrar.setItem(self.fila,0,celdaArchivo)
                self.ui.tw_Mostrar.setItem(self.fila,1,celdaRuta)
        else:
            msg = QtWidgets.QMessageBox(self)  
            msg.setIcon(QtWidgets.QMessageBox.Icon.Warning)      
            msg.setText("Archivo no encongrado")        
            msg.setWindowTitle("Informativo")        
            msg.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)        
            a = msg.exec()
        
        #Para que no se repita el archivo
        fn.listaRutaArchivo = []   
        self.inicializarControles()         

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
#Carga la información de los archivos a la Imterfaz gráfica    
    def cargarArchivo(self):
        posicion = self.ui.tw_Mostrar.selectedItems ()
        fila = posicion[0].row()
        nombreArch = self.ui.tw_Mostrar.item(fila,0)
        ruta = self.ui.tw_Mostrar.item(fila,1)
        
        #Verifica si el archivo esta bloqueado sino lo abre, si esta blqueado se confirma la clave
        if (self.verificacion() == True):
            self.ui.NombreArchivo.setText(nombreArch.text())
            self.ui.DireccionCarpeta.setText(ruta.text()) 
            
            archivo = open(ruta.text(),"r")
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
        ruta = self.ui.tw_Mostrar.item(fila,1).text() 
       
        if filaSelect: 
            msg = QtWidgets.QMessageBox(self)  
            msg.setIcon(QtWidgets.QMessageBox.Icon.Question)      
            msg.setText("¿Desea eliminar el archivo?")        
            msg.setWindowTitle("Confirmación ")        
            msg.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)  
            boton_si = msg.button(QtWidgets.QMessageBox.StandardButton.Yes)
            
            a = msg.exec()
            
            #Realiza la eliminación del archivo    
            if msg.clickedButton() == boton_si:       
                self.ui.tw_Mostrar.removeRow(fila)
                self.fila -=1
                remove(ruta)
                self.msgProceso()
                msg = QtWidgets.QMessageBox(self)  
                msg.setIcon(QtWidgets.QMessageBox.Icon.Warning)      
                msg.setText("El archivo se ha eliminado exitosamente")        
                msg.setWindowTitle("Archivo Creado")        
                msg.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)        
                a = msg.exec()
        else:
            msg = QtWidgets.QMessageBox(self)
            msg.setIcon(QtWidgets.QMessageBox.Icon.Warning)
            msg.setWindowTitle("Eliminar Fila")
            msg.setText("Seleccione una fila. ")
            msg.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
            msg.exec()
            
        self.limpiarTabla()    
        self.inicializarControles()
        
#########################################################################################        
#Modifica los archivos    
    def modificarArchivo(self):
        filaSelect = self.seleccionarArchivo()
        fila = filaSelect[0].row()
        
        #Confirma el cambio
        ruta = self.ui.DireccionCarpeta.text()
        msg = QtWidgets.QMessageBox(self)  
        msg.setIcon(QtWidgets.QMessageBox.Icon.Question)      
        msg.setText("¿Desea modificar el archivo?")        
        msg.setWindowTitle("Confirmación ")        
        msg.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)  
        boton_si = msg.button(QtWidgets.QMessageBox.StandardButton.Yes)
        
        a = msg.exec()
        
        #Realiza la modificación del archivo    
        if msg.clickedButton() == boton_si:
            archivo = open(ruta,"w")
            archivo.write(self.ui.txtEscribir.toPlainText())
            archivo.close()
            self.ui.txtEscribir.clear()
        else:
            msg.close()
        
        self.msgProceso()
        self.limpiarTabla()
        self.inicializarControles()
        
        
##################################################################################################################
#Proteger Archivos
    def protegerArchivo(self):
        nombreArch= self.ui.NombreArchivo.text()
        ruta = self.ui.DireccionCarpeta.text()
        clave = self.ui.txt_clave.text()
        #Si hay un campo el blanco
        if nombreArch == "" or ruta == "" or clave == "": 
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
            
            a = msg.exec()
            archivo = open("C:\Archivos\Contrasenas.txt",'r')  
            linea = archivo.readlines()
            
            #Realiza la protección del archivo
            if msg.clickedButton() == boton_si:
                for i in linea:
                    rut, password = i.strip().split(',')
                    #Verifica si el archivo esta bloqueado, si es asi realiza la solicitud de contraseña
                    if (ruta == rut ):
                        msg = QtWidgets.QMessageBox(self)  
                        msg.setIcon(QtWidgets.QMessageBox.Icon.Warning)      
                        msg.setText("Error: El Archivo ya se encuentra protegido")        
                        msg.setWindowTitle("Información")        
                        msg.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)        
                        a = msg.exec()
                        
                    else:
                        archivo.close() 
                        archivo = open("C:\Archivos\Contrasenas.txt",'a')  
                        archivo.write( self.ui.DireccionCarpeta.text() + ',' +self.ui.txt_clave.text( ) + "\r")  
                    
                    
            else :   
                msg.close()
                
            archivo.close()   
            self.limpiarTabla()
            self.inicializarControles()
  
##########################################################################################################
#Verifica si el archivo esta protegido    
    def verificacion (self):
        filaSelect = self.seleccionarArchivo()
        fila = filaSelect[0].row()
        ruta = self.ui.tw_Mostrar.item(fila,1).text()
        nombreArch = self.ui.tw_Mostrar.item(fila,0).text()
        
        archivo = open("C:\Archivos\Contrasenas.txt", "r")
        linea = archivo.readlines()
        
        if linea == []:
            return True
        else:
            for i in linea:
                rut, password = i.strip().split(',')
                #Verifica si el archivo esta bloqueado, si es asi realiza la solicitud de contraseña
                if (ruta == rut ):
                    ventana = VentanaProteger(ruta, nombreArch)
                    ventana.exec()
                    
                    if (ventana.desbloquear == True):
                        return True
                    else:
                        return False
            archivo.close()     
            return True
             
            
 
##########################################################################################################            
   # Reporte de inventario de documentos y rutas 
    def generar_reporte(self):
        fn.listaRutaArchivo = []
        fn.recorrer_directorios2(os.getcwd())
        listaArchivosEncontrados = fn.listaRutaArchivo
        
        archivo_informe = open("C:\Archivos\informe_inventario.txt", 'w')
        archivo_informe.write("Informe de inventario"+ "\r" + "\r")
        
        if len(listaArchivosEncontrados) > 0:
            for archivo in listaArchivosEncontrados:
                nombreArchivo, extArchivo = os.path.splitext(archivo.NomArchivo)
                if extArchivo == '.txt':
                    archivo_informe.write("Documento: " + nombreArchivo + "\r" + "Ruta: " + archivo.Ruta + "\r" )

            

    
    
     
   
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
    