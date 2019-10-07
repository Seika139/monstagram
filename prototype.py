"""スマホ版"""
import time
import random
import requests
import schedule
import pyautogui
import urllib.request, urllib.error
import urllib.parse
from tqdm import tqdm
from PIL import Image
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.action_chains import ActionChains

def image(N):
    URL = "https://www.pokemon.jp/zukan/detail/"+N+".html"
    images = []
    soup = BeautifulSoup(requests.get(URL).content,'lxml')
    for link in soup.find_all("img"):
        if link.get("src").endswith(".png"):
            images.append(link.get("src"))

    X = images[2]
    re = requests.get("https://www.pokemon.jp"+X)
    with open('/Users/metagurosu/Documents/test/' + X.split('/')[-1], 'wb') as f:
        f.write(re.content)

    y = X.split('/')[-1]
    return y

def description(N):
    url = "https://www.pokemon.jp/zukan/detail/"+N+".html"
    html = urllib.request.urlopen(url)
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

    syoukai = ""
    for tag in div:
        try:
            string_ = tag.get("class").pop(0)
            if string_ in "tab active":
                syoukai = str(tag.p.string) #入れ子の表示ができる
        except:
                pass

    return name,syoukai

def login(driver):
	time.sleep(1)

	driver.get('https://www.instagram.com/?hl=ja')

	f = open('insta.txt','a')
	f.write("instagramにアクセスしました\n")
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
	f.write("instagramにログインしました\n")
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

def job():
	n = random.randint(1,809)
	N = '%03d'%n
	y = image(N)
	pil_img = Image.open('/Users/metagurosu/Documents/test/'+y,'r')
	pil_img = pil_img.convert("RGB") #.jpgはRGB形式でないとエラーがでる
	pil_img.save('/Users/metagurosu/Documents/aaa_test/a.jpg', 'JPEG') #.jpgでaaa_testファイルに保存

	name,data = description(N)
	txt = "No."+N+"  "+name+"\n"+"【ポケモン図鑑】\n"+data+"\n\nAlpha版"

	mobile_emulation = { "deviceName": "iPhone 6" }
	options = webdriver.ChromeOptions()
	options.add_experimental_option("mobileEmulation", mobile_emulation)
	driver = webdriver.Chrome(executable_path='/Users/metagurosu/Downloads/chromedriver', chrome_options=options)

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
	#schedule.every(3).minutes.do(job)
	schedule.every().day.at("00:00").do(job)
	#schedule.every(1).hours.do(job)

	while True:
		schedule.run_pending()
		time.sleep(1)
