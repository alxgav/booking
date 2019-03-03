#!/usr/bin/python
# -*- coding: utf8 -*-
import requests
from bs4 import BeautifulSoup
import csv, time

hotel_id = {'63365', '714886', '714905', '4266142', '4304096', '3631381'}
user_agent = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}

def get_html(URL):
    return requests.get(URL, headers=user_agent).text

def parse_all(checkin='2019-01-01', checkout='2019-01-01'):
    checkin_month = checkin[5:7].strip()
    checkin_monthday = checkin[8:10].strip()
    checkin_year = checkin[0:4].strip()
    checkout_month = checkout[5:7].strip()
    checkout_monthday = checkout[8:10].strip()
    checkout_year = checkout[0:4].strip()
    nov = ''
    nov_std = ''
    H2 = ''
    H2_std = ''
    H4 = ''
    H4_std = ''
    H3 = ''
    H3_std = ''
    H5 = ''
    H5_std = ''
    H6 = ''
    H6_std = ''
    data_hotel = []
    name = ''
    price = 0
    price_std = 0
    url3 = 'https://www.booking.com/searchresults.de.html?aid=304142&label=gen173nr-1FCAEoggI46AdIM1gEaLYBiAEBmAEhuAEZyAEP2AEB6AEB-AELiAIBqAID&sid=573ff0c579984e0f58353621545ebe5f&ac_click_type=b&ac_position=0&checkin_month='+checkin_month+'&checkin_monthday='+checkin_monthday+'&checkin_year='+checkin_year+'&checkout_month='+checkout_month+'&checkout_monthday='+checkout_monthday+'&checkout_year='+checkout_year + \
        '&city=-1829149&class_interval=1&dest_id=-1829149&dest_type=city&from_sf=1&group_adults=1&group_children=0&highlighted_hotels=4266142&label_click=undef&no_rooms=1&raw_dest_type=hotel&room1=A&sb_price_type=total&search_selected=1&shw_aparth=1&slp_r_match=0&src=searchresults&srpvid=257b4c2f42cb05d2&ss=MyRoom%20-%20Top%20Munich%20Serviced%20Apartments%2C%20M%C3%BCnchen%2C%20Bayern%2C%20Deutschland&ss_raw=MyRoom%20-%20Top%20Munich%20Serviced&ssb=empty&ssne_untouched=M%C3%BCnchen&nflt=di%3D579%3B&rsf=di-579&lsf=di%7C579%7C17;selected_currency=EUR'  
    #print (url3)
    soup = BeautifulSoup(get_html(url3), 'lxml')
    hotels = soup.find_all('div', class_='sr_item')
    # time.sleep(2)
    for i in hotels:
        if i.get('data-hotelid') in hotel_id:
            try:
                name = i.find('span', class_='sr-hotel__name').text.strip()
            except:
                name = ''
            try:
                price = int(i.find('strong', class_='price').text.strip().replace(u'€\xa0', ''))
            except:
                price = 0  
            try:
                price_std = int(i.find('span', class_='strike-it-red_anim').text.strip().replace(u'€\xa0', ''))
            except:
                price_std = 0
            print(i.get('data-hotelid'), name, price, price_std, checkin, checkout)
            data_hotel.append([name, price, price_std, i.get('data-hotelid')])
            prices = ';'.join(map(str, data_hotel))
            for row in prices.split(';'):
                if '63365' in row:
                    nov = row.split(',')[1]
                    nov_std = row.split(',')[2]
                elif '714886' in row:
                    H4 = str(row.split(',')[1])
                    H4_std = str(row.split(',')[2])
                elif '714905' in row:
                    H2 = row.split(',')[1]
                    H2_std = row.split(',')[2]
                elif '4266142' in row:
                    H3 = row.split(',')[1]
                    H3_std = row.split(',')[2]
                elif '4304096' in row:
                    H5 = row.split(',')[1]
                    H5_std = row.split(',')[2]
                elif '3631381' in row:
                    H6 = row.split(',')[1]
                    H6_std = row.split(',')[2]        
    data = {'Von': checkin,
            'Bis': checkout,
            'days': 0,
            'room': 4,
            'rate': 0,
            'mid': 0,
            'min': 0,
            'market': 0,
            'my_price': 0,
            'H1': nov,  #Novotel_Actual
            'H4': H4, #H4_Actual
            'H2': H2, #H2_Actual
            'H3': H3,
            'H5': H5,
            'H6': H6,
            'H1_std': nov_std, #Novotel_Actual_std
            'H4_std': H4_std, #H4_Actual_std
            'H2_std': H2_std, #H2_Actual_std
            'H3_std': H3_std, #H3_std
            'H5_std': H5_std, #H5_std
            'H6_std': H6_std} #H6_std
    # write_csv(data)    
    return data    




def write_csv(data, filename='out/booking.csv'):
    csv.register_dialect('myDialect', delimiter=';',
                         quoting=csv.QUOTE_ALL, quotechar='"')
    with open(filename, 'a') as f:
        writer = csv.writer(f, dialect='myDialect')
        writer.writerow((data['Von'],
                         data['Bis'],
                         data['days'],
                         data['room'],
                         data['rate'],
                         data['mid'],
                         data['min'],
                         data['market'],
                         data['my_price'],
                         data['H1'],
                         data['H4'],
                         data['H2'],
                         data['H3'],
                         data['H5'],
                         data['H6'],
                         data['H1_std'],
                         data['H4_std'],
                         data['H2_std'],
                         data['H3_std'],
                         data['H5_std'],
                         data['H6_std']))
