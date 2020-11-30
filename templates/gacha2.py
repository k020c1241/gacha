from flask import Flask, render_template, request
import random

app = Flask(__name__)
#トップページ
@app.route("/")
def top():
    title = "ガチャシミュレーター"
    return render_template('gacha2.html', 
                           title = title)
#ガチャ後
@app.route('/post', methods=['POST', 'GET'])
def gacha():
    if request.method == 'POST':
        result = []
        rare = []
        if "rare" in request.form:
            title = "レアガチャを回しました"
            result = RareGacha()
            rare = RareChoice()
            vo.price = vo.price + 100
            vo.count = vo.count + 1
            vo.card[rare[0]] = vo.card[rare[0]] + 1
        if 'rare11' in request.form:
            title = "11連ガチャを回しました！"
            result = Rare11Gacha()
            rare = Rare11Choice()
            vo.price = vo.price + 1000
            vo.count = vo.count + 1
            for i in range(0,11):
                vo.card[rare[0]] = vo.card[rare[0]] + 1
        if 'reset' in request.form:
            title = "リセットしました"
            vo.price = 0
            vo.count = 0
            vo.card = {"N":0, "N+":0, "R":0, "R+":0, "SR":0, "SR+":0} 
            result = ""
    return render_template('gacha2.html',
                            result = result,
                            rare = rare,
                            title = title,
                            vo = vo,
                            count = vo.count,
                            price = vo.price,
                            card = vo.card)


#レアガチャ
def RareGacha():
    image_list = []
    pick_rare = RareChoice()
    image_list.append(ImageChoice(pick_rare))
    return image_list
def RareChoice():
    cards = ["N","N+","R","R+","SR","SR+"]
    return random.choices(cards,weights = [33, 25, 20, 15, 5, 2])
#11連ガチャ
def Rare11Gacha():
    image_list = []
    for i in range(0,10):
       PickRare = Rare11Choice()
       image_list.append(ImageChoice(PickRare))
    last = ["SR"]
    image_list.append(ImageChoice(last))
    return image_list 
def Rare11Choice():
    cards = ["N","N+","R","R+","SR","SR+"]
    return random.choices(cards,weights = [0, 0, 57, 30, 10, 3])

#画像を指定してhtmlへ
def ImageChoice(pick_rare):
   image_num = PickNum(pick_rare)
   image_path = "static/images/" + pick_rare[0] + "/" + pick_rare[0] + str(image_num[0]) + ".jpg"
   return image_path
#画像番号の範囲
def PickNum(pick_rare):
    list = []
    rare_num = 0
    if pick_rare[0] == "N":
       rare_num = 42
    elif pick_rare[0] == "N+":
       rare_num = 44
    elif pick_rare[0] == "R":
       rare_num = 113  
    elif pick_rare[0] == "R+":
       rare_num = 98
    elif pick_rare[0] == "SR":
       rare_num = 24 
    elif pick_rare[0] == "SR+":
       rare_num = 25
    list.append(random.randint(0,rare_num))
    return list

#ガチャ回数、課金額の記録
class VO(object):
    def __init__(self):
        self._count = 0 # 回数
        self._price = 0 # 課金額
        self._card = {"N":0, "N+":0, "R":0, "R+":0, "SR":0, "SR+":0} #排出カード
    
    def getcount(self):
        return self._count
    def setcount(self, count):
        self._count = count

    def getprice(self):
        return self._price
    def setprice(self, price):
        self._price = price
    
    def getcard(self):
        return self._card
    def setcard(self, card):
        self._card = card

    count = property(getcount, setcount)
    price = property(getprice, setprice)
    card = property(getcard, setcard)
vo = VO()

app.run(host="0.0.0.0",debug=True)