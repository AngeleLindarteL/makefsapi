import http
import json

from flask.json import JSONDecoder
from flask_cors.extension import CORS
from werkzeug.wrappers import response
import Algorithm

import Analysis
import flask_restful
from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from Algorithm import Categories, Chef, Recipes, User

app = Flask(__name__)
CORS(app)
api = Api(app)

class UserV(Resource):
    def get(self, user_id):
        userCr = User.User(user_id, "./UsersInfo")
        response = userCr.initUser()
        return jsonify({
            "code": http.HTTPStatus(200),
            "status": flask_restful.http_status_message(200),
            "response": response
        })

    def post(self, user_id):
        if request.data == "":
            return jsonify({
                "code": 400,
                "status":http.HTTPStatus(400)
            })
        incomingData = request.data.decode("utf-8")
        incomingData = incomingData.replace(r'\\"',r'\"')

        algorithmSort = Analysis.Analize(user_id,"./UsersInfo", f'''{incomingData}''')
        return jsonify({
            "recipes":algorithmSort,
            "status": 200
        })


class VRecipe(Resource):
    def get(self, user_id):
        Allids = Recipes.VRecipe(user_id, "./UsersInfo")
        Allids = Allids.getAllViewedIds()
        return jsonify({"ids":Allids})

    def post(self, user_id):
        print(request.data)
        appendRecipe = Recipes.VRecipe(user_id, "./UsersInfo")
        print("Entro la peticion")
        def checkField(toEval):
            try:
                return request.json[toEval]
            except Exception as e:
                if type(e) is KeyError:
                    return ""
                else:
                    raise TypeError()

        try:
            print("Se esta validando la peticion")
            recipeid = checkField("recipeID")
            viewedTime = checkField("viewedSeconds")
            duration = checkField("videoDuration")
            if recipeid == "" or viewedTime == "" or duration == "":
                raise KeyError()

            print("Se valido la peticion")
            appendRecipe.appendRecipe(recipeid, viewedTime, duration)
            print("Se hace return de la petición")
            return jsonify({200: flask_restful.http_status_message(200)})
        except Exception as e:
            if type(e) is KeyError:
                return jsonify({
                    "ERROR_CODE": {400: flask_restful.http_status_message(400)},
                    "DETAILS": {
                        "MSG": "Some of this Fields are Empty, check it please",
                        "recipeID": checkField("recipeID"),
                        "viewedSeconds": checkField("viewedSeconds"),
                        "videoDuration": checkField("videoDuration"),
                    }
                })
            elif type(e) is TypeError:
                print(e)
                return jsonify({
                    "ERROR_CODE": {400: flask_restful.http_status_message(400)},
                    "MSG": "Type Error, check the Fields in your JSON Request",
                    "err": str(e)
                })
        print("COÑOOOOOOOOOOOOOO"+response)


class RNVRecipe(Resource):
    def get(self, user_id):
        return jsonify(Recipes.getAllRNV(user_id, "./UsersInfo"))

    def post(self, user_id):
        def checkField(toEval):
            try:
                return request.json[toEval]
            except Exception as e:
                if type(e) is KeyError:
                    return ""
                else:
                    raise TypeError()

        try:
            recipe = Recipes.RNVRecipe(user_id, "./UsersInfo")
            recipeId = checkField("recipeID")
            if recipeId == "":
                raise KeyError()
            recipe.appendRecipe(recipeId)
            return jsonify({200: flask_restful.http_status_message(200)})
        except Exception as e:
            if type(e) is KeyError:
                return jsonify({
                    "ERROR_CODE": {400: flask_restful.http_status_message(400)},
                    "DETAILS": {
                        "MSG": "Some of this Fields are Empty, check it please",
                        "recipeID": checkField("recipeID")
                    }
                })
            elif type(e) is TypeError:
                print(e)
                return jsonify({
                    "ERROR_CODE": {400: flask_restful.http_status_message(400)},
                    "MSG": "Type Error, check the Fields in your JSON Request",
                })


