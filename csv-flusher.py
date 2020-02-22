#! /usr/local/bin/python3
# -*-coding:utf-8 -*
from ScrapperSeisme import ScrapperSeisme
import csv
from sys import argv
def r(p):
    return p

csvfile_out=argv[1]
def writeCSV(pool,outname):

    with open(outname, 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(["id","date_time_local","date_time_UTC","country","city","distance","longitude","latitude","depth","magnitude","magnitude_unit","validation","type"])
        for sid in pool:
            s=pool[sid]
            spamwriter.writerow([sid,s.date_time_local,s.date_time_UTC,s.country,s.city,s.distance,s.longitude,s.latitude,s.depth,s.magnitude,s.magnitude_unit,s.validation,s.type])


scr = ScrapperSeisme(nb_threads=16,save_path="output.json")

pool = scr.apply_to_pool(r)
writeCSV(pool,csvfile_out)
