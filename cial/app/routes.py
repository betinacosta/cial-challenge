import logging
import json

from app.stocks_handler import StocksHandler
from app.app import app

@app.route("/stocks/<string:stock_symbol>", methods=["GET"])
def get_stocks(request, stock_symbol):
    stocks_handler = StocksHandler(stock_symbol)
    stocks = stocks_handler.parse_get_stocks()

    if stocks:
        request.setResponseCode(200)
        return stocks
    request.setResponseCode(404)
    return f"No data found for stock_symbol {stock_symbol}"

@app.route("/stocks/", methods=["POST"])
def post_stock(request):
    content = json.loads(request.content.read())
    stock_symbol = content.get("stock_symbol")
    amount = content.get("amount")

    if not stock_symbol or not amount:
        request.setResponseCode(400)
        return 'Missing required fields. Required: "amount:float" and "stock_symbol:str"'
    try:
        amount = float(amount)
    except ValueError:
        request.setResponseCode(400)
        return 'Amount has invalid data. Must be a numerical type'

    stocks_handler = StocksHandler(stock_symbol)
    response = stocks_handler.parse_post_stocks(amount)

    request.setResponseCode(response)

    if response == 500:
        return "Internal server error"

    return f"“{amount} units of stock {stock_symbol} were added to your stock record"

def get_request_errors(request) -> str:
    content = json.loads(request.content.read())

    if not content.get("stock_symbol") or content.get("amount"):
        return 'Missing required fields. Required: "amount:float" and "stock_symbol:str"'
    try:
        float(content.get("amount"))
    except ValueError:
        return 'Amount has invalid data. Must be a numerical type'

    return ""
