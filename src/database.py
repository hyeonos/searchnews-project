import sqlite3




class ScrapDB() :
    
    def __init__(self) :
        print("DB 초기화, 불러오기.")
        self.create_table()
        
    
    def create_table(self) :
        print("DB가 생성됩니다.")
        conn = self.get_db_connection()
        cursor = conn.cursor()      # cursor를 기반으로 query문을 날릴 수 있게 됨
        sql = f"CREATE TABLE IF NOT EXISTS news_scraps (id INTEGER PRIMARY KEY AUTOINCREMENT, company TEXT, title TEXT, content TEXT)"
        cursor.execute(sql)
        conn.commit()
        conn.close()        # 여기까지 하면 DB가 만들어지는 query문까지 작성한 것.
        

    def read_scrap(self) :
        print('DB로부터 스크랩된 뉴스가 있는지 긁어오기')
        conn = self.get_db_connection()
        cursor = conn.cursor()
        sql = "SELECT * FROM news_scraps"
        cursor = conn.execute(sql)     # 수습기간 -> 이거 없애주세영?
        results = cursor.fetchall()
        
        return results
    

    def add_scrap(self, company, title, content):
        conn = self.get_db_connection()
        cursor = conn.cursor()
        #sql = f"""INSERT INTO news_scraps (company, title, content) VALUES ('{company}', '{title}', '{content}')"""
        
        sql = "INSERT INTO news_scraps (company, title, content) VALUES (?, ?, ?)"
        cursor.execute(sql, (company, title, content))
        print(sql)
        #cursor.execute(sql) # 실행해
        conn.commit() # 반영해
        conn.close()
    
    
    
    # DB랑 연결하는 것.
    def get_db_connection(self):
        conn = sqlite3.connect('scrap_database.db')
        conn.row_factory = sqlite3.Row
    
        return conn
    



def save_scrap() :
    print("뉴스를 scrap합니다.")