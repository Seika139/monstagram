import os
from PIL import Image
import requests
from random import randint
from bs4 import BeautifulSoup
import urllib

# 必要ディレクトリの宣言
IMG_DIR = 'imgs/'
os.makedirs(IMG_DIR,exist_ok=True)


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


def main():
    nombre = randint(1,809)
    print(getImage(nombre))
    for i in getDiescription(nombre):
        print(i)

if __name__ == '__main__':
    main()
