from flask import Flask, render_template, request
import numpy as np
import random

app = Flask(__name__)
#トップページ
@app.route("/")
def top():
    title = "ガチャシミュレーター"
    message = "ガチャを回そう！"
    return render_template('gacha.html',
                           message=message, 
                           title=title)
#ガチャ後
@app.route('/post', methods=['POST', 'GET'])
def post():
    message = ""
    if request.method == 'POST':
        result = []
        if "rare" in request.form:
            title = "レアガチャを回しました"
            result = RareGacha()
        if 'rare11' in request.form:
            title = "11連ガチャを回しました！"
            result = Rare11Gacha()
        if 'reset' in request.form:
            title = "リセットしました"
            result = ""
            message = "リセットしました"
    return render_template('gacha.html',
                            result=result, 
                            title=title,
                            message=message)


#レアガチャ
def RareGacha():
    image_list = []
    pick_rare = RareChoice()
    image_list.append(ImageChoice(pick_rare))
    return image_list
def RareChoice():
    cards = ["N","Np","R","Rp","SR","SRp"]
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
    cards = ["N","Np","R","Rp","SR","SRp"]
    return random.choices(cards,weights = [0, 0, 57, 30, 10, 3])

#画像を指定してhtmlへ
def ImageChoice(pick_rare):
   image_num = PickNum(pick_rare)
   image_path = "static/images/" + pick_rare[0] + "/" + pick_rare[0] + str(image_num[0]) + ".jpg"
   return image_path
#画像番号の範囲
def PickNum(pick_rare):
    many = []
    rare_num = 0
    if pick_rare[0] == "N":
       rare_num = 42
    elif pick_rare[0] == "Np":
       rare_num = 43
    elif pick_rare[0] == "R":
       rare_num = 113  
    elif pick_rare[0] == "Rp":
       rare_num = 98
    elif pick_rare[0] == "SR":
       rare_num = 24 
    elif pick_rare[0] == "SRp":
       rare_num = 25
    many.append(random.randint(0,rare_num))
    return many

app.run(host="0.0.0.0",debug=True)