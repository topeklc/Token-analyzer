from flask_restful import Resource
from src.runner import Runner


class All(Resource):
    def get(self, token: str, chain: str) -> dict:
        runner = Runner(token, chain)
        result = runner.get_all_data()
        runner.stop_analyzer()
        return result


class NameSymbol(Resource):
    def get(self, token: str, chain: str) -> dict:
        runner = Runner(token, chain)
        name, symbol = runner.get_name_symbol()
        runner.stop_analyzer()
        return {"name": name, "symbol": symbol}


class BuyTax(Resource):
    def get(self, token: str, chain: str) -> dict:
        runner = Runner(token, chain)
        result = runner.get_buy_tax()
        runner.stop_analyzer()
        return {"buy_tax": result}


class SellTax(Resource):
    def get(self, token: str, chain: str) -> dict:
        runner = Runner(token, chain)
        result = runner.get_sell_tax()
        runner.stop_analyzer()
        return {"sell_tax": result}


class TotalSupply(Resource):
    def get(self, token: str, chain: str) -> dict:
        runner = Runner(token, chain)
        result = runner.get_total_supply()
        runner.stop_analyzer()
        return {"total_supply": result}


class CirculatingSupply(Resource):
    def get(self, token: str, chain: str) -> dict:
        runner = Runner(token, chain)
        result = runner.get_circulating_supply()
        runner.stop_analyzer()
        return {"circulating_supply": result}


class MarketCap(Resource):
    def get(self, token: str, chain: str) -> dict:
        runner = Runner(token, chain)
        result = runner.get_marketcap()
        runner.stop_analyzer()
        return {"market_cap": result}


class Owner(Resource):
    def get(self, token: str, chain: str) -> dict:
        runner = Runner(token, chain)
        result = runner.get_owner()
        runner.stop_analyzer()
        return {"owner": result}
