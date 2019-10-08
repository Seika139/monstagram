from bs4 import BeautifulSoup
from datetime import datetime
import os
from PIL import Image
import pyautogui
import requests
from random import randint
import time
import urllib

from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.action_chains import ActionChains

# 必要ディレクトリの宣言
IMG_DIR = 'imgs/'
os.makedirs(IMG_DIR,exist_ok=True)

def timestamp():
    now = datetime.now()
    timestamp = f'{now.year}/{now.month:02}/{now.day:02} {now.hour:02}:{now.minute:02}:{now.second:02}'
    return timestamp

# ポケモンの画像を取得
# 引数 図鑑番号
def getImage(Nombre):
    URL = f"https://www.pokemon.jp/zukan/detail/{Nombre:03}.html"
    images = []
    soup = BeautifulSoup(requests.get(URL).content,'lxml')
    # print(soup.div.find(class_='names'))
    for link in soup.find_all("img"):
        if link.get("src").endswith(".png"):
            images.append(link.get("src"))
    target_img = images[2]
    re = requests.get("https://www.pokemon.jp"+target_img)
    png = os.path.join('imgs',f'No-{Nombre}.png')
    with open(png, 'wb') as f:
        f.write(re.content)

    # pngをjpgに変換
    pil = Image.open(png,'r')
    pil = pil.convert("RGB") #.jpgはRGB形式でないとエラーがでる
    jpg = png.split('.')[0]+'.jpg'
    pil.save(jpg,'JPEG')
    os.remove(png)
    return jpg


# ポケモンの説明文を取得
# 引数 図鑑番号
def getDiescription(Nombre):
    URL = f"https://www.pokemon.jp/zukan/detail/{Nombre:03}.html"
    html = urllib.request.urlopen(URL)
    soup = BeautifulSoup(html, "html.parser")
    div = soup.find_all("div")
    p = soup.find_all("p")

    name = ""
    for tag in p:
        try:
            string_ =tag.get("class").pop(0)
            if string_ in "name":
                name = tag.string
                break
        except:
                pass

    description = ""
    for tag in div:
        try:
            string_ = tag.get("class").pop(0)
            if string_ in "tab active":
                description = str(tag.p.string) #入れ子の表示ができる
        except:
                pass

    return name,description

def login(driver):
	time.sleep(1)

	driver.get('https://www.instagram.com/?hl=ja')

	f = open('insta.txt','a')
	f.write(timestamp() + " instagramにアクセスしました\n")
	f.close()
	time.sleep(1)

	driver.find_element_by_class_name('L3NKy      ').click() #ログインのログイン

	time.sleep(1)

	#メアドと、パスワードを入力
	driver.find_element_by_name('username').send_keys('east_bot')
	#time.sleep(1)
	driver.find_element_by_name('password').send_keys('80385070')
	#time.sleep(1)

	#ログインボタンを押す
	driver.find_element_by_xpath("/html/body/span/section/main/article/div/div/div/form/div[7]/button").click()
	#find_element_by_nameではfacebookの方に飛んでいくので絶対パスを通した。

	f = open('insta.txt','a')
	f.write(timestamp() + " instagramにログインしました\n")
	f.close()

	time.sleep(5)

	#ログイン情報を保存しますか?「あとで」をクリック
	pyautogui.click(210,610)
	time.sleep(3)

	#ホーム画面に追加しますか?「キャンセル」をクリック
	pyautogui.click(330,690)

def post1():
	pyautogui.click(205,810) #投稿ボタンをクリック
	time.sleep(2)

	pyautogui.click(210,330) #「書類」を選択
	time.sleep(2)

	pyautogui.press('right') #マウス操作ではウィンドウの下をクリックしてしまう
	time.sleep(1)
	pyautogui.press('return')
	time.sleep(1)
	pyautogui.press('right')
	time.sleep(1)
	pyautogui.press('return')
	time.sleep(1)
	pyautogui.press('right')
	time.sleep(1)
	pyautogui.press('return')
	time.sleep(1)

def post2(driver,text):
	driver.find_element_by_xpath('/html/body/span/section/div[1]/header/div/div[2]').click() #「次へ」
	time.sleep(1)

	driver.find_element_by_xpath('/html/body/span/section/div[2]/section[1]/div[1]/textarea').send_keys(text) #キャプション入力
	time.sleep(1)

	driver.find_element_by_xpath('/html/body/span/section/div[1]/header/div/div[2]').click() #share

def main():
    nombre = randint(1,809)
    print(getImage(nombre))
    name,data = getDiescription(nombre)
    txt = f"No.{nombre}{name}\n【ポケモン図鑑\n{data}\nAlpha版"
    mobile_emulation = { "deviceName": "iPhone 6" }
    options = webdriver.ChromeOptions()
    options.add_experimental_option("mobileEmulation", mobile_emulation)
    driver = webdriver.Chrome(chrome_options=options)
    login(driver)
    time.sleep(1)

    post1()
    time.sleep(1)

    post2(driver,txt)
    time.sleep(5)

    driver.close()
    time.sleep(2)
    driver.quit()

if __name__ == '__main__':
    main()
