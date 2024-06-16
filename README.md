# Scrapper
![](https://velog.velcdn.com/images/sohyeonos248/post/8bfd0070-7151-4b8b-8a48-f89009843880/image.png)

사용자로부터 검색 키워드를 받아  구글 뉴스를 크롤링하여 보여 주는 프로그램

---

## 개발 기간
23.10.20 ~ 23.11.01


<br>

## Tech Stack
- Python 3.11
- PyQt6 (GUI)
- selenium (크롤링)
- sqlite3 (Database)



<br>

## Functions
-  **검색 키워드를 받아 구글 뉴스 크롤링**
    1. 사용자가 원하는 뉴스 토픽을 검색할 수 있도록 검색 창을 생성한다.
    2. '검색'버튼 옆의 '음성'버튼을 클릭하면 사용자의 음성을 인식해서 검색 키워드 입력도 가능하다.
    3. 사용자가 토픽 입력 후 검색버튼(또는 Enter키)을 누르면 가운데 화면에 검색 결과가 가져와진다.
![image](https://github.com/hyeonos/searchnews-project/assets/79961865/86cf8716-2c3e-46a3-86de-9dd42f56b0a0)

    4. 관심있는 뉴스를 클릭하면 뉴스를 작성한 회사, 뉴스의 제목, 뉴스의 내용이 가운데 화면에 뜬다. 뉴스를 스크랩할 수 없으면 뉴스의 링크를 띄운다.
![image](https://github.com/hyeonos/searchnews-project/assets/79961865/26fb6f16-d23c-46b7-a3ed-ec18bdb993c5)

    5. '뒤로 가기'를 누르면 이전 화면으로 돌아간다.


- **관심있는 뉴스를 스크랩**
    1. 관심있는 뉴스를 클릭하면, 뉴스의 여러 내용과 함께 아래에 '스크랩' 버튼이 생성된다.
    2. '스크랩'을 누르면 기사 내용이 내부 데이터베이스에 저장된다. 데이터베이스의 변경은 즉시 저장(commit)되기 때문에 프로그램을 종료, 재시작하여도 스크랩한 뉴스가 삭제되지 않는다.
![image](https://github.com/hyeonos/searchnews-project/assets/79961865/c63d840e-d505-409a-802b-f0cf2ad870d7)
![image](https://github.com/hyeonos/searchnews-project/assets/79961865/52d74a50-5b6f-4d8e-8915-db2aa5db716c)





<br>

## Run
```cmd
python main.py
```


<br>

## 회고

Python으로 GUI 기능까지 넣어 프로그램을 구현한 건 이번이 처음인데, 여러 가지 기능을 넣어서 볼 만한 소프트웨어가 나온 것 같아 뿌듯했다. 크롤링 기능을 추가하면서 웹 사이트의 HTML 언어들을 간접적으로 복습하고, 사이트마다 다르게 구성되어 있는 태그들을 활용할 방법까지 고민해 볼 수 있었다. 또한 Python에서 GUI 기능을 새롭게 접하면서 코드로 시각화하는 방법에 관심도 많이 생겼다. 앞으로 프로그램의 완성도를 높이기 위해 GUI 기능까지 구현할 생각이다.

<br>

### 📝 해당 프로젝트를 진행하며 배운 점

1. **GUI 기능**으로 프로그램을 시각적으로 사용성 있게 **디자인**하는 경험을 해 봄
    - **PyQt6**를 사용하여 프로그램 내에서 뉴스를 검색하고 저장할 수 있도록 인터페이스 구현
    - GUI를 사용하기 위해 요소 모듈의 분류와 계층 구성을 공부함
2. **크롤링 기능**을 사용하여 쉽게 인터넷에서 정보를 받아와 **자동화**할 수 있음
    - 뉴스 뿐만 아닌 주식, 외화 환율 등 **실시간 변동이 있는 정보들을 자동으로 업데이트**하는 알고리즘 구축 가능
3. **sqlite3** 라이브러리를 사용하여 **데이터베이스 관리**를 할 수 있음
    - 체계적인 데이터 관리를 해야 하는 경우 데이터베이스를 관리하는 기능이 필요
    - sqlite3로 직접 DB와 연결하고 query문을 작성해서 데이터를 저장하고 가져오는 기능을 구현해 봄
4. 구글 Speech to Text 처럼 좋은 기능을 가진 **여러 가지 API를 활용해 보자**
    - 소프트웨어는 **모듈의 집합**으로, 미리 구현되어 있는 기능을 가져오는 것도 중요한 능력
    - 구글 외에도 OpenAI, 네이버 같은 곳에서 많은 기능의 API를 배포하고 있으므로, 필요한 기능이 있다면 탐색 후 사용

<br>

### 💬 발생했던 어려움과 해결 방법

1. 눈에 보이는 GUI 기능 내부를 코드로 구현하는 것이 쉽지 않았음
    - Python으로 GUI 기능을 사용해 보는 것은 처음이었기 때문에 Window의 개념부터 시작
        - **Window와 Layout, Widget 요소들로 화면 구성**
        - 실질적인 기능을 하는 것은 Widget들인데, 이들만 절대 위치로 정렬하기에는 어렵고 비효율적이었음
        - 그래서 Layout을 사용하기로 하였으나, **Layout을 여러 개 사용하면서 Widget이 묻히거나 정렬되지 않는 문제** 발생
        - GUI 기능들은 기본적으로 **계층 구도**가 존재했고, Layout 안에 Widget을 정렬, 배치하는 방식으로 수행
    - 초기에는 자료가 많이 있는 PyQt5 버전을 사용했으나, PyQt5가 실행되지 않는 오류가 지속되어 가장 최신 버전인 PyQt6으로 업그레이드
    - 참고할 자료가 충분치 않은 PyQt6 버전을 사용하며 **공식 문서를 참고**하면서 구현 도중 **디버깅, print문으로 확인**하는 방식으로 프로그래밍 진행
2. **웹페이지마다 다른 HTML 구조**로 원하는 내용을 크롤링하기 까다로웠음
    - 다수의 홈페이지가 `<class="article">` 태그로 그룹화된 곳에 기사 내용이 담겨 있었으나, `"news"`로, 또는 그 외 다른 단어나 `<p>`, `<div>` 태그 사이에 지정되어 있는 곳도 존재
    - 기사 내용이 중간에 끊기는 형태로 구성되거나 읽어올 수 없는 이미지 형태로 되어 있는 사이트도 존재
    - 독특한 구성을 띄고 있어 지정할 수 없다면 try-exception 처리 후 받아온 내용의 길이가 0인지 검사하여 크롤링 실패 결과 출력

