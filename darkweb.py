import requests
from bs4 import BeautifulSoup
import pymysql

session = requests.session()

session.proxies['http'] = 'socks5h://localhost:9050'
session.proxies['https'] = 'socks5h://localhost:9050'

count = 0

keyword = ["drug"]

conn = pymysql.connect(
    user="root",
    passwd="871717",
    host="146.56.172.84",
    db="CRIME"
    # charset="utf-8"
)
cursor = conn.cursor()


# 실행할 때마다 다른값이 나오지 않게 테이블을 제거해두기
# cursor.execute("DROP TABLE IF EXISTS melon")
# # 테이블 생성하기
# cursor.execute("CREATE TABLE melon (NO int, title text, url text, album text)")
# #conn.commit()

def search(url):
    r = session.get(url)
    html = r.text
    soup = BeautifulSoup(html, 'html.parser')
    links = soup.find_all("a")
    for a in links:
        href = str(a.attrs['href'])
        text = a.string
        index = href.find("url=") + 4
        if "http://" in href[index:]:
            try:
                # print("---------------------------------------------------------------------------------------------")
                request = session.get(href[index:])
                html = request.text
                soup = BeautifulSoup(html, 'html.parser')
                no = count
                text = text.rstrip()
                data = soup.get_text().rstrip()
                # print(len(text))
                # print("=====================================================")
                # print(href[index:])
                # print("=====================================================")
                # print(len(data))
                # print("=====================================================")
                if len(data) < 65365 and len(text) < 65365:
                    # try:
                    sql = "INSERT INTO melon (no, title, url, album) VALUES (%s, %s, %s, %s)"
                    cursor.execute(sql, (count, text, href[index:], data))
                else:
                    print("maxlen")
                conn.commit()
            except requests.exceptions.RequestException as erra:
                print("AnyException : ", erra)


def ahmia(keyword):
    url = 'http://juhanurmihxlp77nkq76byazcldy2hlmovfu2epvl5ankdibsot4csyd.onion/search/?q='
    for word in keyword:
        url = url + word
        search(url)


def duckduckgo(keyword):
    url = 'https://duckduckgogg42xjoc72x3sjasowoarfbgcmvfimaftt6twagswzczad.onion/?q='
    for word in keyword:
        url = url + word
        search(url)

def torsearch(keyword):
    url = 'http://torchdeedp3i2jigzjdmfpn5ttjhthh5wbmda2rr3jvqjg5p77c54dqd.onion/search?query=d'
    for word in keyword:
        url = url + word
        search(url)



ahmia(keyword)

# conn.commit()
# conn.close()
