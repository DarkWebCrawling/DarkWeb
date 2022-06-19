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
    # cursor.execute("DROP TABLE IF EXISTS wordSiyeon")
    # # # 테이블 생성하기
    # cursor.execute("CREATE TABLE wordSiyeon (NO int, title text, url text, album text)")
    # conn.commit()

def reset():
    # # 실행할 때마다 다른값이 나오지 않게 테이블을 제거해두기
    open_db()
    cursor.execute("DROP TABLE IF EXISTS wordSiyeon")
    # 테이블 생성하기
    cursor.execute("CREATE TABLE wordSiyeon (NO int, title text, url text, album text)")
    conn.commit()


def search(url, count):
    r = session.get(url)
    html = r.text
    soup = BeautifulSoup(html, 'html.parser')
    links = soup.find_all("a")
    no = 0
    for a in links:
        href = str(a.attrs['href'])
        text = a.string
        if count != 0 and no >= count:
            break
        if "url=" in href:  # ahmia data parsing
            index = href.find("url=") + 4
            href = href[index:]
        if "http://" in href:
            try:
                request = session.get(href)
                html = request.text
                soup = BeautifulSoup(html, 'html.parser')
                text = text.rstrip()
                data = soup.get_text().rstrip()
                if text != "Last Week" and text != "Last Day" and text != "Last Month" and text != "Any Time":
                    if len(data) < 65535 and len(text) < 65535:
                        sql1 = "SELECT * FROM wordSiyeon where title = %s or album = %s"
                        cursor.execute(sql1, (text, data))
                        result = cursor.fetchall()
                        if len(result) == 0:
                            print("---------------------------------------------------------------------------------------")
                            print(no + 1, "번째 데이터가 수집 되었습니다.")
                            sql = "INSERT INTO wordSiyeon (no, title, url, album) VALUES (%s, %s, %s, %s)"
                            cursor.execute(sql, (no, text, href, data))
                            no += 1
                            conn.commit()
                    else:
                        print("---------------------------------------------------------------------------------------")
                        print("데이터 크기로 인한 수집 불가")
                        print("---------------------------------------------------------------------------------------")
            except requests.exceptions.RequestException as erra:
                print("---------------------------------------------------------------------------------------")
                print("잘못된 웹 페이지입니다.")
                print("---------------------------------------------------------------------------------------")


def ahmia(keyword, count):
    url = 'http://juhanurmihxlp77nkq76byazcldy2hlmovfu2epvl5ankdibsot4csyd.onion/search/?q='
    for word in keyword:
        url_ah = url + word
        print("====================================== ahmia ==========================================")
        print(word + "와 관련된 문자 데이터 수집 시작합니다.")
        search(url_ah, count)


def torsearch(keyword, count):
    url = 'http://torchdeedp3i2jigzjdmfpn5ttjhthh5wbmda2rr3jvqjg5p77c54dqd.onion/search?query='
    for word in keyword:
        url_tor = url + word
        print("===================================== torsearch =========================================")
        print(word + "와 관련된 문자 데이터 수집 시작합니다.")
        search(url_tor, count)


def start(query, count):
    socket()
    open_db()
    ahmia(query, count)
    torsearch(query, count)
    conn.close()
