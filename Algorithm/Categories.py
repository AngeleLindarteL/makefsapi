import json


class Categories:

    def __init__(self, uid, route):
        self.userid = uid
        self.route = f"{route}/U#{self.userid}/category.json"

    def getAllCategories(self):
        with open(self.route, "r") as allCategories:
            jsonLoaded = json.load(allCategories)
            return dict(jsonLoaded)

    def getTopRegions(self):
        regions = self.getAllCategories()
        regionView = {}
        for key in regions.keys():
            regionView[key] = regions[key]["timesVisited"]

        return dict(sorted(regionView.items(), key=lambda x: x[1], reverse=True))

    def getTopTags(self, region):
        regions = self.getAllCategories()
        regions = regions[region]
        regions.pop("timesVisited")
        return dict(sorted(regions.items(), key=lambda x: x[1], reverse=True))

    def setRegionVisit(self, region, tags=None):
        if tags is None:
            tags = []
            return False
        regions = self.getAllCategories()
        regions[region]["timesVisited"] += 1
        for tag in tags:
            regions[region][tag] += 1

        with open(self.route, "w") as categories:
            json.dump(regions, categories, indent=4)

"""
pro = Categories(14)

pro.setRegionVisit("oceania", ["Sopa", "Vegana"])
print(pro.getTopRegions())
print(pro.getTopTags("oceania"))
"""