import json


def getAllRNV(uid, route=None):
    if route is not None:
        with open(f"{route}/U#{uid}/RecipesInfo/rnv.json", "r") as allrnv:
            return json.load(allrnv)
    else:
        with open(f"../UsersInfo/U#{uid}/RecipesInfo/rnv.json", "r") as allrnv:
            return json.load(allrnv)


class RNVRecipe:
    def __init__(self, uid, route):
        self.userid = uid
        self.dir = f"{route}/U#{self.userid}/RecipesInfo/rnv.json"
        self.route = route

    def appendRecipe(self,rid):
        with open(self.dir, "r") as rnvFile:
            appendTo = json.load(rnvFile)

        appendTo[rid] = 1

        with open(self.dir, "w") as rnvFile:
            json.dump(appendTo, rnvFile, indent=4)

    def getRNVRecipe(self,rid):
        allr = getAllRNV(self.userid,route=self.route)
        try:
            result = {
                rid: allr[f"{rid}"]
            }
            return result
        except KeyError:
            return False

    def sumNVWRecipe(self,rid):
        if self.getRNVRecipe(rid) == False:
            self.appendRecipe(rid)
            return
        allr = getAllRNV(self.userid,self.route)
        try:
            allr[f"{rid}"] += 1

            with open(self.dir, "w") as rnvFile:
                json.dump(allr, rnvFile, indent=4)
        except Exception as e:
            raise KeyError()

class VRecipe:
    def __init__(self, uid, route):
        self.userid = uid
        self.route = f"{route}/U#{self.userid}/RecipesInfo/vw.json"

    def getAllViewedIds(self):
        with open(self.route, "r") as vwInfo:
            loadedData = json.load(vwInfo)
            return list(loadedData["video_ids"])

    def getVRInfo(self):
        with open(self.route, "r") as vwInfo:
            loadedData = json.load(vwInfo)
            return loadedData

    def isViewed(self, searchId):
        data = self.getAllViewedIds()
        try:
            return data.index(searchId)
        except ValueError:
            return False

    def appendRecipe(self, rid, secs, videoduration):
        if rid == "" or secs == "" or videoduration == "":
            raise Exception()
        if self.isViewed(rid) is not False:
            return False
        try:
            data = self.getVRInfo()
            data["num"] += 1
            if data["max"] < videoduration:
                data["max"] = videoduration

            data["last_sum"] += secs
            data["avg_secs"] += data["last_sum"] / data["num"]

            data["video_ids"].append(rid)

            with open(self.route, "w") as vwData:
                json.dump(data, vwData, indent=2)
        except Exception as e:
            raise TypeError()


# Tests

"""
This are test for RecommendedNotViewedRecipe
rnvTest = RNVRecipe(14, 58992)

rnvTest.sumNVWRecipe()

print(getAllRNV(14))

print(rnvTest.getRNVRecipe())

"""

""" This are tests for Viewed Videos """

"""
vwrecipe = VRecipe(14)

print(vwrecipe.isViewed(15))

vwrecipe.appendRecipe(25,800,1580)
print(vwrecipe.getVRInfo())
vwrecipe.appendRecipe(80,800,1980)

print(vwrecipe.isViewed(15))
print(vwrecipe.isViewed(25))

print(vwrecipe.getAllViewedIds())
"""