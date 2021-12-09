import os
import json

class User:
    """
    This is a class for interact with user files only
    (ONLY SHOULD BE USED FOR DIRS)
    """
    def __init__(self, userid,dir):
        self.userid = str(userid)
        self.userDir = f"{dir}/U#{userid}"
        self.userRecipesDir = self.userDir + "/RecipesInfo"

    def createUserDirs(self):
        try:
            # Creation of user root dir
            os.mkdir(self.userDir)
            # Creation of recipes dir
            os.mkdir(self.userRecipesDir)
        except OSError:
            return False

    def createUserCategories(self):
        tags = ["Sopa", "Vegana", "Gourmet", "Postres", "Casero", "Tipica"]
        regions = ["latam","asia","norteA","europa","africa","oceania"]
        categoryFile = self.userDir+"/category.json"

        # Writes the category JSON File for a New User
        with open(categoryFile, "w") as categories:
            categoriesDict = {}
            for region in regions:
                categoriesDict[region] = {"timesVisited": 0}
                for tag in tags:
                    categoriesDict[region][tag] = 0

            json.dump(categoriesDict,categories,indent=4)

    def createUserChefs(self):
        chefsDir = self.userDir + "/chefs.json"
        with open(chefsDir, "w") as chefs:
            json.dump({}, chefs)

    def createUserRecipes(self):
        recommendedNotViewed = self.userRecipesDir + "/rnv.json"
        viewedRecipes = self.userRecipesDir + "/vw.json"

        with open(recommendedNotViewed,"w") as rnv, open(viewedRecipes, "w") as vw:
            json.dump({},rnv)
            json.dump({
                "avg_secs": 300,
                "last_sum": 0,
                "max": 0,
                "num": 0,
                "video_ids": []
            },vw,indent=4)

    def getUserDir(self):
        return os.path.exists(self.userDir)

    def initUser(self):
        if self.getUserDir() is False:
            self.createUserDirs()
            self.createUserChefs()
            self.createUserCategories()
            self.createUserRecipes()
            return True
        else:
            return False
