import sys
from PyQt6.QtCore import Qt, QEvent
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QStackedLayout, QPushButton,
    QTabWidget, QTextEdit, QLabel
)
from PyQt6.QtGui import QPalette, QColor, QPixmap, QKeyEvent, QKeySequence

from .voice_recog import SpeechRecognition
from .crawling import News_Crawling


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
        self.hlayout = QHBoxLayout()
        self.left_vlayout = QVBoxLayout()       # 검색하는 곳
        self.middle_vlayout = QVBoxLayout()       # crawling 칸
        self.right_vlayout = QVBoxLayout()       # memo 칸
        
        self.hlayout.setContentsMargins(5,0,5,0)
        self.hlayout.setSpacing(3)

        ##### left side layout design
            ## put title image
        title_pic = QPixmap()
        title_pic.load("image1.png")
        pix_label = QLabel()
        pix_label.setPixmap(title_pic)
        self.left_vlayout.addWidget(pix_label)
        
            ## put search word and button
        h_search_layout = QHBoxLayout()     # 검색단어 입력하는 곳 (textedit, btn)
        self.search_text = QTextEdit()
        self.search_text.setPlaceholderText("검색할 단어를 입력하시오")
        self.search_btn = QPushButton("검색")
        self.speech_btn = QPushButton("음성")
        self.search_text.installEventFilter(self)
        self.search_btn.clicked.connect(self.click_search_btn)
        self.speech_btn.clicked.connect(self.click_speech_recog_btn)
        self.search_btn.setMaximumHeight(50)
        print('search_btn.height():', self.search_btn.height())
        self.search_text.setFixedHeight(self.search_btn.height()) 
        h_search_layout.addWidget(self.search_text)
        h_search_layout.addWidget(self.speech_btn)
        h_search_layout.addWidget(self.search_btn)
        self.left_vlayout.addLayout(h_search_layout, 1)
        
            ## put recent searched words
        guide_label = QLabel()
        guide_label.setText("최근 검색 단어")
        self.left_vlayout.addWidget(guide_label, 1)
        recent_words_layout = QGridLayout()     # 최근 검색 단어 띄우는 layout
        recent_words_layout.addWidget(Color('red'), 0, 0)
        recent_words_layout.addWidget(Color('green'), 1, 0)
        recent_words_layout.addWidget(Color('blue'), 1, 1)
        recent_words_layout.addWidget(Color('purple'), 2, 1)
        self.left_vlayout.addLayout(recent_words_layout)
        self.hlayout.addLayout(self.left_vlayout)
        ##### =====================================================
        
        self.hlayout.addLayout(self.middle_vlayout, 2)
        # sample_widget = Color('yellow')     # 크롤링하기 전 레이아웃 적용.. 굳이 안 해도 돼서. 위아래 순서는 상관 없는 듯?
        # sample_widget.setStyleSheet("background-color: transparent;")
        # v_layout2.addWidget(sample_widget)
        
        self.right_vlayout.addWidget(Color('purple'))
        self.right_vlayout.addWidget(Color('purple'))
        self.right_vlayout.addWidget(Color('green'))
        self.hlayout.addLayout(self.right_vlayout, 1)
        
        widget = QWidget()
        widget.setLayout(self.hlayout)
        self.setCentralWidget(widget)
        
    
    def click_search_btn(self) :
        text = self.search_text.toPlainText() # text_edit text 값 가져오기
        
        if text == '' or text == ' ' :
            print('nothing in search_text')
            return False
        
        news_result = News_Crawling(text)       # list
        
        if len(news_result) == 0 :
            print('no search result.')
            no_result_label = QLabel("결과가 없습니다.")
            self.middle_vlayout.addWidget(no_result_label)
        else :
            print('crawling result 있음')
            for news in news_result :
                news_layout = make_news_layout(news)
                news_link = news['link']
                self.middle_vlayout.addLayout(news_layout, 0)
                news_layout.mousePressEvent = self.news_layout_clicked(news_link=news_link)
        
        
    def click_speech_recog_btn(self) :
        word = SpeechRecognition()
        print('word : ', word)
        self.search_text.setText(word)
        
        self.click_search_btn()
    
    def news_layout_clicked(self, e, news_link) :      # 크롤링해서 가져온 뉴스의 레이아웃이 클릭되면
        print('news layout clicked')
        
    
    def eventFilter(self, obj, e) :
        if obj == self.search_text and e.type() == QEvent.Type.KeyPress :
            key = e.key()       # 여기까진 잘 된다. 근데 enter를 누르면 뭐가 안 됨...
            if key == Qt.Key.Key_Return :   # Key_Enter이 아니라 Key_Return이 된다!
                # Enter키를 눌렀을 때, 검색 버튼 클릭 이벤트 발생
                print('wjtjjwtjj enter!!')
                self.search_btn.click()
                return True
        
        return super().eventFilter(obj, e)
        


def make_news_layout(news) :
    print(news['company'])
    print(news['title'])
    print(news['info'])
    print(news['link'])
    
    company = QLabel(news['company'])
    title = QLabel(news['title'])
    info = QLabel(news['info'])
    link = QLabel(news['link'])
    
    vertical_layout = QVBoxLayout()
    vertical_layout.addWidget(company)
    vertical_layout.addWidget(title)
    vertical_layout.addWidget(info)
    vertical_layout.addWidget(link)
    
    return vertical_layout
        

class Color(QWidget):
    def __init__(self, color):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(color))
        self.setPalette(palette)