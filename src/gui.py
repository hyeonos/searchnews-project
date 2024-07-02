import sys
import copy

from PyQt6.QtCore import Qt, QEvent
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QTextEdit, QLabel, QMessageBox, QTextBrowser, QScrollArea, QGroupBox
)
from PyQt6.QtGui import QPalette, QColor, QPixmap, QKeyEvent, QKeySequence, QFont

from .voice_recog import SpeechRecognition
from .crawling import News_Crawling, News_Content_Crawling
from .database import *


def Run() :
    app = QApplication(sys.argv)
    
    global db
    db = ScrapDB()
    
    window = MainWindow()
    window.show()       # ** Window는 기본적으로 숨겨져 있다.
    
    app.exec()


# layout부터 만들기..
class MainWindow(QMainWindow):      # horizontal에 vertical을 연결해서 layout 만들기. 하지만 정렬에 어려움이 있음.

    def __init__(self):
        super(MainWindow, self).__init__()

        self.scrapped_news_list = db.read_scrap()
        
        
        self.setWindowTitle("Scrapper")
        self.setFixedSize(1600, 900)
        
        self.hlayout = QHBoxLayout()
        self.left_vlayout = QVBoxLayout()       # 검색하는 곳
        self.middle_vlayout = QVBoxLayout()       # crawling 칸
        self.right_vlayout = QVBoxLayout()       # memo 칸
        
        self.hlayout.setContentsMargins(5,0,5,0)
        self.hlayout.setSpacing(3)

        ##### left side layout design
            ## put title image
        title_pic = QPixmap("scrappers_icon.png")
        title_pic.scaled(100, 100)
        #title_pic.load("image1.png")
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
        self.search_btn.setMaximumWidth(50)
        self.speech_btn.setMaximumHeight(50)
        self.speech_btn.setMaximumWidth(50)
        self.search_text.setFixedHeight(self.search_btn.height()) 
        h_search_layout.addWidget(self.search_text)
        h_search_layout.addWidget(self.speech_btn)
        h_search_layout.addWidget(self.search_btn)
        self.left_vlayout.addLayout(h_search_layout)
        
        self.hlayout.addLayout(self.left_vlayout, 1)
        ##### =====================================================
        
        self.hlayout.addLayout(self.middle_vlayout, 3)
        
        ##### =====================================================
        # self.right_vlayout.addWidget(Color('purple'))
        self.right_vlayout.addStretch(1)
        if len(self.scrapped_news_list) > 0 :
            for scrapped_news in self.scrapped_news_list :
                scrapped_layout = ScrappedClickableWidget(self, scrapped_news)
                self.right_vlayout.addWidget(scrapped_layout, 0)
        
        self.hlayout.addLayout(self.right_vlayout, 1)
        
        widget = QWidget()
        widget.setLayout(self.hlayout)
        self.setCentralWidget(widget)
    
    
    def view_crawling_result(self, news_result) :
        print('view crawling result ...')
        
        for i, news in enumerate(news_result) :
            news_layout = NewsListClickableWidget(self, news, i)
            self.middle_vlayout.addWidget(news_layout, 0)
        
    
    def click_search_btn(self) :
        for i in reversed(range(self.middle_vlayout.count())):
            widget = self.middle_vlayout.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)
        
        text = self.search_text.toPlainText() # text_edit text 값 가져오기
        
        if text == '' or text == ' ' :
            print('nothing in search_text')
            return False
        
        self.news_result = News_Crawling(text)       # list
        
        if len(self.news_result) == 0 :
            print('no search result.')
            no_result_label = QLabel("결과가 없습니다.")
            self.middle_vlayout.addWidget(no_result_label)
        else :
            print('crawling result 있음')
            self.view_crawling_result(self.news_result)
    
        
    def click_speech_recog_btn(self) :
        word = SpeechRecognition()
        print('word : ', word)
        self.search_text.setText(word)
        
        self.click_search_btn()
    
    
    
    def click_back_btn(self) :
        for i in reversed(range(self.middle_vlayout.count())):
            widget = self.middle_vlayout.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)
        
        self.view_crawling_result(self.news_result)
    
    
    def click_scrap_btn(self) :
        QMessageBox.about(self, 'Scrapper', '스크랩되었습니다.')
        
        company = self.middle_vlayout.itemAt(0).widget().text()
        title = self.middle_vlayout.itemAt(1).widget().text()
        content = self.middle_vlayout.itemAt(2).widget().toPlainText()
        
        
        print("데이터베이스에 저장...")
        print('company : ', company)
        print('title : ', title)
        print('content : ', content)
        
        db.add_scrap(company, title, content)
        
        new_scrapped = ScrappedClickableWidget(self, {'company' : company, 'title' : title, 'content' : content})
        self.right_vlayout.addWidget(new_scrapped, 0)
    

    def news_layout_clicked(self, e) :      # 크롤링해서 가져온 뉴스의 레이아웃이 클릭되면
        print('버튼 클릭 확인')
        if e.button() == Qt.MouseButton.LeftButton:
            print("QVBoxLayout를 클릭하셨습니다!")


    def eventFilter(self, obj, e) :
        if obj == self.search_text and e.type() == QEvent.Type.KeyPress :
            key = e.key()
            if key == Qt.Key.Key_Return :
                # Enter키를 눌렀을 때, 검색 버튼 클릭 이벤트 발생
                self.search_btn.click()
                return True
                
        return super().eventFilter(obj, e)
        


