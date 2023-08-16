import traceback
import os
import sys

from formP import *



#Nueva ventana para colocar la contraseña y verificar si es la correcta 

class VentanaProteger(QtWidgets.QDialog):
    
    #Indica si las claves son correctas para desbloquerlo
    desbloquear = False

    def __init__(self,ruta):
        super().__init__()
        self.ui = Ui_ventana()
        self.objPersona = None
        self.ruta = ruta

        self.ui.setupUi(self)
        self.inicializarControles() #se inicia con una condicion
        
        self.ui.txt_Archivo.setText(self.ruta)  
        self.ui.btn_Aceptar.clicked.connect(self.verificar)
        self.ui.btn_cancelar.clicked.connect(self.cerrar)
        
        
    #incializa lo nesecesario 
    def inicializarControles(self):
        self.ui.txt_Contrasena.clear()
        self.ui.txt_Archivo.clear()
          
    #Verifica la ruta y la contraseña    
    def verificar(self):
        clave = self.ui.txt_Contrasena.text()

        archivo = open("C:\Archivos\Contrasenas.txt",'r')
        linea = archivo.readlines()   
        
        for i in linea:
            rut, password = i.strip().split(',')
            print (self.ruta + " " + clave)
            print (rut + " " + password)
            if (self.ruta == rut):
                if(clave == password):
                    self.desbloquear = True
                else:
                    msg = QtWidgets.QMessageBox(self)  
                    msg.setIcon(QtWidgets.QMessageBox.Icon.Warning)      
                    msg.setText("Contraseña Incorrecta")        
                    msg.setWindowTitle("Contraseña")        
                    msg.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)        
                    a = msg.exec()
      
        archivo.close()
        self.close()
        
    def cerrar(self):
        self.close()
    
                    

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)    
    ventana = VentanaProteger('')        
    ventana.show()
    sys.exit(app.exec())
    