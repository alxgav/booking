#!/usr/bin/python
# -*- coding: utf-8 -*-
from datetime import date, timedelta, datetime
from bs4 import BeautifulSoup
import calculate, parsing, pandas, requests, json, time, os
import pytz
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email import Encoders

# begin const 
datenow = datetime.now(pytz.timezone('Europe/Berlin'))
date365 = datenow + timedelta(30)
url = 'https://api.beds24.com/json/getRoomDates' #get room avilable
data_hotel = []
# end const
# get list of dates in period
def getListOfDates(date1='2019-01-31', date2='2019-01-31'):
    listdays = []
    start = datetime.strptime(date1, '%Y-%m-%d')
    end = datetime.strptime(date2, '%Y-%m-%d')
    step = timedelta(days=1)
    while start <= end:
        listdays.append(start.date())
        start += step
    return listdays

# get avilabel rooms
def getRooms(d1, d2):
        params = {'authentication': {'apiKey':'testtesttesttesttest', 'propKey':'66197apitest66197apitest'},'roomId':'154156','from':d1.strftime('%Y%m%d'),'to':d2.strftime('%Y%m%d')}
        data = requests.post(url, data = json.dumps(params))
        list_days = getListOfDates(d1.strftime('%Y-%m-%d'), d2.strftime('%Y-%m-%d'))
        days = 1
        prices = {}
        
        with open('templates/hotel.json') as json_file:
                data_json = json.load(json_file)

        for i in list_days:
                room = data.json()[str(i.strftime('%Y%m%d'))]['i']
                date = i.strftime('%Y-%m-%d')
                # print (room, date)
                prices = parsing.parse_all(str(i), str(i + timedelta(1)))
                price = []
                try:
                    price.append(int(prices['H1']))
                except:
                    price.append(0)
                try:
                   price.append(int(prices['H4']))
                except:
                    price.append(0)
                try:
                   price.append(int(prices['H2']))
                except:
                    price.append(0)   
                try:
                   price.append(int(prices['H5']))
                except:
                    price.append(0)
                try:
                    price.append(int(prices['H6']))
                except:
                    price.append(0)    
                while len(price) < 5:
                       price.append(0)
                # print price 
                calc = calculate.Calculate(price)
                n_price = int(calc.newPrice(room, days, calc.rate(calc.min(),calc.mid()), calc.min(), calc.mid(), calc.SoldOutRate(), calc.max()))
                prices.update({'room': room})
                prices.update({'rate': calc.rate(calc.min(),calc.mid())})
                prices.update({'mid': calc.mid()})
                prices.update({'min': calc.min()})
                prices.update({'market': calc.SoldOutRate()})
                prices.update({'days': days})
                prices.update({'my_price': n_price})
                # print n_price
                data_json['dates'][i.strftime('%Y%m%d')] = {'p1': str(n_price)}
                days +=1
                # time.sleep(2)
                parsing.write_csv(prices)
                # data_hotel.append(prices)
        js_data =  json.dumps(data_json, indent=4)   
        print js_data
        return data_json


def send_email():
    msg = MIMEMultipart()
    msg['Subject'] = 'booking price' 
    msg['From'] = 'booking@serviziocorsa.com'
    msg['To'] = 'J@grobman.de'
    part = MIMEBase('application', "octet-stream")
    part.set_payload(open("out/booking.xls", "rb").read())
    Encoders.encode_base64(part)

    part.add_header('Content-Disposition', 'attachment; filename="booking.xls"')

    msg.attach(part)

    server = smtplib.SMTP('localhost')
    server.sendmail(msg['From'], msg['To'], msg.as_string())

def sendToBeds24(json_data):
        url = 'https://api.beds24.com/json/setRoomDates'
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain','Content-Encoding': 'utf-8'}
        send = requests.post(url, data=json.dumps(json_data), headers=headers)
        print(send.status_code)



def import_to_excel():
    df = pandas.read_csv('out/booking.csv', delimiter=';', names=[u'Von', 
                                                                  u'Bis',
                                                                  u'days',
                                                                  u'room',
                                                                  u'rate',
                                                                  u'mid',
                                                                  u'min',
                                                                  u'market',
                                                                  u'my_price',
                                                                  u'Novotel Actual',
                                                                  u'H4 Actual',
                                                                  u'H2 Actual',
                                                                  u'MyRoom - Top Munich Serviced Apartments',
                                                                  u'Apart Hotel Messe Munich - my room Apartments',
                                                                  u'Motel One München-Messe',
                                                                  u'Novotel std',
                                                                  u'H4 std', 
                                                                  u'H2 std',
                                                                  u'MyRoom - Top Munich Serviced Apartments std',
                                                                  u'Apart Hotel Messe Munich - my room Apartments std',
                                                                  u'Motel One München-Messe std'], encoding='utf-8')
    df.to_excel('out/booking.xls', index = False, encoding='utf-8')
    del_csv()


def del_csv():
    if os.path.exists("out/booking.csv"):
        os.remove("out/booking.csv")


if __name__ == "__main__":
        del_csv()
        # sendToBeds24(getRooms(datenow, date365))
        getRooms(datenow, date365)
        import_to_excel()
        # send_email()

