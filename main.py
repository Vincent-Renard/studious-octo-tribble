#! /usr/local/bin/pypy3
# -*-coding:utf-8 -*
import requests,os,threading,random
from datetime import datetime,date,time
from bs4 import BeautifulSoup
from sys import argv
import multiprocessing as mp
from Seisme import Seisme
from ScrapperSeisme import ScrapperSeisme


if __name__ == '__main__':
    path= "https://renass.unistra.fr/les-derniers-seismes/page/"

    #

    scr = ScrapperSeisme(path,nb_threads=8,save_path="seismes.json")
    scr.start()
    """
    pool=scr._pool
    mags={}

    for sid in pool:

        s=pool[sid]
        m=s.magnitude_unit
        a=s.date_time_local.year
        if a not in mags:
            mags[a]={}
        if m in mags[a]:
            mags[a][m]+=1
        else:
            mags[a][m]=1

    #print(mags)
    for a in mags:
        print(a,mags[a])
    """
