from maag_app.orders.models import Order
from maag_app.sales.models import Sales
from maag_app.stocks.models import Stock


def get_latest_sales_report_date():
    try:
        return Sales.objects.order_by("-date").first().date
    except:
        pass


def get_latest_stock_report_date():
    try:
        return Stock.objects.order_by("-date").first().date
    except:
        pass


def get_latest_orders_report_date():
    try:
        return Order.objects.order_by("-order_date").first().order_date
    except:
        pass
