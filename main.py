from flask import Flask, render_template, request
import random
import numpy as np
cards = ["N", "N+", "R", "R+", "SR", "SR+"]
count_list = [0, 0, 0, 0, 0, 0]
SRp_count = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

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
            vo.Tcount = vo.Tcount + 1
            vo.Scount = vo.Scount + 1
            msg = SRpComp()
        if 'rare11' in request.form:
            title = "11連ガチャを回しました！"
            result = Rare11Gacha()
            vo.price = vo.price + 1000
            vo.Tcount = vo.Tcount + 1
            vo.Ccount = vo.Ccount + 1
            msg = SRpComp()
        if 'reset' in request.form:
            title = "リセットしました"
            vo.price = 0
            vo.Tcount = 0
            vo.Scount = 0
            vo.Ccount = 0
            result = ""
            msg = SRpComp()
        """"
        if 'aa' in request.form:
            title = "debug"
            result = debugfunc()
            vo.price = vo.price + 1000
            vo.count = vo.count + 1
            msg = SRpComp()
          """
    return render_template(
        'gacha.html',
        result=result,
        rare=rare,
        title=title,
        vo=vo,
        Scount=vo.Scount,
        Ccount=vo.Ccount,
        Tcount=vo.Tcount,
        price=vo.price,
        msg = msg,
        debug = SRp_count,
        N = count_list[0],
        Np = count_list[1],
        R = count_list[2],
        Rp = count_list[3],
        SR = count_list[4],
        SRp = count_list[5])


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
""""
#debug:SR+コンプ
def debugfunc():
    image_list = []
    for i in range(25):
      RareCount("SR+", count_list)
      image_list.append(ImageChoice("SR+"))
    return image_list 
"""

#画像を指定してhtmlへ
def ImageChoice(pick_rare):
    image_num = PickNum(pick_rare)
    image_path = "static/images/" + pick_rare + "/" + pick_rare + str(image_num) + ".jpg"
    if pick_rare == "SR+":
      SRp_count[image_num] += 1
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
#SRカウント
def SRpComp():
  msg = ""
  if 0 in SRp_count:
    pass
  else:
    msg ="SR+を全て獲得しました！！"
  return msg

#ガチャ回数、課金額の記録
class VO(object):
    def __init__(self):
        self._Scount = 0 # 単発回数
        self._Ccount = 0 # 連続回数
        self._Tcount = 0 #合計回数
        self._price = 0  # 課金額

    def get_Scount(self):
        return self._Scount
    def set_Scount(self, Scount):
        self._Scount = Scount

    def get_Ccount(self):
        return self._Ccount
    def set_Ccount(self, Ccount):
        self._Ccount = Ccount

    def get_Tcount(self):
        return self._Tcount
    def set_Tcount(self, Tcount):
        self._Tcount = Tcount

    def get_price(self):
        return self._price
    def set_price(self, price):
        self._price = price

    Scount = property(get_Scount, set_Scount)
    Ccount = property(get_Ccount, set_Ccount)
    Tcount = property(get_Tcount, set_Tcount)
    price = property(get_price, set_price)

vo = VO()

app.run(host="0.0.0.0", debug=True)
