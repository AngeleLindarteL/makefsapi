from flask.json import JSONDecoder
import flask_restful
from Algorithm import Categories,Chef,Recipes
import base64

def Analize(uid,route,info):
    recipes = JSONDecoder().decode(info)
    # recipes = info
    allRecipes = {}
    allTimeRelations = {}
    # n/6000pts 
    for recipe in recipes:
        recipeStatus = {
            "recipeid": recipe["recipeid"],
            "videoPer": 0,
            "chefPer": 0,
            "catPer": 0,
            "durPer": 0,
        }
        # ------------------------------------------------------------- CHEF ANALYSIS (30%) (CHEFID) 1800pts
        tmp_chef = recipe["chefid"]
        chefHandler = Chef.Chef(uid,route)
        # First at all, we got to see if the chef exist for the user
        if chefHandler.getChefInfo(tmp_chef) is False:
            recipeStatus["chefPer"] = 0
        else:
        # Now we analyze the Chef 2 User stats
            chefInfo = chefHandler.getChefInfo(tmp_chef)
            viewed = (chefInfo["viewedtime"] / 2000) * 72
            rate = (chefInfo["rate"] / 0.5) * 72
            report = 180 if chefInfo["isReported"] is True else 0
            srecipes = chefInfo["savedRecipes"] * 3.6

            recipeStatus["chefPer"] = round(viewed + rate + report + srecipes)
        # -------------------------------------------- VIDEO STAT ANALYSIS (40%) (STATUS,DURATION,RATE,VIEWS) 2400pts

        viewRanges = [
            [0,20],
            [20,50],
            [50,100],
            [100,500],
            [500,1000],
            [1000,10000],
            [10000, 20000],
            [20000, 50000],
            [50000, 100000],
            [100000,1000000]
        ]
        viewsPer = 0
        for i in range(len(viewRanges)):
            if int(recipe["views"]) > viewRanges[i][1]:
                continue
            elif int(recipe["views"]) >= viewRanges[i][0] and int(recipe["views"]) <= viewRanges[i][1]:
                viewsPer = (i+1) * 67.2
        try:
            vrate = (float(recipe["rate"]) / 0.5) * 100.8
        except ZeroDivisionError:
            vrate = 100.8
        status = 720 if recipe["status"] == "not_reported" else 0

        recipeStatus["videoPer"] = round(viewsPer + vrate + status)
        try:
            recipeStatus["durPer"] = round(float(recipe["duration"]) / Recipes.VRecipe(uid,route).getVRInfo()["avg_secs"],3)
        except ZeroDivisionError:
            recipeStatus["durPer"] = round(float(recipe["duration"]),3)

        Recipes.RNVRecipe(uid,route).sumNVWRecipe(recipe["recipeid"])

        # ------------------------------------------------------ CATEGORIES ANALYSIS (30%) (TAGS, REGION)
        
        rtags = base64.b64decode(recipe["tags"]).decode("utf-8")
        rtags = rtags.replace("[\"","")
        rtags = rtags.replace("\"]","")
        region = recipe["region"]

        categoryHandler = Categories.Categories(uid,route)
        if region != "":
            treg = categoryHandler.getTopRegions()
            ttags = categoryHandler.getTopTags(region)
            
            regTotal = 0
            for keyindex in range(len(treg)):
                if list(treg)[keyindex] == region:
                    regTotal = keyindex * 150
                    break
            
            tagTotal = 0
            for keyindex in range(len(ttags)):
                if region+list(ttags)[keyindex] == rtags:
                    regTotal = keyindex * 150
                    break
            
            recipeStatus["catPer"] = tagTotal + regTotal

        # Now we got to prepare the appending of scores
        allRecipes[recipe["recipeid"]] = {
            "recipeid": recipe["recipeid"],
            "finalScore": recipeStatus["catPer"] + recipeStatus["chefPer"] + recipeStatus["videoPer"],
            "chefid": recipe["chefid"],
            "namer": recipe["namer"],
            "rate": recipe["rate"],
            "views": recipe["views"],
            "chefname": recipe["chefname"],
            "imagen": recipe["imagen"],
            "chefpic": recipe["minpic"]
        }
        allTimeRelations[recipe["recipeid"]] = recipeStatus["durPer"]
    
    # -+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-++-+-+-+-+-+ FINAL ORDERING -+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-++-+-+-+-+-+
    
    allTimeRelations = sorted(allTimeRelations.items(), key=lambda x: x[1], reverse=True)
    try:
        criteria = 400 / len(allTimeRelations)
        count = 400
    except ZeroDivisionError as e:
        criteria = 0
        count = 400

    for timeRelPos in range(len(allTimeRelations)):
        obj = allTimeRelations[timeRelPos]
        allRecipes[obj[0]]["finalScore"] += count
        count -= criteria

    #  This modules correspondes to the final ordering and returning, the format to be ordered is
    # {'finalScore': 3108.0, 'chefid': 10, 'recipeid': 87, 'namer': 'El mejor video Increible 2', 'rate': '5.00', 'views': '1', 'chefname': 'angelxd'}

    # finalSort = dict(sorted(allRecipes.items(), key=lambda x: x[1]['finalScore'], reverse=True))
    finalSort = sorted(allRecipes.items(), key=lambda x: x[1]['finalScore'], reverse=True)
    # print(f"\n ALL RECIPES  WITH FINAL SORT \n {finalSort}")
    for el in range(len(finalSort)):
        finalSort[el] = finalSort[el][1]

    return finalSort


if __name__ == "__main__":
    # Test using a real example of our DB
    data = '''[{"recipeid":57,"chefid":10,"namer":"Como hacer \\"\\" reaL","status":"not_reported","duration":"53.084","tags":"WyJsYXRhbUdvdXJtZXQiXQ==","region":"latam","views":"2","privater":false,"chefname":"angelxd","rate":"4.50"},{"recipeid":60,"chefid":10,"namer":"Bruh inifinito en bucle por -1 hora bruh XDDDDDDDDDDDDDDDDDD","status":"not_reported","duration":"14.066667","tags":"W10=","region":"","views":"9","privater":false,"chefname":"angelxd","rate":"4.33"},{"recipeid":72,"chefid":1,"namer":"Mi primer video, suscribios :D","status":"not_reported","duration":"4.966667","tags":"WyJhc2lhVmVnYW5hIl0=","region":"asia","views":"23","privater":false,"chefname":"AngelAnimator","rate":"5.00"},{"recipeid":86,"chefid":1,"namer":"El mejor video del mundo, increible","status":"not_reported","duration":"23.266","tags":"WyJsYXRhbVRpcGljYSJd","region":"latam","views":"4","privater":false,"chefname":"AngelAnimator","rate":"4.00"},{"recipeid":87,"chefid":10,"namer":"El mejor video Increible 2","status":"not_reported","duration":"23.266","tags":"WyJsYXRhbVBvc3RyZXMiXQ==","region":"latam","views":"1","privater":false,"chefname":"angelxd","rate":"5.00"}]'''
    Analize(12,"./UsersInfo",data)