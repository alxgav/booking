#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import division
import time

class Calculate:

    def __init__(self, prices):
        self.prices = prices

    def min(self):
        if sum(self.prices)>0:
            return min(list(filter(lambda a: a != 0, self.prices))) 
        else:
            return 0    

    def max(self):
        return max(self.prices)
    
    def mid(self):
        size = len(list(filter(lambda a: a != 0, self.prices)))
        if size != 0:
            return sum(self.prices)/size
        else:
            return 500 

    def rate(self, min, mid):
        if min > 0:
            return min/mid
        else:
            return 0 

    def newPrice(self, room, daysnow, rate, min, mid, market, max):
        price = 500
        # =ЕСЛИ(B1<=2;70;ЕСЛИ(B1<7;ЕСЛИ(B16>0,6;(B18-1);B19)*(1+(3-B2)/10);B19*(1+B14)))
        # if daysnow <= 3: 
        #     price = 65
        # else:
        #     if daysnow <= 7:
        #         if rate > 0.6:
        #             price1 = min -1
        #         else:
        #             price1 = mid
        #         price = price1 * (1 + (3 - room)/10)
        #     else:
        #         price = mid * (1+SoldOutRate) 
        # if daysnow > 3 and SoldOutRate < 0.5 and mid < 100:
        #     price = mid
        # if daysnow > 3 and SoldOutRate < 0.5 and mid > 200:
        #     price = max    

        # if price == 0:
        #    price = 500

    # <=3


    # >7
        if daysnow > 14:
            price = 500
        if price == 0:
            return 500
        

    # >=4 <=7
       # if daysnow <=14:    
             
       #     price = mid        

        if room > 2:
            price = (mid+min)/2
            if market > 0.5 and mid < 100:
                price = mid
            if market < 0.5 and mid > 100:
                price = max   
            if market < 0.3:
                    price = 350   
        if room > 2 and rate >0.8:
            price = min-1

        #if room > 2 and rate <=0.8 and min > 200:
        #   price = min-1

            # <=3       
        if daysnow <= 3:
            price=min-1
        #if price <65:
        #    price = 65
                    
                    #price = 65
        #    print (daysnow, price)
        # neu regel

        if daysnow <= 3 and market < 0.3 and room <= 2:
            price = 100
            
        if daysnow <= 3 and room > 1:
            price = min*0.7    
        if daysnow <= 2 and room > 1:
            price = min*0.5    
        #if daysnow == 1 and room > 0:
        #    price = min * 0.7
        if daysnow == 1 and room > 0:
            return  55
        if daysnow == 1 and room > 0 and time.strftime('%H')>12:
           price = 55
        if price < 55:
            return 55            

        return price   
              
    def SoldOutRate(self): #market
        room_size = len(self.prices)
        room_size_zero = len(list(filter(lambda a: a!=0, self.prices)))
        return room_size_zero/room_size


