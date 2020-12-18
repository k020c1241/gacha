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
    result = GetData("data/rarecount.txt")
    count_data = GetData("data/count.txt")
    price_data = GetData("data/price.txt")

  if "rare11" in request.form:
    title = "11連ガチャを回しました！"
    message = ""
    rare_data = GetData("data/rarecount.txt")
    count_data = GetData("data/count.txt")
    price_data = GetData("data/price.txt")

  if "comp" in request.form:
    title = "SR+コンプリート"
    message = "おめでとう！"
    result = GetData("data/srpcount.txt")
    count_data = GetData("data/count.txt")
    price_data = GetData("data/price.txt")

  if "reset" in request.form:
    title = "リセット"
    message = "リセットしました"
    result = ResetData()
  
  return render_template(
          "gacha.html",
          result = result,
          title = title,
          message = message,
          count = count_data,
          price = price_data,
          N = rare_data[0],
          Np = rare_data[1],
          R = rare_data[2],
          Rp = rare_data[3],
          SR = rare_data[4],
          SRp = rare_data[5],)

#---------------------------------------------------------#

#1連ガチャ
def RareGacha():
  result_rare = []
  weight = [0.33, 0.25, 0.20, 0.15, 0.05, 0.02]
  result_rare.append(PickupRare(weight))
  SetData("data/count.txt")
  SetData("data/price.txt")
  RareCountData(result_rare)
  return result_rare

# 11連ガチャ
def Rare11Gacha():
    result_rare = []
    weight = [0.0, 0.0, 0.57, 0.30, 0.10, 0.03]
    for i in range(0, 10):
      result_rare.append(PickupRare(weight))
      SetData("data/count.txt")
      SetData("data/price.txt")
      RareCountData(result_rare)
    result_rare.append("SR")
    SetData("data/count.txt")
    SetData("data/price.txt")
    RareCountData(result_rare)
    return result_rare

#SR+コンプガチャ
def SRpComp():
  while True:
    Rare11Gacha()
    list = GetData("data/srpcount.txt")
    if len(list) == 26:
      break


# カードを排出
def PickupRare(weight):
  cards = ["N", "N+", "R", "R+", "SR", "SR+"]
  picked_rare = np.random.choice(cards, p=weight)
  if picked_rare == "SR+":
    SRpComp(picked_rare)
  return picked_rare

#画像の決定
def PickImage(picked_rare):
  num = {"N":43, "N+":45, "R":114, "R+":99, "SR":25, "SR+":26}
  image_num = np.random.randint(0,num.get(picked_rare))
  image_path = "static/images/" + picked_rare + "/" + picked_rare + str(image_num) + ".jpg"
  return image_path

#画像リスト
def ImageHolder(image_path):
  image_holder = []
  image_holder.append(PickImage())
  return image_holder

 
#---------------------------------------------------------#

#ガチャ回数、課金額の記録
def SetData():
  with open("data/count.txt","r") as f:
    count = f.read()
    count = int(count)
    count += 1
  with open("data/price.txt","r") as f:
    price = f.read()
    price = int(price)
    price += 100
  with open("data/count.txt","w") as f:
    f.write(str(count))
  with open("data/price.txt","w") as f:
    f.write(str(price))

#レアリティごとの排出回数を記録
def RareCountData(result):
  count_list = {"N":0, "N+":0, "R":0, "R+":0, "SR":0, "SR+":0}
  dic = GetData("/data/rarecount.txt")
  dic[count_list[result]] += 1

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

#記録リセット
def ResetData():
  with open("data/count.txt","w") as f:
    f.write("0")
  with open("data/price.txt","w") as f:
    f.write("0")
  with open("data/rarecount.txt","w") as f:
    f.write("0")
  with open("data/srpcount.txt","w") as f:
    f.write("0")

#記録の取得
def GetData():
  with open("data/count.txt","w") as f:
    count = f.read()
  with open("data/price.txt") as f:
    price = f.read()
  with open("data/rarecount.txt","w") as f:
    rarecount = f.read()
  with open("data/srpcount.txt","w") as f:
    srpcount = f.read()
  return count, price,rarecount,srpcount


app.run(host="0.0.0.0", debug=True)