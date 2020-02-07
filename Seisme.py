#! /usr/local/bin/pypy3
# -*-coding:utf-8 -*
from datetime import datetime,date,time
import json
class Seisme(object):
    """Seisme bean"""

    def __init__(self):
        self.id=""
        self.date_time_local=datetime.today()
        self.date_time_UTC=date.today()
        self.city=''
        self.country=''
        self.nearest_cities={}
        self.longitude=0.0
        self.latitude=0.0
        self.depth=0
        self.magnitude=0.0
        self.magnitude_unit=""
        self.validation=False
        self.type=''

    def __date_from_str(self,s):
        s=s.split(' ')
        d=s[0].split('/')
        h=s[1].split(':')
        date_s=datetime(int(d[2]),int(d[1]),int(d[0]),int(h[0]),int(h[1]),int(h[2]))
        return date_s


    def set_date_local(self,d):
        self.date_time_local=self.__date_from_str(d)
        
    def set_date_UTC(self,d):
        self.date_time_UTC=self.__date_from_str(d)

    def from_JSON(self,thing):
        payload=json.loads(thing,encoding='utf8')
        self.id=payload["id"]
        self.set_date_local(payload["date_time_local"])
        self.set_date_UTC(payload["date_time_UTC"])
        self.city=payload["city"]
        self.country=payload["country"]
        #self.nearest_cities={payload["nearest_cities"][c] for c in payload["nearest_cities"]}
        self.longitude=float(payload["longitude"])
        self.latitude=float(payload["latitude"])
        self.depth=int(payload["depth"])

        self.magnitude=float(payload["magnitude"])
        self.magnitude_unit=payload["magnitude_unit"]

        self.validation=payload["validation"]
        self.type=payload["type"]


    def add_near_city(city,distance):
        self.nearest_cities[city]=distance

    def custom_converter(self,o):
        if isinstance(o,datetime):
            return "{}/{}/{} {}:{}:{}".format(o.day, o.month,o.year,o.hour ,o.minute,o.second)
        if isinstance(o,date):
            return "{}/{}/{}".format(o.day, o.month,o.year)
        if isinstance(o,time):
            return "{}:{}:{}".format(o.hour ,o.minute,o.second)

    def to_JSON(self):
        return json.dumps(self.__dict__,default = self.custom_converter, ensure_ascii=False,sort_keys=False, indent=4)
