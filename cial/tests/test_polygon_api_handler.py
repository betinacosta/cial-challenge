# import pytest
# import logging
#
# from app.polygon_api_handler import PolygonAPIHandler
#
# logger = logging.getLogger("PolygonAPIHandler")
#
# @pytest.fixture
# def stocks_handler():
#     handler = PolygonAPIHandler()
#     yield handler
#
# @pytest.fixture
# def valid_stock_symbol():
#     symbol = "aapl"
#     yield symbol
#
# @pytest.fixture
# def invalid_stock_symbol():
#     symbol = "&%(#^"
#     yield symbol
#
# def test_should_return_polygon_data(stocks_handler, valid_stock_symbol):
#     polygon_data = stocks_handler.get_polygon_data(valid_stock_symbol)
#
#     assert polygon_data != {}
#
# def test_should_return_empty_polygon_data_and_log_error(stocks_handler, invalid_stock_symbol, caplog):
#     polygon_data = stocks_handler.get_polygon_data(invalid_stock_symbol)
#
#     assert polygon_data == {}
#     assert "Polygon request failed" in caplog.records[0].msg