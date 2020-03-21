from .models import Stock
import datetime

def calc_52_day_average(ticker, date):
        stock = Stock.objects.get(symbol=ticker, date=date)

        date = datetime.datetime.strptime(date, '%Y-%m-%d')
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