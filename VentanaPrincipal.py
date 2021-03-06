#Parte Lógica de la Ventana Principal

import time, os, pyqtgraph.exporters
import pyqtgraph as pg
import pandas as pd 
import serial as ser
from VentanaPrincipalDiseño import Ui_MainWindow
from PyQt5 import QtWidgets, QtCore, QtGui, QtTest   
from PyQt5.QtCore import QTimer, QTime
from PyQt5.QtWidgets import QMessageBox, QAction
from pyqtgraph.Qt import QtGui

#Ventana Principal
class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow): #Main Window
     
      def __init__(self, parent=None):
         super(MainWindow, self).__init__(parent)
         
        #Diseño
         self.setupUi(self)
         self.setStyleSheet("color: rgb(255, 255, 255); background-color: rgb(35, 35, 35);") 
         
        #Variables
         self.count = 0
         self.commando='@249DL?;FF'
         self.TP=[]
         self.t=[]
         self.DatosGraf=[]
         self.paso=0
         self.start = False
         self.nombre = "prueba1.csv"

        #Funciones extra.
         self.BotonSelec()
         self.Guard()
         
        #Temporizador
         timer1 = QTimer(self)
         timer1.timeout.connect(self.Datos)
         timer1.start(1000)
      
      #Botones
        #Botones Sensor
         self.b1_4.clicked.connect(self.start_action)#Iniciar Sensor
         self.b25_2.clicked.connect(self.reset_action)#Reiniciar Sensor
         self.b2_2.clicked.connect(self.pause_action)#Detener Sensor
        
        #Botones Tiempo
         self.b1_5.clicked.connect(self.T_Determinado)#Determinado
         self.b1_6.clicked.connect(self.T_Indeterminado)#Indeterminado      

        #Botones Guardado
         self.b5_2.clicked.connect(self.guardarg)#Guardar Gráfica
         self.b6_2.clicked.connect(self.guardard)#Guardar Datos
        
        #Botones Pres y Graf
         self.b3_2.clicked.connect(self.presionventana)#Presión Actual
         self.b4_2.clicked.connect(self.grafventana)#Gráfica
        
        #Botones Puertos
         self.radioButton.toggled.connect(self.BotonSelec)#TTYUSB2
         self.radioButton_2.toggled.connect(self.BotonSelec)#TTYUSB1
         self.radioButton_3.toggled.connect(self.BotonSelec)#TTYUSB0
         
        #Botones Selección
         self.pushButton.clicked.connect(self.OpenFileDatos)#Seleccion Datos
         self.pushButton_2.clicked.connect(self.OpenFileGraf)#Seleccion Graf
         
        #Botones Cerrar
         quit = QAction("Quit", self)#Close
         quit.triggered.connect(self.closeEvent)

         self.show()

 #Funciones ligadas a los botones
    
     #Funciones para elegir ruta
      def OpenFileDatos(self):
          fileName = QtGui.QFileDialog.getExistingDirectory(self, 'OpenFile')
          self.lineEdit.setText(fileName)
      
      def OpenFileGraf(self):
          fileName = QtGui.QFileDialog.getExistingDirectory(self, 'OpenFile')
          self.lineEdit_2.setText(fileName)
      
     #Función para elegir puerto 
      def BotonSelec(self):
          if self.radioButton.isChecked():
              self.pSerial = ser.Serial('/dev/ttyUSB2',baudrate=9600,timeout=1)
          elif self.radioButton_2.isChecked():
              self.pSerial = ser.Serial('/dev/ttyUSB1',baudrate=9600,timeout=1)
          elif self.radioButton_3.isChecked():
              self.pSerial = ser.Serial('/dev/ttyUSB0',baudrate=9600,timeout=1)
              
     #Función guardado automático
      def Guard(self):
          if self.radioButton_4.isChecked():
               self.guard = True
          elif self.radioButton_5.isChecked():
               self.guard = False
            
     #Función error puerto
      def Puerto_error(self):
         self.start = False
         self.errorp = QMessageBox()
         self.errorp.setWindowTitle("Error")
         self.errorp.setText("¡Puerto Incorrecto!")
         self.errorp.setDetailedText("Cambiar el puerto en la pestaña de configuración.")
         self.errorp.setIcon(QMessageBox.Critical)
         self.errorp.setStyleSheet("color: rgb(255, 255, 255); background-color: rgb(64, 64, 64);")
         self.errorp.exec()

     #Obtención de datos.

      #Función interactuante con el sensor.
      def regreso(self):
         x='@249DLC!STOP;FF'
         self.pSerial.write(x.encode())
         x='@249DLC!START;FF'
         self.pSerial.write(x.encode())
         QtTest.QTest.qWait(2500)
         self.pSerial.write(self.commando.encode())
         z=self.pSerial.readline().decode()
         s=z.split(';')
         try:
            s=s[3].split('\r')
            print(s)
         except Exception:
            self.Puerto_error()
            return 1
         a=s[0]
         now=time.strftime("%X")
         return a,now

      #Tabla y presión
      def Datos(self):
         global tabla, a
         if self.start:
            c=self.regreso()
            a=c[0]
            now=c[1]
            self.presion=float(a)
            self.count = self.count+1
            self.TP.append((now,self.presion))
            tabla=pd.DataFrame(self.TP,columns=['Hora','Presión']) 
            self.t.append(self.paso)
            self.DatosGraf.append(self.presion)
            self.paso=self.paso+5
            if self.count == tiempo1:
               self.start = False
            else:
               pass
            if self.guard:
               tabla.to_csv(r'/home/detectores/Software/mks_control/Datos_Presion/datos1.csv',index=False)
               path="/home/detectores/Software/mks_control/Datos_Presion/"+ self.nombre
               os.rename("/home/detectores/Software/mks_control/Datos_Presion/datos1.csv",path)
               
      #Botones Iniciar, Pausar, Reiniciar          
      
      def start_action(self):
         if self.pSerial.is_open:
           self.pSerial.close()
         self.pSerial.open()
         self.start = True
         try:
            if self.count == tiempo1:
               self.start = False
         except Exception:
            self.start = False
            self.error = QMessageBox()
            self.error.setWindowTitle("Error")
            self.error.setText("¡Tiempo no definido!")
            self.error.setIcon(QMessageBox.Critical)
            self.error.setDetailedText("Definir tiempo con los botones Determinado o Indeterminado.")
            self.error.setStyleSheet("color: rgb(255, 255, 255); background-color: rgb(64, 64, 64);")
            self.error.exec()

      def pause_action(self):
         self.start = False
  
      def reset_action(self):
         self.start = False
         self.count = 0
         
     #Funcion ventana presion
      
      def presionventana(self):
        self.PressureWindow = QtWidgets.QWidget()
        self.PressureWindow.resize(410, 270)
        self.PressureWindow.setStyleSheet("background-color: rgb(45, 45,45); border-color: rgb(56, 56, 56);alternate-background-color: rgb(0, 0, 0);")
        self.PressureWindow.setWindowTitle("Presión Actual.")
        
        #Título Presión Actual
        self.labelp = QtWidgets.QLabel(self.PressureWindow)
        self.labelp.setGeometry(QtCore.QRect(20, 10, 368, 31))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setUnderline(False)
        font.setWeight(75)
        font.setKerning(True)
        self.labelp.setFont(font)
        self.labelp.setAutoFillBackground(False)
        self.labelp.setStyleSheet("color: rgb(255, 255, 255); background-color: rgb(56, 56, 56);")
        self.labelp.setScaledContents(False)
        self.labelp.setAlignment(QtCore.Qt.AlignCenter)
        self.labelp.setText("Presión cada 5s (aprox.)")
        
       #Título Hora
        self.labelp_2 = QtWidgets.QLabel(self.PressureWindow)
        self.labelp_2.setGeometry(QtCore.QRect(40, 70, 321, 61))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.labelp_2.setFont(font)
        self.labelp_2.setStyleSheet("color: rgb(255, 255, 255);")
        self.labelp_2.setAlignment(QtCore.Qt.AlignCenter)
        self.labelp_2.setText("Hora:  ")
        
       #Título Presión
        self.labelp_3 = QtWidgets.QLabel(self.PressureWindow)
        self.labelp_3.setGeometry(QtCore.QRect(20, 150, 361, 61))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.labelp_3.setFont(font)
        self.labelp_3.setStyleSheet("color: rgb(255, 255, 255);")
        self.labelp_3.setAlignment(QtCore.Qt.AlignCenter)
        self.labelp_3.setText("Presión:  ")
        
        self.PressureWindow.show()
        timerp=QTimer(self)
        timerp.timeout.connect(self.showpressure)
        timerp.start(1000)
        
       #Actualizador de Presión    
        
      def showpressure(self): 
        HoraActual=QTime.currentTime()
        Tiempo=HoraActual.toString('hh:mm:ss')
        Press=a
        self.labelp_2.setText("Hora:  " + Tiempo)
        self.labelp_3.setText("Presión:  " + Press + " Torr")
        QtTest.QTest.qWait(2000)
        
     #Funciones ventana grafica
      def grafventana(self):
          
       #Diseño ventana
         self.win=pg.GraphicsWindow()
         self.win.setWindowTitle("Gráfica")
         self.layout = QtGui.QGridLayout()
         self.layout.setParent(self.win)
         self.win.setStyleSheet("color: rgb(255, 255, 255); background-color: rgb(35, 35, 35);") 
        
       #Grafica datos
         self.curve=pg.PlotWidget()
         self.win.setLayout(self.layout)

       #Botones 
         self.startBtn = QtGui.QPushButton("Gráfica Actual") #Botón iniciar gráfica.
         self.startBtn.setParent(self.win)
         self.startBtn.show()

         self.stopBtn = QtGui.QPushButton("Detener") #Botón detener gráfica.
         self.stopBtn.setParent(self.win)
         self.stopBtn.show()

        #Organización botones     
         self.layout.addWidget(self.startBtn, 1, 0)
         self.layout.addWidget(self.stopBtn, 2, 0)
         self.layout.addWidget(self.curve, 0, 3, 2, 3 )

        #Conexión botones
         self.startBtn.clicked.connect(self.Inicio_G)
         self.stopBtn.clicked.connect(self.Pausar_G)
        
       #Gráfica y diseño
         self.curve.plot(self.t,self.DatosGraf,pen=pg.mkPen('r', width=2))
         self.curve.setLabel(axis='left', text='Presión (Torr)')
         self.curve.setLabel(axis='bottom', text='Tiempo (s)')                
         pg.mkColor('r')             
         self.curve.setPos(0,0)

       #Contador para auto-actualizar
         self.startg = False
         timerg = QTimer(self)
         timerg.timeout.connect(self.Actualizador)
         timerg.start(1000)

         self.win.show()

     #Funciones de los botones de las gráfica
      def Inicio_G(self):
         self.startg=True

      def Pausar_G(self):
         self.startg=False
      
      def Actualizador(self):
         QtTest.QTest.qWait(2500)
         if self.startg:
            self.curve.plot(self.t,self.DatosGraf,pen=pg.mkPen('r', width=2))
         exporter = pg.exporters.ImageExporter(self.curve.plotItem)
         exporter.export('/home/detectores/Software/mks_control/Graficas_Presion/grafica.png')
   
     #Funciones para determinar el tiempo
      def T_Determinado(self):
         global tiempo1,tiempo2
         text= QtWidgets.QInputDialog.getText(self, 'Tiempo...', '¿Cuántos segundos?:')   
         if text[1]:
            tiempo = text[0]
         tiempo1=float(tiempo)
         tiempo2=False
         try: 
            cmd='@254ADC?;FF'
            self.pSerial.write(cmd.encode())
         except Exception:
            self.Puerto_error()
         
      def T_Indeterminado(self):
         global tiempo1, tiempo2
         tiempo2=True
         tiempo1=-1
         try: 
            cmd='@254ADC?;FF'
            self.pSerial.write(cmd.encode())
         except Exception:
            self.Puerto_error()
          
     #Cerrar ventana
      def closeEvent(self,event):
         #Diseño ventana 
          self.close = QMessageBox()
          self.close.setWindowTitle("Salir...")
          self.close.setText("¿Deseas salir?")
          self.close.setIcon(QMessageBox.Question)
          self.close.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
          self.close.setStyleSheet("color: rgb(255, 255, 255); background-color: rgb(64, 64, 64);")
          self.close = self.close.exec()

         #Acciones
          if self.close == QMessageBox.Yes:
             x='@249DLC!STOP;FF'
             self.pSerial.write(x.encode())
             event.accept()
          else:
             event.ignore()
             
     #Guardado Datos y Graf
      def guardard(self):
         text= QtWidgets.QInputDialog.getText(self, 'Guardar Como:', 'Guardar Como:')   
         if text[1]:
            self.nombre = text[0] + ".csv"
            tabla.to_csv(r'/home/detectores/Software/mks_control/Datos_Presion/datos1.csv',index=False)
            path="/home/detectores/Software/mks_control/Datos_Presion/"+ self.nombre
            os.rename("/home/detectores/Software/mks_control/Datos_Presion/datos1.csv",path)
             
      def guardarg(self):
         text= QtWidgets.QInputDialog.getText(self, 'Guardar Como:', 'Guardar Como:')   
         if text[1]:
            nombre = text[0] + ".png"
            path="/home/detectores/Software/mks_control/Graficas_Presion/"+nombre
            exporter = pg.exporters.ImageExporter(self.curve.plotItem)
            exporter.export(path)
           
if __name__ == "__main__":
   app = QtWidgets.QApplication([])
   window = MainWindow()
   window.show()
   app.exec_()
   
# pylint: disable-msg=E0611
# pylint: disable wildcard-import