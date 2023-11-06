import re
import requests
from bs4 import BeautifulSoup

from selenium import webdriver 
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


# 이걸 class로 만들 것인가, 아니면 function으로 만들 것인가.
def News_Crawling(word) :
    return crawling_selenium(word)




def News_Content_Crawling(link) :
    print('news content crawling...')
    
    # Chrome 옵션 설정 (headless 모드로 실행)
    chrome_options = Options()
    chrome_options.add_argument("--headless")

    # Selenium을 사용하여 Chrome 브라우저 실행
    browser = webdriver.Chrome(options=chrome_options)

    # 웹 페이지에 접속
    browser.get(link)

    # 뉴스 내용 가져오기
    content_list = []
    article = []
    
    try :
        print('first try')
        # cls = '[class*="' + cls + '"]'
        news_content = browser.find_elements(By.CSS_SELECTOR, ('[class*="article"]'))
        
        for element in news_content :
            if len(element.text) > 500 :
                article = check_article_content(element.text)
            #print(element.text)  # 요소의 텍스트 출력
    except Exception as e:
        print('no search element found by article tag, Error occured : ', e)
    
    if news_content == [] or len(article) == 0:
        print('second try')
        try :
            # cls = '[class*="' + cls + '"]'
            news_content = browser.find_elements(By.CSS_SELECTOR, ('[class*="news"]'))
            for element in news_content :
                if len(element.text) > 500 :
                    article = check_article_content(element.text)
                #print(element.text)  # 요소의 텍스트 출력
        
        except Exception as e:
            print('no search element found by article tag, Error occured : ', e)    
    
    print('================================================================')

    
    if len(article) == 0 :
        article = ['뉴스 내용을 크롤링해 오는 데 실패했습니다.', f'link : {link}']
    # Selenium 종료
    browser.quit()
    
    return article



def check_article_content(text) :
    print('check if text is article content...')
    
    final_text = []
    
    splitted_text = text.split('\n')
    
    for t in splitted_text :
        if len(t) > 50 :
            if t[-1] == '.' or t[-1] == ' ' :
                final_text.append(t)
        else :
            #print(t, '    [', t[-1], ']')
            pass
            #splitted_text.remove(t)
    
    return final_text


def crawling_selenium(word) :
    print('crawling using selenium...')
    
    # Chrome 옵션 설정 (headless 모드로 실행)
    chrome_options = Options()
    chrome_options.add_argument("--headless")

    # Selenium을 사용하여 Chrome 브라우저 실행
    browser = webdriver.Chrome(options=chrome_options)

    # 웹 페이지에 접속
    url = "https://www.google.com/search?q=" + word + "&sca_esv=577560233&tbm=nws"
    browser.get(url)

    # 페이지 내용 가져오기
    #page_source = driver.page_source
    
    news_list = []
    
    try :
        #news = browser.find_elements(By.CLASS_NAME, 'SoaBEf')      # 뉴스들 가져오기
        news_company = browser.find_elements(By.CLASS_NAME, 'MgUUmf')
        news_title = browser.find_elements(By.CLASS_NAME, 'n0jPhd')
        news_info = browser.find_elements(By.CLASS_NAME, 'GI74Re')
        #news_link = browser.find_elements(By.TAG_NAME, 'a')
        news_link = browser.find_elements(By.CLASS_NAME, 'WlydOe')
        
        for company, title, info, link in zip(news_company, news_title, news_info, news_link) :
            # print(company.text)
            # print(title.text)
            # print(info.text)
            # print(link.get_attribute('href'))
            # print("================================================================")
            news = {"company":company.text,
                    "title":title.text,
                    "info":info.text,
                    "link":link.get_attribute('href')}
            news_list.append(news)
        
        # Selenium 종료
        browser.quit()
    
    except :
        print('no search element find')

    return news_list


    # 페이지 내용 출력
    #print(page_source)

    


def crawling_beautifulsoup(word) :
    print('start news crawling from google news tab ...')
    
    # 크롤링할 웹 페이지의 URL
    # 우선 google news tab으로 들어가야 한다.
    # 구글 검색 query + 사용자 검색 단어 + news tab을 선택했을 때의 url 포함
    url = "https://www.google.com/search?q=" + word + "&sca_esv=577560233&tbm=nws"
    
    # 웹 페이지 내용을 가져옴
    res = requests.get(url)
    print("response ::: \n", res)

    if res.status_code == 200:
        # 웹 페이지 내용을 파싱
        soup = BeautifulSoup(res.text, "html.parser")
        print("soup parsed ::: \n", soup)


        '''
        print('제대로 파싱되었는지 확인! : ', soup.prettify())
        # 원하는 정보 추출
        # 예를 들어, 웹 페이지의 제목 가져오기
        # soup.find('a', attrs={"class": "Nbtn_upload"})
        # divTag = soup.find_all("div", {"class":"dr_article"})
        #test_div = soup.select("div.SoaBEf")
        test_div = soup.find_all("div")
        # BNeawe vvjwJb AP7Wnd : news title
        # lRVwie : 뉴스 기사 회사
        # 
        news_divs = soup.find_all("div", {"class" : "BNeaWe"})        # , class="SoaBEf"
        print('soup.find_all div 결과 : \n', test_div)
        print("soup.find_all 결과 : \n", news_divs)        
        '''
        
        # 다른 정보를 가져오거나 페이지 내에서 원하는 작업을 수행할 수 있습니다.
    else:
        print("요청이 실패했습니다. 상태 코드:", res.status_code)
        
        
