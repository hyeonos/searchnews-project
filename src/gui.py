import sys
from PyQt6.QtCore import Qt, QEvent
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QStackedLayout, QPushButton,
    QTabWidget, QTextEdit, QLabel
)
from PyQt6.QtGui import QPalette, QColor, QPixmap, QKeyEvent, QKeySequence



def Run() :
    app = QApplication(sys.argv)
    
    window = MainWindow()
    window.show()       # ** Window는 기본적으로 숨겨져 있다.
    
    app.exec()


# layout부터 만들기..
class MainWindow(QMainWindow):      # horizontal에 vertical을 연결해서 layout 만들기. 하지만 정렬에 어려움이 있음.

    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("Scrapper")
        self.setFixedSize(1600, 900)
        
        #widget = Color('red')       # widget이 빨간색으로 변한다.
        
        #layout = QVBoxLayout()
        h_layout = QHBoxLayout()
        left_vlayout1 = QVBoxLayout()       # 검색하는 곳
        v_layout2 = QVBoxLayout()       # crawling 칸
        v_layout3 = QVBoxLayout()       # memo 칸
        
        h_layout.setContentsMargins(5,0,5,0)
        h_layout.setSpacing(3)

        ##### left side layout design
            ## put title image
        title_pic = QPixmap()
        title_pic.load("image1.png")
        pix_label = QLabel()
        pix_label.setPixmap(title_pic)
        left_vlayout1.addWidget(pix_label)
        
            ## put search word and button
        h_search_layout = QHBoxLayout()     # 검색단어 입력하는 곳 (textedit, btn)
        self.search_text = QTextEdit()
        self.search_text.setPlaceholderText("검색할 단어를 입력하시오")
        self.search_btn = QPushButton("검색")
        self.search_text.installEventFilter(self)
        self.search_btn.clicked.connect(self.click_search_btn)
        self.search_btn.setMaximumHeight(50)
        print('search_btn.height():', self.search_btn.height())
        self.search_text.setFixedHeight(self.search_btn.height()) 
        h_search_layout.addWidget(self.search_text)
        h_search_layout.addWidget(self.search_btn)
        left_vlayout1.addLayout(h_search_layout, 1)
        
            ## put recent searched words
        guide_label = QLabel()
        guide_label.setText("최근 검색 단어")
        left_vlayout1.addWidget(guide_label, 1)
        recent_words_layout = QGridLayout()     # 최근 검색 단어 띄우는 layout
        recent_words_layout.addWidget(Color('red'), 0, 0)
        recent_words_layout.addWidget(Color('green'), 1, 0)
        recent_words_layout.addWidget(Color('blue'), 1, 1)
        recent_words_layout.addWidget(Color('purple'), 2, 1)
        left_vlayout1.addLayout(recent_words_layout)
        h_layout.addLayout(left_vlayout1)
        ##### =====================================================
        
        v_layout2.addWidget(Color('yellow'))
        h_layout.addLayout(v_layout2, 2)
        
        v_layout3.addWidget(Color('purple'))
        v_layout3.addWidget(Color('purple'))
        v_layout3.addWidget(Color('green'))
        h_layout.addLayout(v_layout3, 1)
        
        widget = QWidget()
        widget.setLayout(h_layout)
        self.setCentralWidget(widget)
        
    
    def click_search_btn(self) :
        text = self.search_text.toPlainText() # text_edit text 값 가져오기
        print('search_btn clicked, ', text)
        
    def eventFilter(self, obj, e) :
        if obj == self.search_text and e.type() == QEvent.Type.KeyPress :
            key = e.key()       # 여기까진 잘 된다. 근데 enter를 누르면 뭐가 안 됨...
            if key == Qt.Key.Key_Return :   # Key_Enter이 아니라 Key_Return이 된다!
                # Enter키를 눌렀을 때, 검색 버튼 클릭 이벤트 발생
                print('wjtjjwtjj enter!!')
                self.search_btn.click()
                return True
        
        return super().eventFilter(obj, e)
        
        

class Color(QWidget):
    def __init__(self, color):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(color))
        self.setPalette(palette)