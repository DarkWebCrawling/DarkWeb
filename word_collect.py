import requests
from bs4 import BeautifulSoup
import pymysql


# keyword = ['counterfeit', 'hosting', 'bitcoin', 'murder', 'drug', 'hack', 'mobile', 'weapon']


def socket():
    global session
    session = requests.session()

    session.proxies['http'] = 'socks5h://localhost:9050'
    session.proxies['https'] = 'socks5h://localhost:9050'


def open_db():
    global conn, cursor
    conn = pymysql.connect(
        user="root",
        passwd="871717",
        host="146.56.172.84",
        db="CRIME"
        # charset="utf-8"
    )

    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS wordSiyeon")
    # # 테이블 생성하기
    cursor.execute("CREATE TABLE wordSiyeon (NO int, title text, url text, album text)")
    conn.commit()


# # 실행할 때마다 다른값이 나오지 않게 테이블을 제거해두기
# cursor.execute("DROP TABLE IF EXISTS melon")
# # 테이블 생성하기
# cursor.execute("CREATE TABLE melon (NO int, title text, url text, album text)")
# conn.commit()


def search(url):
    r = session.get(url)
    html = r.text
    soup = BeautifulSoup(html, 'html.parser')
    links = soup.find_all("a")
    no = 0
    for a in links:
        href = str(a.attrs['href'])
        text = a.string
        if "url=" in href:  # ahmia data parsing
            index = href.find("url=") + 4
            href = href[index:]
        if "http://" in href:
            try:
                print("---------------------------------------------------------------------------------------")
                request = session.get(href)
                html = request.text
                soup = BeautifulSoup(html, 'html.parser')
                text = text.rstrip()
                print(text)
                data = soup.get_text().rstrip()
                if text != "Last Week" and text != "Last Day" and text != "Last Month" and text != "Any Time":
                    if len(data) < 65535 and len(text) < 65535:
                        sql1 = "SELECT * FROM wordSiyeon where title = %s or album = %s"
                        cursor.execute(sql1, (text, data))
                        result = cursor.fetchall()
                        if len(result) == 0:
                            print(no + 1, "번째 데이터가 수집 되었습니다.")
                            sql = "INSERT INTO wordSiyeon (no, title, url, album) VALUES (%s, %s, %s, %s)"
                            cursor.execute(sql, (no, text, href, data))
                            no += 1
                            conn.commit()
                    else:
                        print("maxlen")
            except requests.exceptions.RequestException as erra:
                print("AnyException : ", erra)


def ahmia(keyword):
    url = 'http://juhanurmihxlp77nkq76byazcldy2hlmovfu2epvl5ankdibsot4csyd.onion/search/?q='
    for word in keyword:
        url_ah = url + word
        print(word)
        search(url_ah)


def torsearch(keyword):
    url = 'http://torchdeedp3i2jigzjdmfpn5ttjhthh5wbmda2rr3jvqjg5p77c54dqd.onion/search?query='
    for word in keyword:
        url_tor = url + word
        print(word)
        search(url_tor)


def start(query):
    socket()
    open_db()
    ahmia(query)
    # torsearch(query)
    conn.close()
