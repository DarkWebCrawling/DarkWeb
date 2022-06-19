import requests
from bs4 import BeautifulSoup
import pymysql


# counterfeit hosting porno bitcoin murder drug hack mobile weapon
# keyword = ['counterfeit', 'hosting', 'bitcoin', 'murder', 'drug', 'hack', 'mobile', 'weapon']


def socket():
    global session
    session = requests.session()

    session.proxies['http'] = 'socks5h://localhost:9050'
    session.proxies['https'] = 'socks5h://localhost:9050'


def open_db():
    global conn, cursor, url_list, num
    url_list = []
    num = 0
    conn = pymysql.connect(
        user="root",
        passwd="871717",
        host="146.56.172.84",
        db="CRIME"
        # charset="utf-8"
    )
    # 실행할 때마다 다른값이 나오지 않게 테이블을 제거해두기
    cursor = conn.cursor()

    # # 실행할 때마다 다른값이 나오지 않게 테이블을 제거해두기
    # cursor.execute("DROP TABLE IF EXISTS melon")
    # # 테이블 생성하기
    # cursor.execute("CREATE TABLE melon (NO int, title text, url text, album text)")
    # conn.commit()


def down(url, word):
    global num
    if url not in url_list:
        url_list.append(url)
        imgUrl = url
        print(imgUrl)
        if '.png' in imgUrl:
            f = open('./img/' + word + str(num) + '.png', 'wb')
        elif '.webp' in imgUrl:
            f = open('./img/' + word + str(num) + '.webp', 'wb')
        else:
            f = open('./img/' + word + str(num) + '.jpg', 'wb')
        response = session.get(imgUrl)
        f.write(response.content)
        f.close()
        print('다운로드 완료')
        num += 1


def search(url, count, word):
    r = session.get(url)
    html = r.text
    soup = BeautifulSoup(html, 'html.parser')
    links = soup.find_all("a")
    # sql1 = "SELECT COUNT(*) FROM melon"
    # cursor.execute(sql1)
    # no = cursor.fetchall()[0]
    n = 0
    for a in links:
        href = str(a.attrs['href'])
        if count != 0 and n >= count:
            break
        if "url=" in href:  # ahmia data parsing
            index = href.find("url=") + 4
            href = href[index:]
        if "http://" in href:
            try:
                request = session.get(href)
                html = request.text
                soup = BeautifulSoup(html, 'html.parser')
                img = soup.find_all('img')
                for i in img:
                    if i.get('src') is not None and 'http' in i['src']:
                        down(i['src'], word)
                    if i.get('data-src') is not None and 'http' in i['data-src']:
                        down(i['data-src'], word)
                    if i.get('srcset') is not None:
                        string_list = i.get('srcset').split()
                        if len(string_list) > 0:
                            down(string_list[0], word) # same image, different size
                    if i.get('data-large_image') is not None and 'http' in i['data-large_image']:
                        down(i['data-large_image'], word)

            except requests.exceptions.RequestException as erra:
                print("---------------------------------------------------------------------------------------")
                print("잘못된 웹 페이지입니다.")
                print("---------------------------------------------------------------------------------------")


def ahmia(keyword, count):
    url = 'http://juhanurmihxlp77nkq76byazcldy2hlmovfu2epvl5ankdibsot4csyd.onion/search/?q='
    for word in keyword:
        url_ah = url + word
        print("====================================== ahmia ==========================================")
        print(word + "와 관련된 이미지 데이터 수집 시작합니다.")
        search(url_ah, count, word)


def torsearch(keyword, count):
    url = 'http://torchdeedp3i2jigzjdmfpn5ttjhthh5wbmda2rr3jvqjg5p77c54dqd.onion/search?query='
    for word in keyword:
        url_tor = url + word
        print("===================================== torsearch =========================================")
        print(word + "와 관련된 이미지 데이터 수집 시작합니다.")
        search(url_tor, count, word)


def start(query, count):
    socket()
    open_db()
    ahmia(query, count)
    # torsearch(query, count)
    conn.close()

