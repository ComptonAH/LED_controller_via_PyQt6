from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import QIODevice, QIODeviceBase
from PyQt6.QtSerialPort import QSerialPort, QSerialPortInfo

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        self.pinsList = set()
        self.serial = QSerialPort()
        self.serial.setBaudRate(115200)
        self.serial.setParity(self.serial.Parity.NoParity)
        self.serial.setDataBits(self.serial.DataBits.Data8)
        self.serial.readyRead.connect(lambda: self.onRead())
        
        
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(532, 300)
        self.widget = QtWidgets.QWidget(parent=MainWindow)
        self.widget.setObjectName("widget")
        
        self.PINS_CB = QtWidgets.QComboBox(parent=self.widget)
        self.PINS_CB.setGeometry(QtCore.QRect(140, 150, 41, 30))
        self.PINS_CB.setEditable(False)
        self.PINS_CB.setObjectName("PINS_CB")
        
        self.LED_txt = QtWidgets.QLabel(parent=self.widget)
        self.LED_txt.setGeometry(QtCore.QRect(100, 150, 41, 31))
        
        font = QtGui.QFont()
        font.setPointSize(15)
        self.LED_txt.setFont(font)
        self.LED_txt.setObjectName("LED_txt")
        
        self.LED_BT_ON = QtWidgets.QPushButton(parent=self.widget)
        self.LED_BT_ON.setGeometry(QtCore.QRect(40, 210, 90, 40))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.LED_BT_ON.setFont(font)
        self.LED_BT_ON.setObjectName("LED_BT_ON")
        self.LED_BT_ON.clicked.connect(lambda: self.serialSend(self.onLED()))
        
        self.LED_BT_OFF = QtWidgets.QPushButton(parent=self.widget)
        self.LED_BT_OFF.setGeometry(QtCore.QRect(160, 210, 90, 40))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.LED_BT_OFF.setFont(font)
        self.LED_BT_OFF.setObjectName("LED_BT_OFF")
        self.LED_BT_OFF.clicked.connect(lambda: self.serialSend(self.offLED()))
        
        self.PIN_adding_slot = QtWidgets.QLineEdit(parent=self.widget)
        self.PIN_adding_slot.setGeometry(QtCore.QRect(147, 26, 30, 25))
        self.PIN_adding_slot.setObjectName("PIN_adding_slot")

        self.PIN_txt = QtWidgets.QLabel(parent=self.widget)
        self.PIN_txt.setGeometry(QtCore.QRect(60, 20, 81, 31))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.PIN_txt.setFont(font)
        self.PIN_txt.setObjectName("PIN_txt")
        
        self.PIN_BT_append = QtWidgets.QPushButton(parent=self.widget)
        self.PIN_BT_append.setGeometry(QtCore.QRect(50, 70, 91, 31))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.PIN_BT_append.setFont(font)
        self.PIN_BT_append.setObjectName("PIN_BT_append")
        self.PIN_BT_append.clicked.connect(lambda: self.pinAdd())
        self.PIN_BT_append.clicked.connect(lambda: self.PIN_adding_slot.clear())
        
        self.PIN_BT_remove = QtWidgets.QPushButton(parent=self.widget)
        self.PIN_BT_remove.setGeometry(QtCore.QRect(160, 70, 91, 31))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.PIN_BT_remove.setFont(font)
        self.PIN_BT_remove.setObjectName("PIN_BT_remove")
        self.PIN_BT_remove.clicked.connect(lambda: self.pinRemove())
        self.PIN_BT_remove.clicked.connect(lambda: self.PIN_adding_slot.clear())
        
        self.horizontalLayoutWidget = QtWidgets.QWidget(parent=self.widget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(250, 0, 31, 291))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.horizontalLayout.addItem(spacerItem)
        
        self.COM_txt = QtWidgets.QLabel(parent=self.widget)
        self.COM_txt.setGeometry(QtCore.QRect(320, 80, 91, 31))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.COM_txt.setFont(font)
        self.COM_txt.setObjectName("COM_txt")
        
        self.COMs_CB = QtWidgets.QComboBox(parent=self.widget)
        self.COMs_CB.setGeometry(QtCore.QRect(420, 80, 70, 30))
        self.COMs_CB.setEditable(False)
        self.COMs_CB.setObjectName("COMs_CB")
        
        ports = QSerialPortInfo().availablePorts()
        for port in ports:
            self.COMs_CB.addItem(port.portName())     
        
        self.PORT_BT_open = QtWidgets.QPushButton(parent=self.widget)
        self.PORT_BT_open.setGeometry(QtCore.QRect(310, 130, 91, 31))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.PORT_BT_open.setFont(font)
        self.PORT_BT_open.setObjectName("PORT_BT_open")
        self.PORT_BT_open.clicked.connect(lambda: self.openPort())
        
        self.PORT_BT_close = QtWidgets.QPushButton(parent=self.widget)
        self.PORT_BT_close.setGeometry(QtCore.QRect(420, 130, 91, 31))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.PORT_BT_close.setFont(font)
        self.PORT_BT_close.setObjectName("PORT_BT_close")
        self.PORT_BT_close.clicked.connect(lambda: self.closePort())
        
        MainWindow.setCentralWidget(self.widget)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        
        
    def pinAdd(self):
        pin = self.PIN_adding_slot.text()
        if pin not in self.pinsList and pin.isdigit():
            self.pinsList.add(pin)
            self.PINS_CB.addItem(pin)
            
    def pinRemove(self):
        pin = self.PIN_adding_slot.text()
        if pin in self.pinsList and pin.isdigit():
            self.PINS_CB.removeItem(list(self.pinsList).index(pin))
            self.pinsList.remove(pin)
            
    def openPort(self):
        self.serial.setPortName(self.COMs_CB.currentText())
        self.serial.open(QIODeviceBase.OpenModeFlag.ReadWrite)
        
    def closePort(self):
        self.serial.close()
    
    def onRead(self):
        rx = self.serial.readLine()
        rxs = str(rx,'utf-8').strip()
        data = rxs.split(',')
        
    def serialSend(self, data: list[int]):
        txs = ""
        for value in data:
            txs += str(value)
            txs += ','
        txs = txs[:-1]
        txs += ';'
        txEncoded = txs.encode(encoding='utf-8')
        self.serial.write(txEncoded)
        
    def onLED(self) -> list[int]:
        if self.PINS_CB.currentText() != '':
            pinLed = int(self.PINS_CB.currentText())
            data = [pinLed, 1]
        else:
            data = []
        return data
    
    def offLED(self) -> list[int]:
        if self.PINS_CB.currentText() != '':
            pinLed = int(self.PINS_CB.currentText())
            data = [pinLed, 0]
        else:
            data = []
        return data
        
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "LED controller"))
        self.LED_txt.setText(_translate("MainWindow", "LED"))
        self.LED_BT_ON.setText(_translate("MainWindow", "Turn on"))
        self.LED_BT_OFF.setText(_translate("MainWindow", "Turn off"))
        self.PIN_txt.setText(_translate("MainWindow", "Enter pin:"))
        self.PIN_BT_append.setText(_translate("MainWindow", "append"))
        self.PIN_BT_remove.setText(_translate("MainWindow", "remove"))
        self.COM_txt.setText(_translate("MainWindow", "COMPORT"))
        self.PORT_BT_open.setText(_translate("MainWindow", "open"))
        self.PORT_BT_close.setText(_translate("MainWindow", "close"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())