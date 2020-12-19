from flask import Flask, render_template, request
import numpy as np

app = Flask(__name__)

#トップページ
@app.route("/")
def top():
  title = "ガチャシミュレーター"
  message = "ガチャを回そう！！"
  return render_template(
    "gacha.html",
    title = title,
    message = message)

#ガチャ実行
@app.route("/gacha", methods = ["POST", "GET"])
def gacha():
  if "rare" in request.form:
    title = "レアガチャを回しました！"
    message = ""
    result = RareGacha()
    countData_list,price_data,rare_data = GetData()

  if "rare11" in request.form:
    title = "11連ガチャを回しました！"
    message = ""
    result = Rare11Gacha()
    countData_list,price_data,rare_data = GetData()

  if "reset" in request.form:
    title = "リセット"
    message = ResetData()
    countData_list = [0,0]
    price_data = 0
    rare_data = [0,0,0,0,0,0]
    result = ""
  
  return render_template(
          "gacha.html",
          result = result,
          title = title,
          message = message,
          count_sum = countData_list[0] + countData_list[1],
          count1 = countData_list[0],
          count11 = countData_list[1],
          price = price_data,
          N = rare_data[0],
          Np = rare_data[1],
          R = rare_data[2],
          Rp = rare_data[3],
          SR = rare_data[4],
          SRp = rare_data[5])

#---------------------------------------------------------#

#1連ガチャ
def RareGacha():
  result_rare = []
  weight = [0.33, 0.25, 0.20, 0.15, 0.05, 0.02]
  pick_rare = PickupRare(weight)
  result_rare.append(PickImage(pick_rare))
  SetData("1ren")
  RareCountData(pick_rare)

  return result_rare

# 11連ガチャ
def Rare11Gacha():
    result_rare = []
    weight = [0.0, 0.0, 0.57, 0.30, 0.10, 0.03]
    for i in range(0, 10):
      pick_rare = PickupRare(weight)
      result_rare.append(PickImage(pick_rare))
      RareCountData(pick_rare)
    result_rare.append("SR")
    result_rare.append(PickImage("SR"))
    RareCountData("SR")
    SetData("11ren")
    return result_rare

# カードを排出
def PickupRare(weight):
  cards = ["N", "N+", "R", "R+", "SR", "SR+"]
  picked_rare = np.random.choice(cards, p=weight)
  return picked_rare

#画像の決定
def PickImage(picked_rare):
  num = {"N":43, "N+":45, "R":114, "R+":99, "SR":25, "SR+":26}
  image_num = np.random.randint(0,num.get(picked_rare))
  image_path = "static/images/" + picked_rare + "/" + picked_rare + str(image_num) + ".jpg"
  return image_path

#---------------------------------------------------------#

#ガチャ回数、課金額の記録
def SetData(ren):
  count_list = [] 
  with open("data/count.txt") as f: 
    data = f.readlines()
    for i in data:
      count_list.append(int(i.strip()))

  if ren == "1ren":
    with open("data/count.txt","r") as f:
        count_list[0] += 1
    with open("data/price.txt","r") as f:
        price = f.read()
        price = int(price)
        price += 100
  else:
    with open("data/count.txt","r") as f:
        count_list[1] += 1
    with open("data/price.txt","r") as f:
        price = f.read()
        price = int(price)
        price += 1000

  with open("data/count.txt","w") as f:
    f.write(str(count_list[0]) + "\n")
    f.write(str(count_list[1]))
  with open("data/price.txt","w") as f:
    f.write(str(price))


#レアリティごとの排出回数を記録
def RareCountData(pick_rare):
  rareIndex_dic = {"N":0, "N+":1, "R":2, "R+":3, "SR":4, "SR+":5}
  rarecount_list = []
  with open("data/rarecount.txt") as f: ##テキストファイルのデータをリストに変形
    data = f.readlines()
    for i in data:
      rarecount_list.append(int(i.strip()))
  rarecount_list[rareIndex_dic[pick_rare]] += 1
  with open("data/rarecount.txt", mode = "w") as f: ##リストをテキストファイルに保存
    f.write(str(rarecount_list[0]) + "\n")
    f.write(str(rarecount_list[1]) + "\n")
    f.write(str(rarecount_list[2]) + "\n")
    f.write(str(rarecount_list[3]) + "\n")
    f.write(str(rarecount_list[4]) + "\n")
    f.write(str(rarecount_list[5]))
  
""""
#引いたSR+を記録
def SRpHolder(result_rare):
  srp_list = GetData("data/srpcount.txt")
  if result_rare in srp_list:
    pass
  else:
    srp_list.append(result_rare)
  with open("data/srpcount.txt", "w") as f:
    f.write(srp_list)
  return srp_list
"""

#記録リセット
def ResetData():
  with open("data/count.txt","w") as f:
    f.write("0"+ "\n")
    f.write("0")
  with open("data/price.txt","w") as f:
    f.write("0")
  with open("data/rarecount.txt","w") as f:
    f.write("0" + "\n")
    f.write("0" + "\n")
    f.write("0"+ "\n")
    f.write("0"+ "\n")
    f.write("0"+ "\n")
    f.write("0")
  return "リセットしました。"


#記録の取得
def GetData():
  countData_list = []
  with open("data/count.txt") as f:
    data = f.readlines()
    for i in data:
      countData_list.append(int(i.strip()))
  print(countData_list,"aaaaaaaaaaaaaa")
  with open("data/price.txt") as f:
    price = f.read()
  rarecount_list = []
  with open("data/rarecount.txt") as f:
    data = f.readlines()
    for i in data:
      rarecount_list.append(int(i.strip()))
  return countData_list, price,rarecount_list


app.run(host="0.0.0.0", debug=True)