# coding=utf8
from flask import Flask
from flask_restful import Resource, Api
from src.resources.resources import *
import os

app = Flask(__name__)
api = Api(app)


api.add_resource(All, '/<string:chain>/<string:token>/all')
api.add_resource(NameSymbol, '/<string:chain>/<string:token>/name')
api.add_resource(BuyTax, '/<string:chain>/<string:token>/buy-tax')
api.add_resource(SellTax, '/<string:chain>/<string:token>/sell-tax')
api.add_resource(TotalSupply, '/<string:chain>/<string:token>/total-supply')
api.add_resource(CirculatingSupply, '/<string:chain>/<string:token>/circulating-supply')
api.add_resource(MarketCap, '/<string:chain>/<string:token>/marketcap')
api.add_resource(Owner, '/<string:chain>/<string:token>/owner')

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