class RNVERecipe(Resource):
    def get(self, user_id, rnv_id):
        searchRecipe = Recipes.RNVRecipe(user_id, "./UsersInfo")
        return jsonify({
            "data": searchRecipe.getRNVRecipe(rnv_id, "./UsersInfo"),
            "status": {
                "RESPONSE": 200,
                "MSG": flask_restful.http_status_message(200)
            }
        })

    def post(self, user_id, rnv_id):
        try:
            sumRecipe = Recipes.RNVRecipe(user_id, "./UsersInfo")
            sumRecipe.sumNVWRecipe(rnv_id, "./UsersInfo")
            return jsonify({
                "STATUS": 200,
                "MSG": flask_restful.http_status_message(200)
            })
        except KeyError as e:
            return jsonify({
                "MSG": flask_restful.http_status_message(400),
                "STATUS": 400
            })


class Chefs(Resource):
    def get(self,user_id):
        try:
            return jsonify({
                "STATUS": 200,
                "MSG": flask_restful.http_status_message(200),
                "data": Chef.Chef(user_id, "./UsersInfo").getAllChefs()
            })
        except Exception as e:
            return jsonify({
                "STATUS": 400,
                "MSG": flask_restful.http_status_message(400),
                "DETAIL": str(e)
            })

    def post(self,user_id):
        def checkField(toEval):
            try:
                return request.json[toEval]
            except Exception as e:
                if type(e) is KeyError:
                    return ""
                else:
                    raise TypeError()

        try:
            chefid = checkField("chefID")
            viewedTime = checkField("viewedTime")
            rate = checkField("rate")
            savedRecipes = checkField("savedRecipes")
            isReported = checkField("isReported")
            if chefid == "" or viewedTime == "":
                raise KeyError()
            if rate == "":
                rate = 0.0
            if savedRecipes == "":
                savedRecipes = 0
            if isReported == "":
                isReported = False

            chefToAppend = Chef.Chef(user_id,route="./UsersInfo")
            chefToAppend.appendChef(chefid,viewedTime,rate,savedRecipes,isReported)
            return jsonify({
                "RESPONSE": 200,
                "STATUS": flask_restful.http_status_message(200),
                "MSG": f"Chef ID {chefid} Created in User {user_id}"
            })
        except Exception as e:
            if type(e) is KeyError:
                return jsonify({
                    "ERROR_CODE": {400: flask_restful.http_status_message(400)},
                    "DETAILS": {
                        "MSG": "Some of this Fields are Empty, check it please",
                        "ADVISE": "Minimum Requirements [chefID,viewedTime]",
                        "chefID": checkField("chefID"),
                        "viewedTime": checkField("viewedTime"),
                        "rate": checkField("rate"),
                        "savedRecipes": checkField("savedRecipes"),
                        "isReported": checkField("isReported"),
                    }
                })
            elif type(e) is TypeError:
                print(e)
                return jsonify({
                    "ERROR_CODE": {400: flask_restful.http_status_message(400)},
                    "MSG": "Type Error, check the Fields in your JSON Request",
                    "ADVISE": "Expected Fields [chefID,viewedTime,rate,savedRecipes,isReported]",
                    "ADVISE": "Minimum Requirements [chefID, viewedTime]"
                })


