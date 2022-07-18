# coding=utf8
from flask import Flask
from flask_restful import Resource, Api
from src.run import run
import os

app = Flask(__name__)
api = Api(app)


class Check(Resource):
    def get(self, token, chain):
        name, symbol, buy_tax, sell_tax, total_supply, circulating_supply, marketcap, ownership = run(token, chain)
        return {'name': name, 'symbol': symbol, 'total supply': total_supply, 'criculating supply': circulating_supply, 'marketcap': marketcap, "ownership": ownership, 'buy tax': buy_tax, 'sell tax': sell_tax}

api.add_resource(Check, '/<string:chain>/<string:token>')

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
