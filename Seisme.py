#! /usr/local/bin/pypy3
# -*-coding:utf-8 -*
from datetime import datetime,date,time
import json
class Seisme(object):
    """Seisme bean"""

    def __init__(self,name):
        self.date_time_local=date.today()
        self.date_time_UTC=date.today()
        self.name = name
        self.country=''
        self.nearest_cities={}
        self.longitude=0.0
        self.latitude=0.0
        self.depth=0
        self.magnitude=0.0
        self.validation=False
        self.type=''

    def add_near_city(city,distance):
        self.nearest_cities[city]=distance

    def custom_converter(self,o):
        if isinstance(o,datetime):
            return "{}/{}/{} - {}:{}:{}".format(o.day, o.month,o.year,o.hour ,o.minute,o.second)
        if isinstance(o,date):
            return "{}/{}/{}".format(o.day, o.month,o.year)
        if isinstance(o,time):
            return "{}:{}:{}".format(o.hour ,o.minute,o.second)
    def to_JSON(self):
        return json.dumps(self.__dict__,default = self.custom_converter, sort_keys=False, indent=4)
