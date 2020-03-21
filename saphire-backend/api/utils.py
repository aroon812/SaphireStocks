from .models import Stock

def calc_52_day_average(self, ticker, date):
        s = Stock(date='2020-1-4', symbol='AAPL', name="Apple", vol=1, high=1, low=1, avg=2, open=1, close=1)
        s.save()
        s = Stock(date='2020-1-1', symbol='AAPL', name="Apple", vol=1, high=1, low=1, avg=2, open=1, close=4)
        s.save()
        s = Stock(date='2020-1-2', symbol='AAPL', name="Apple", vol=1, high=1, low=1, open=1, avg = 0, close=2)
        s.save()

        stock = Stock.objects.get(symbol=ticker, date=date)
        
        prev_date = date - datetime.timedelta(days=1)
        
        if Stock.objects.filter(symbol=ticker, date=prev_date).exists():
            prevStock = Stock.objects.get(symbol=ticker, date=prev_date)
            stock.avg = ((51 * prevStock.avg) + stock.close)/52
            print(stock.avg)
            stock.save()

        else:
            num_stocks = 0
            sum = 0
            for i in range(52):
                curDate = date - datetime.timedelta(days=i)
                
                if Stock.objects.filter(symbol=ticker, date=curDate).exists():
                    cur_stock = Stock.objects.get(symbol=ticker, date=curDate)
                    num_stocks += 1
                    sum += cur_stock.close

            stock.avg = sum / num_stocks
            print(stock.avg)
            stock.save()