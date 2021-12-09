import json


class Chef:
    def __init__(self, userid,route):
        self.userid = userid
        self.chefRoute = f"{route}/U#{self.userid}/chefs.json"

    def getAllChefs(self):
        with open(self.chefRoute, "r") as chefsJson:
            jsonChefsDoc = json.load(chefsJson)
            return jsonChefsDoc

    def appendChef(self, chefid, viewedtime, rate=0.0, savedrecipes=0, isreported=False):
        jsonChefsDoc = self.getAllChefs()
        if jsonChefsDoc.get(f"{chefid}") is not None:
            return False

        with open(self.chefRoute, "w") as chefsFile:
            chefInfo = {
                "viewedtime": viewedtime,
                "rate": rate,
                "savedRecipes": savedrecipes,
                "isReported": isreported,
                "lastCountRate": 0,
                "lastRateSum": 0,
            }
            jsonChefsDoc[f"{chefid}"] = chefInfo
            json.dump(jsonChefsDoc, chefsFile, indent=4)

    def getChefInfo(self,chefid):
        with open(self.chefRoute, "r") as chefFile:
            try:
                chefinfo = json.load(chefFile)
                return chefinfo[f"{chefid}"]
            except KeyError:
                return False

    def setChefInfo(self,chefid,viewedtime=0, rate=0.0, savedRecipes=0, isreported=False):
        chefInfo = self.getChefInfo(chefid)
        if chefInfo == False:
            return False
        if viewedtime != 0:
            chefInfo["viewedtime"] += viewedtime
        if rate != 0.0:
            chefInfo["lastCountRate"] += 1
            chefInfo["lastRateSum"] += rate
            chefInfo["rate"] = float("{:.2f}".format(chefInfo["lastRateSum"] / chefInfo["lastCountRate"]))
        if savedRecipes != 0:
            chefInfo["savedRecipes"] += savedRecipes
        if isreported == True:
            chefInfo["isreported"] = True

        updatedData = self.getAllChefs()
        updatedData[f"{chefid}"] = chefInfo
        with open(self.chefRoute, "w") as chefInfo:
            json.dump(updatedData, chefInfo, indent=4)

        return updatedData[f"{chefid}"]


# Tests

"""

#Tests for Chef Handler Class

chef_Handler = Chef(12,"./Usersinfo")

chef_Handler.appendChef(1, 0, 0.0, 0, False)
chef_Handler.appendChef(12, 0, 0.0, 0, False)

print(chef_Handler.setChefInfo(14,1900,2.2,12))

print(chef_Handler.getChefInfo(14))
"""