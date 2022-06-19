import word_collect
import webbrowser
import image_collect


print('''
	██████╗ ███████╗███████╗██████╗ ███████╗███████╗ █████╗ ██████╗  ██████╗██╗  ██╗
	██╔══██╗██╔════╝██╔════╝██╔══██╗██╔════╝██╔════╝██╔══██╗██╔══██╗██╔════╝██║  ██║
	██║  ██║█████╗  █████╗  ██████╔╝███████╗█████╗  ███████║██████╔╝██║     ███████║
	██║  ██║██╔══╝  ██╔══╝  ██╔═══╝ ╚════██║██╔══╝  ██╔══██║██╔══██╗██║     ██╔══██║
	██████╔╝███████╗███████╗██║     ███████║███████╗██║  ██║██║  ██║╚██████╗██║  ██║
	╚═════╝ ╚══════╝╚══════╝╚═╝     ╚══════╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝''')

print("원하는 기능을 선택하세요.")
print("--------------------------------------------------------------------------------------")
print("1: 문자 데이터 수집, 2: 이미지 데이터 수집, 3: 수집된 문자 데이터 보기, 4: 수집된 이미지 데이터 보기, 5: 문자 데이터 초기화")
n = int(input())

if n == 1:
    word = input("수집하고 싶은 키워드를 입력하시오.(여러 단어인 경우 띄어쓰기로 구분) : ")
    count = int(input("수집하고 싶은 데이터의 수를 입력하시오.(0 = max) : "))
    keyword = word.split(" ")
    word_collect.start(keyword, count)

if n == 2:
    word = input("수집하고 싶은 키워드를 입력하시오.(여러 단어인 경우 띄어쓰기로 구분) : ")
    count = int(input("수집하고 싶은 데이터의 수를 입력하시오.(0 = max) : "))
    keyword = word.split(" ")
    image_collect.start(keyword, count)

if n == 3:
    url = "http://146.56.172.84/crawling_siyeon.php"
    webbrowser.open(url)

if n == 4:
    # to be continue...
    print("to be continue...")

if n == 5:
    # to be continue...
    word_collect.reset()