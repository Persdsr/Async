def profit_margin(cost_price, sales_price):
    return '{:.1%}'.format((sales_price - cost_price)/sales_price)


print(profit_margin(14, 50))