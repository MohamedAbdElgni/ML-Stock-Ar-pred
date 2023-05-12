from getdata import YahooFinance


data = YahooFinance('AAPL')

x = data.get_data()


print(x.head(5))