class NewsListClickableWidget(QWidget):
    def __init__(self, parent, news, index) :
        super().__init__()

        self.parent = parent
        self.layout = QVBoxLayout()
        self.groupbox = QGroupBox('뉴스')
        self.setLayout(self.layout)
        self.index = index
        
        self.groupbox.setLayout(self.layout)
        self.parent.middle_vlayout.addWidget(self.groupbox)
        
        self.company = news['company']
        self.title = news['title']
        self.info = news['info']
        self.link = news['link']

        ql_company = QLabel(self.company)
        ql_title = QLabel(self.title)
        ql_info = QLabel(self.info)
        ql_company.setFont(QFont('Arial', 9))
        ql_title.setFont(QFont('Arial', 12))
        ql_info.setFont(QFont('Arial', 10))
        
        self.layout.addWidget(ql_company)
        self.layout.addWidget(ql_title)
        self.layout.addWidget(ql_info)
                
        self.parent.scrap_btn = QPushButton('스크랩')
        self.parent.scrap_btn.clicked.connect(self.parent.click_scrap_btn)
        
        self.parent.back_btn = QPushButton('뒤로 가기')
        self.parent.back_btn.clicked.connect(self.parent.click_back_btn)
        
        self.groupbox.mousePressEvent = self.mousePressEvent
        

    def mousePressEvent(self, event):
        print(f"클릭 가능한 항목을 클릭했습니다.")
        print(f"company : {self.company}, title : {self.title}, info : {self.info}, link : {self.link}")
        
        self.deleteLater()
        
        # layout에 들어 있는 widget들 제거
        for i in reversed(range(self.parent.middle_vlayout.count())):
            widget = self.parent.middle_vlayout.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)
        
        article = make_news_content(self.link)
        
        # 가져온 뉴스 내용으로 가운데 layout을 새롭게 작성
        self.content = article

        ql_company = QLabel(self.company)
        ql_title = QLabel(self.title)
        ql_title.setFixedWidth(800)
        ql_title.setWordWrap(True)
        qb_content = QTextBrowser()
        
        for i in self.content :
            qb_content.append(i + '\n')
        ql_company.setFont(QFont('Arial', 9))
        ql_title.setFont(QFont('Arial', 20))
        
        self.parent.middle_vlayout.addWidget(ql_company, 0)
        self.parent.middle_vlayout.addWidget(ql_title, 0)
        self.parent.middle_vlayout.addWidget(qb_content, 0)
        
        self.parent.middle_vlayout.addWidget(self.parent.back_btn)      # Main
        self.parent.middle_vlayout.addWidget(self.parent.scrap_btn)      # Main
        
        
    def click_back_btn(self) :
        print("뒤로 가기 버튼 눌림")
        
        for i in reversed(range(self.parent.middle_vlayout.count())):
            widget = self.parent.middle_vlayout.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)
        
        #self.parent.middle_vlayout.addWidget(self.parent.news_tmp, 0)
        
        self.parent.view_crawling_result(self.parent.news_tmp)




class ScrappedClickableWidget(QWidget):
    def __init__(self, parent, scrapped_news) :
        super().__init__()

        self.parent = parent
        self.groupbox = QGroupBox('스크랩')
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        
        self.groupbox.setLayout(self.layout)
        self.parent.right_vlayout.addWidget(self.groupbox)
        
        self.company = scrapped_news['company']
        self.title = scrapped_news['title']
        self.content = scrapped_news['content']

        ql_company = QLabel(self.company)
        ql_title = QLabel(self.title)
        
        self.layout.addWidget(ql_company)
        self.layout.addWidget(ql_title)
        self.layout.addStretch(1)
        
        self.groupbox.mousePressEvent = self.mousePressEvent    # ★ 레이아웃 클릭하게 만들기.

        
    def mousePressEvent(self, event):
        print("스크랩 항목을 클릭했습니다.")
        print(f"company : {self.company}, title : {self.title}, info : {self.content}")
        
        # layout에 들어 있는 widget들 제거
        for i in reversed(range(self.parent.middle_vlayout.count())):
            widget = self.parent.middle_vlayout.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)

        ql_company = QLabel(self.company)
        ql_title = QLabel(self.title)
        ql_title.setFixedWidth(800)
        ql_title.setWordWrap(True)
        qb_content = QTextBrowser()
        qb_content.append(self.content)

        ql_company.setFont(QFont('Arial', 9))
        ql_title.setFont(QFont('Arial', 20))
        
        self.parent.middle_vlayout.addWidget(ql_company, 0)
        self.parent.middle_vlayout.addWidget(ql_title, 0)
        self.parent.middle_vlayout.addWidget(qb_content, 0)



def remove_layout_widgets(parent_layout) :
    for i in reversed(range(parent_layout.count())):
        widget = parent_layout.itemAt(i).widget()
        if widget is not None:
            widget.setParent(None)


def make_news_content(news_link) :
    print('news_link : ', news_link)
    article = News_Content_Crawling(news_link)        # 뉴스 내용을 crawling해서 가져온다.
    return article


def make_news_layout(news) :
    print(news['company'])
    print(news['title'])
    print(news['info'])
    print(news['link'])
    
    company = QLabel(news['company'])
    title = QLabel(news['title'])
    info = QLabel(news['info'])
    link = QLabel(news['link'])
    company.setFont(QFont('Arial', 9))
    title.setFont(QFont('Arial', 12))
    info.setFont(QFont('Arial', 10))
    link.setFont(QFont('Arial', 9))
        
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