class EChef(Resource):
    def get(self,user_id,chef_id):
        try:
            return jsonify({
                "RESPONSE": 200,
                "STATUS": flask_restful.http_status_message(200),
                "data": Chef.Chef(user_id,"./UsersInfo").getChefInfo(chef_id)
            })
        except Exception as e:
            return jsonify({
                "RESPONSE": 400,
                "STATUS": flask_restful.http_status_message(400),
                "data": str(e)
            })

    def post(self,user_id,chef_id):
        def checkField(toEval):
            try:
                return request.json[toEval]
            except Exception as e:
                if type(e) is KeyError:
                    return ""
                else:
                    raise TypeError()

        try:
            viewedTime = checkField("viewedTime")
            rate = checkField("rate")
            savedRecipes = checkField("savedRecipes")
            isReported = checkField("isReported")
            if viewedTime == "" or rate == "" or savedRecipes == "" or isReported == "":
                raise KeyError()

            chefSet = Chef.Chef(user_id,"./UsersInfo")
            chefSet = chefSet.setChefInfo(chef_id,viewedTime,rate,savedRecipes,isReported)
            return jsonify({
                "RESPONSE": 200,
                "STATUS": flask_restful.http_status_message(200),
                "MSG": {
                    "Info": "Modified",
                    "Res": chefSet
                }
            })
        except Exception as e:
            if type(e) is KeyError:
                return jsonify({
                    "ERROR_CODE": {400: flask_restful.http_status_message(400)},
                    "DETAILS": {
                        "MSG": "Some of this Fields are Empty, check it please",
                        "chefID": chef_id,
                        "viewedTime": checkField("viewedTime"),
                        "rate": checkField("rate"),
                        "savedRecipes": checkField("savedRecipes"),
                        "isReported": checkField("isReported"),
                    }
                })
            elif type(e) is TypeError:
                print(e)
                return jsonify({
                    "ERROR_CODE": {400: flask_restful.http_status_message(400)},
                    "MSG": "Type Error, check the Fields in your JSON Request",
                    "ADVISE": "Expected Fields [chefID,viewedTime,rate,savedRecipes,isReported]",
                })


class RCategories(Resource):
    def get(self,user_id):
        try:
            obj = Categories.Categories(user_id, "./UsersInfo")
            return jsonify({
                "STATUS": 200,
                "RESPONSE": flask_restful.http_status_message(200),
                "data": {
                    "General": obj.getAllCategories(),
                    "TopRegions": obj.getTopRegions()
                }
            })
        except Exception as e:
            return jsonify({
                "STATUS": 400,
                "RESPONSE": flask_restful.http_status_message(400),
                "MSG": str(e)
            })

    def post(self,user_id):
        def checkField(toEval):
            try:
                return request.json[toEval]
            except Exception as e:
                if type(e) is KeyError:
                    return ""
                else:
                    raise TypeError()

        try:
            region = checkField("region")
            tags = checkField("tags")
            obj = Categories.Categories(user_id, "./UsersInfo")

            if region == "" or tags == "":
                raise KeyError()

            obj.setRegionVisit(region,tags)

            return jsonify({
                "STATUS": 200,
                "RESPONSE": flask_restful.http_status_message(200),
                "MSG": f"Visit registered to Region {region} and Tags {tags}"
            })
        except Exception as e:
            if type(e) is KeyError:
                return jsonify({
                    "ERROR_CODE": {400: flask_restful.http_status_message(400)},
                    "DETAILS": {
                        "MSG": "Some of this Fields are Empty, check it please",
                        "region": checkField("region"),
                        "tags": checkField("tags")
                    }
                })
            elif type(e) is TypeError:
                print(e)
                return jsonify({
                    "ERROR_CODE": {400: flask_restful.http_status_message(400)},
                    "MSG": "Type Error, check the Fields in your JSON Request",
                    "ADVISE": "Expected Fields [region,tags]",
                })


api.add_resource(UserV, "/user/<user_id>")
api.add_resource(VRecipe, "/user/<user_id>/vr")
api.add_resource(RNVRecipe, "/user/<user_id>/rnv")
api.add_resource(RNVERecipe, "/user/<user_id>/rnv/<rnv_id>")
api.add_resource(Chefs, "/user/<user_id>/chefs")
api.add_resource(EChef, "/user/<user_id>/chefs/<chef_id>")
api.add_resource(RCategories, "/user/<user_id>/cats")

if __name__ == "__main__":
    app.run(debug=True)
