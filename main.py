#! /usr/local/bin/pypy3
# -*-coding:utf-8 -*
from Seisme import Seisme
from datetime import date

if __name__ == '__main__':
    s = Seisme("Hosso")


    print(s.to_JSON())
    #print(s.date)
    #s.date=date.today()

    #print(s.date)
    #s.add_near_city('LOS ang',40)
    #print(s.to_JSON())
