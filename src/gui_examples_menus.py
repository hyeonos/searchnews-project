



def Run() :
    app = QApplication(sys.argv)
    
    window = MainWindow()
    window.show()       # ** Window는 기본적으로 숨겨져 있다.
    
    app.exec
    
    
    
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        
        tabs = QTabWidget()
        tabs.setDocumentMode(True)      # give slimline tabs(??) similar to what you see on other platforms
        tabs.setTabPosition(QTabWidget.TabPosition.West)
        tabs.setMovable(True)       # tab을 움직일 수 있게 만든다.
        
        for _, color in enumerate(["red", "green", "blue", "yellow"]) :
            tabs.addTab(Color(color), color)
        
        self.setCentralWidget(tabs)