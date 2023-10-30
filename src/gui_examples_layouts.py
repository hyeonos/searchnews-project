import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QStackedLayout, QPushButton,
    QTabWidget
)
from PyQt6.QtGui import QPalette, QColor



def Run() :
    app = QApplication(sys.argv)
    
    window = MainWindow()
    window.show()       # ** Window는 기본적으로 숨겨져 있다.
    
    app.exec()



class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        
        tabs = QTabWidget()
        tabs.setDocumentMode(True)      # give slim                  line tabs(??) similar to what you see on other platforms
        tabs.setTabPosition(QTabWidget.TabPosition.West)
        tabs.setMovable(True)       # tab을 움직일 수 있게 만든다.
        
        for _, color in enumerate(["red", "green", "blue", "yellow"]) :
            tabs.addTab(Color(color), color)
        
        self.setCentralWidget(tabs)


class MainWindow_4(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Main Window")
        
        page_layout = QVBoxLayout()
        button_layout = QHBoxLayout()
        self.stacklayout = QStackedLayout()
        
        page_layout.addLayout(button_layout)
        page_layout.addLayout(self.stacklayout)
        
        btn = QPushButton("First")
        btn.pressed.connect(self.activate_tab_1)
        button_layout.addWidget(btn)
        self.stacklayout.addWidget(Color("red"))
        
        btn = QPushButton("Second")
        btn.pressed.connect(self.activate_tab_2)
        button_layout.addWidget(btn)
        self.stacklayout.addWidget(Color("green"))
        
        btn = QPushButton("Third")
        btn.pressed.connect(self.activate_tab_3)
        button_layout.addWidget(btn)
        self.stacklayout.addWidget(Color("yellow"))
        
        widget = QWidget()
        widget.setLayout(page_layout)
        self.setCentralWidget(widget)
        
        
    def activate_tab_1(self):
        self.stacklayout.setCurrentIndex(0)
        
    def activate_tab_2(self):
        self.stacklayout.setCurrentIndex(1)
    
    def activate_tab_3(self):
        self.stacklayout.setCurrentIndex(2)


class MainWindow_3(QMainWindow):
    def __init__(self) :
        super(MainWindow, self).__init__()
        
        self.setWindowTitle("asdfbabab")
        
        layout = QStackedLayout()
        
        layout.addWidget(Color('red'))
        layout.addWidget(Color('green'))
        layout.addWidget(Color('blue'))
        layout.addWidget(Color('yellow'))
        
        layout.setCurrentIndex(3)
        
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)


class MainWindow_2(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("My App")

        layout = QGridLayout()

        layout.addWidget(Color('red'), 0, 0)
        layout.addWidget(Color('green'), 1, 0)
        layout.addWidget(Color('blue'), 1, 1)
        layout.addWidget(Color('purple'), 2, 1)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)


class MainWindow_1(QMainWindow):      # horizontal에 vertical을 연결해서 layout 만들기. 하지만 정렬에 어려움이 있음.

    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("My App")

        #widget = Color('red')       # widget이 빨간색으로 변한다.
        
        #layout = QVBoxLayout()
        layout1 = QHBoxLayout()
        layout2 = QVBoxLayout()
        layout3 = QVBoxLayout()
        
        layout1.setContentsMargins(0,0,0,0)
        layout1.setSpacing(20)

        layout2.addWidget(Color('red'))
        layout2.addWidget(Color('green'))
        layout2.addWidget(Color('blue'))

        layout1.addLayout(layout2)
        
        layout1.addWidget(Color('green'))
        
        layout3.addWidget(Color('red'))
        layout3.addWidget(Color('purple'))

        layout1.addLayout(layout3)
        
        

        widget = QWidget()
        widget.setLayout(layout1)
        self.setCentralWidget(widget)
        
        

class Color(QWidget):

    def __init__(self, color):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(color))
        self.setPalette(palette)