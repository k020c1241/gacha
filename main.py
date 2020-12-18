#Save
from flask import Flask, render_template, request
import numpy as np
#import pickle
#import os
app = Flask(__name__)

cards = ["N", "N+", "R", "R+", "SR", "SR+"]
count_list = [0, 0, 0, 0, 0, 0]
SRp_count = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
#DATAFILE = "/.data.txt"

#トップページ
@app.route("/")
def top():
    title = "ガチャシミュレーター"
    message = "ガチャを回そう！！"
    return render_template(
      "gacha.html",
      title = title,
      message = message)

#ガチャ後
@app.route("/gacha", methods = ["POST", "GET"])
def gacha():
    if request.method == "POST":
      result = []
      rare = []
      """
      #データ読み込み
      if os.path.exists(DATAFILE):
        with open(DATAFILE, "rb") as f:
          obj = pickle.load(f)
          vo.prince = obj[0]
          vo.Scount = obj[1]
          vo.Ccount = obj[2]
          vo.Tcount = obj[3]
      """
      if "rare" in request.form:
          title = "レアガチャを回しました！"
          message = ""
          result = RareGacha()
          vo.price = vo.price + 100
          vo.Tcount = vo.Tcount + 1
          vo.Scount = vo.Scount + 1
          #write_txt(vo.price,vo.Scount, vo.Ccount, vo.Tcount)

      if "rare11" in request.form:
          title = "11連ガチャを回しました！"
          message = ""
          result = Rare11Gacha()
          vo.price = vo.price + 1000
          vo.Tcount = vo.Tcount + 1
          vo.Ccount = vo.Ccount + 1
          #write_txt(vo.price,vo.Scount, vo.Ccount, vo.Tcount)
        
        #if "comp" in request.form:
          #title = "SR+コンプリート"
          #message = "おめでとう！"
          #result = SRpComp(SRp_count)
          #vo.price = vo.price
          #vo.Tcount = vo.Tcount
          #vo.Ccount = vo.Ccount
          #write_txt(vo.price,vo.Scount, vo.Ccount, vo.Tcount)

      if "reset" in request.form:
          title = "リセット"
          message = "リセットしました"
          vo.price = 0
          vo.Tcount = 0
          vo.Scount = 0
          vo.Ccount = 0
          result = ""
          #write_txt(vo.price,vo.Scount, vo.Ccount, vo.Tcount)

      return render_template(
          "gacha.html",
          result = result,
          rare = rare,
          title = title,
          message = message,
          vo = vo,
          Scount = vo.Scount,
          Ccount = vo.Ccount,
          Tcount = vo.Tcount,
          price = vo.price,
          N = count_list[0],
          Np = count_list[1],
          R = count_list[2],
          Rp = count_list[3],
          SR = count_list[4],
          SRp = count_list[5])


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
"""
#SR+コンプガチャ
def SRpComp(SRp_count):
    flag = 1
    vo.price = 0
    vo.Ccount = 0
    vo.Tcount = 0    
    while flag == 1:
      if 0 in SRp_count:
        Rare11Gacha()
        vo.price += 1000
        vo.Ccount += 1
        vo.Tcount += 1
      else:
        flag = 0
"""
#画像を指定してhtmlへ
def ImageChoice(pick_rare):
    image_num = PickNum(pick_rare)
    image_path = "static/images/" + pick_rare + "/" + pick_rare + str(image_num) + ".jpg"
    if pick_rare == "SR+":
      SRp_count[image_num] += 1
    return image_path

#画像番号の範囲
rare_num = {"N":43, "N+":45, "R":114, "R+":99, "SR":25, "SR+":26}
def PickNum(pick_rare):
    num = np.random.randint(0,rare_num.get(pick_rare))
    return num

#累計
def RareCount(pick_rare, count_list):
  list = ["N", "N+", "R", "R+", "SR", "SR+"]
  num = list.index(pick_rare)
  count_list[num] += 1
"""
def WriteTxt(price,Scount,Ccount,Tcount):
  with open(DATAFILE, "wb") as f:
    d_li = []
    d_li.append(price)
    d_li.append(Scount)
    d_li.append(Ccount)
    d_li.append(Tcount)
    
    pickle.dump(d_li, f)   
"""
app.run(host="0.0.0.0", debug=True)