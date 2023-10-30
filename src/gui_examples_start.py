import sys
from random import choice

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QLabel, QLineEdit, QVBoxLayout, QMenu

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
    
class MainWindow(QMainWindow) :     # context menu example. (우클릭하면 나오는 메뉴칸들 예제)
    def __init__(self) :
        super().__init__()
        
        #self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        #self.customContextMenuRequested.connect(self.on_context_menu)
    
    def contextMenuEvent(self, e) :
        context = QMenu(self)
        context.addAction(QAction("text1", self))
        context.addAction(QAction("text2", self))
        context.addAction(QAction("text3", self))
        context.exec(e.globalPos())         # 엥 이거랑 아래 거랑 뭐가 다른 거지..
        #context.exec(self.mapToGlobal(pos))        # 아 똑같나봄. 강의 문서에 entirely up to you which you choose.라고 되어 잇음

    
class MainWindow_3(QMainWindow):          # mouse click event example
    def __init__(self):
        super().__init__()
        self.label = QLabel("Click in this window")
        self.setCentralWidget(self.label)

    def mouseMoveEvent(self, e):
        self.label.setText("mouseMoveEvent")

    def mousePressEvent(self, e):
        if e.button() == Qt.MouseButton.LeftButton:
            # handle the left-button press in here
            self.label.setText("mousePressEvent LEFT")

        elif e.button() == Qt.MouseButton.MiddleButton:
            # handle the middle-button press in here.
            self.label.setText("mousePressEvent MIDDLE")

        elif e.button() == Qt.MouseButton.RightButton:
            # handle the right-button press in here.
            self.label.setText("mousePressEvent RIGHT")

    def mouseReleaseEvent(self, e):
        if e.button() == Qt.MouseButton.LeftButton:
            self.label.setText("mouseReleaseEvent LEFT")

        elif e.button() == Qt.MouseButton.MiddleButton:
            self.label.setText("mouseReleaseEvent MIDDLE")

        elif e.button() == Qt.MouseButton.RightButton:
            self.label.setText("mouseReleaseEvent RIGHT")

    def mouseDoubleClickEvent(self, e):
        if e.button() == Qt.MouseButton.LeftButton:
            self.label.setText("mouseDoubleClickEvent LEFT")

        elif e.button() == Qt.MouseButton.MiddleButton:
            self.label.setText("mouseDoubleClickEvent MIDDLE")

        elif e.button() == Qt.MouseButton.RightButton:
            self.label.setText("mouseDoubleClickEvent RIGHT")


class MainWindow_2(QMainWindow) :           # 칸에 텍스트를 입력하는 대로 label이 변화하는 예제
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