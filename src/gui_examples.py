import sys
from random import choice

from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QLabel, QLineEdit, QVBoxLayout

# pyqt에서는 단 하나의 QApplication이 필요하며, 단 하나만 존재해야 한다.
# sys.argv로 PyQt application에 command line arguments를 전달.
# command line argument가 없다면 QApplication([])라는 명령도 동작한다.




## PyQt GUI 프로그램 실행
def Run() :
    app = QApplication(sys.argv)
    
    window = MainWindow()
    window.show()       # ** Window는 기본적으로 숨겨져 있다. **

    # event loop 시작.
    app.exec()
    
    
    # application을 종료하거나 event loop가 멈추지 않는 한 이곳으로 도달하지 않음
    

class MainWindow(QMainWindow) :
    def __init__(self) :
        super().__init__()          # subclass로 Qt class를 생성할 때 반드시 super().__init__()을 불러야 함
        
        
        self.setWindowTitle("title")
        
        self.label = QLabel()
        self.input = QLineEdit()
        self.input.textChanged.connect(self.label.setText)
        
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.input)
        
        container = QWidget()
        container.setLayout(layout)
        
        self.setCentralWidget(container)


class MainWindow_1(QMainWindow):
    def __init__(self) :
        super().__init__()          # subclass로 Qt class를 생성할 때 반드시 super().__init__()을 불러야 함
        
        
        self.n_times_clicked = 0

        self.setWindowTitle("title")
        self.setFixedSize(720, 480)
        
        self.button_is_checked = True
        
        self.button = QPushButton("Press Me")
        self.button.setCheckable(True)
        self.button.clicked.connect(self.the_button_was_clicked)
        #button.clicked.connect(self.the_button_was_toggled)
        #self.button.released.connect(self.the_button_was_released)
        #self.button.setChecked(self.button_is_checked)
        
        self.windowTitleChanged.connect(self.the_window_title_changed)      # window title이 변경되면 발생시키는 이벤트
        
        self.setCentralWidget(self.button)
        
    def the_button_was_clicked(self) :
        self.button.setText("You already clicked me.")
        self.button.setEnabled(False)
        self.setWindowTitle("Button is used")
        print("Clicked!")
        
    def the_button_was_toggled(self, checked) :
        self.button_is_checked = checked        # self로 클래스 내에 button의 toggle 여부를 저장해둘 수 있음.
        print(self.button_is_checked)
        #print("Toggled?", checked)      # button 객체 내부의 toggle되는 아이템이 있는 것 같음. 누를 때마다 T/F 변환
    
    def the_button_was_released(self) :
        self.button_is_checked = self.button.isChecked()
        print(self.button_is_checked)
    
    def the_window_title_changed(self, window_title):
        print("Window title changed: %s" % window_title)
        if window_title == 'Something went wrong':
            self.button.setDisabled(True)
        
        #self.setCentralWidget(button)       # button으로 화면을 꽉 채운다.