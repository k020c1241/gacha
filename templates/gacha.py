from flask import Flask, render_template, request
import random
import numpy as np

app = Flask(__name__)

#トップページ
@app.route("/")
def top():
    title = "ガチャシミュレーター"
    return render_template(
      'gacha.html',
      title=title)

#ガチャ後
@app.route('/post', methods=['POST', 'GET'])
def gacha():
    if request.method == 'POST':
        result = []
        rare = []
        if "rare" in request.form:
            title = "レアガチャを回しました"
            result = RareGacha()
            vo.price = vo.price + 100
            vo.count = vo.count + 1
        if 'rare11' in request.form:
            title = "11連ガチャを回しました！"
            result = Rare11Gacha()
            vo.price = vo.price + 1000
            vo.count = vo.count + 1
        if 'reset' in request.form:
            title = "リセットしました"
            vo.price = 0
            vo.count = 0
            result = ""
    return render_template(
        'gacha.html',
        result=result,
        rare=rare,
        title=title,
        vo=vo,
        count=vo.count,
        price=vo.price,
        N = count_list[0],
        N+ = count_list[1],
        R = count_list[2],
        R+ = count_list[3],
        SR = count_list[4],
        SR+ = count_list[5])


#レアガチャ
def RareGacha():
    image_list = []
    pick_rare = np.random.choice(cards, p=[0.33, 0.25, 0.20, 0.15, 0.05, 0.02])
    RareCount(pick_rare, count_list)
    image_list.append(ImageChoice(pick_rare))
    return image_list

#11連ガチャ
def Rare11Gacha():
    image_list = []
    for i in range(0,10):
      pick_rare = np.random.choice(cards, p=[0.0, 0.0, 0.57, 0.30, 0.10, 0.03])
      RareCount(pick_rare, count_list)
      image_list.append(ImageChoice(pick_rare))
    image_list.append(ImageChoice("SR"))
    RareCount("SR", count_list)
    return image_list   


#画像を指定してhtmlへ
def ImageChoice(pick_rare):
    image_num = PickNum(pick_rare)
    image_path = "static/images/" + pick_rare + "/" + pick_rare + str(image_num) + ".jpg"
    return image_path

#画像番号の範囲
rare_num = {"N":42, "N+":44, "R":113, "R+":98, "SR":24, "SR+":25}
def PickNum(pick_rare):
    num = np.random.randint(0,rare_num.get(pick_rare))
    return num

#累計
def RareCount(pick_rare, count_list):
  list = ["N", "N+", "R", "R+", "SR", "SR+"]
  num = list.index(pick_rare)
  count_list[num] += 1


#ガチャ回数、課金額の記録
class VO(object):
    def __init__(self):
        self._count = 0  # 回数
        self._price = 0  # 課金額

    def getcount(self):
        return self._count
    def setcount(self, count):
        self._count = count

    def getprice(self):
        return self._price
    def setprice(self, price):
        self._price = price

    count = property(getcount, setcount)
    price = property(getprice, setprice)

vo = VO()

app.run(host="0.0.0.0", debug=True)
