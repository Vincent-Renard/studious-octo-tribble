#! /usr/local/bin/pypy3
# -*-coding:utf-8 -*
from time import sleep

import requests,threading,json,operator
from datetime import datetime
from bs4 import BeautifulSoup
from os import path
import multiprocessing as mp
from Seisme import Seisme
from tqdm import tqdm

class ScrapperSeisme:
    """ScrapperSeisme : Scrapper for renass unistra / seismes """
    ## TODO: Mettre même patern dans json pour les date heures
    def __init__(self, base_url,nb_threads=4,save_path=None):
        self.__base_url = base_url
        self.__nthreads=nb_threads
        self.__save_path=save_path
        self.__pool=dict()

        if save_path is not None:
            self.__deserialize()

    def __deserialize(self):
        if path.exists(self.__save_path):
            with open(self.__save_path,"r") as f_in:
                    f=f_in.read()
                    for seisme_serialized in f.split(';')[:-1]:
                        s=Seisme()
                        s.from_JSON(seisme_serialized)
                        #print(s.id)
                        self.__pool[s.id]=s


    def __avg(self,list):
        if (len(list)):
            return sum(list)/len(list)
        else:
            return 0

    def __find_borders(self,url):
        """
        Retrouve les bornes contenant la page pivot
        url: url de la page-mère
        """

        w = self.__get_weight_page(url,1)
        weights ,lp= [],[]
        p=1
        while (not( w < self.__avg(weights)/2 )):
            lp.append(p)
            w = self.__get_weight_page(url,p)
            #print(p,w)
            weights.append(w)
            if p > 1:
                p*=2
            else:
                p=2
        r = lp[-2:]
        return r[0] ,r[1]

    def __page_compare(self,val_in,val_out,url,n_page):
        val_p=self.__get_weight_page(url,n_page)
        val_p_next=self.__get_weight_page(url,n_page+1)
        if val_p > val_in//4 and val_p_next == val_out :
            return 0
        if val_p > val_in//4 and val_p_next > val_in//4:
            return 1
        else:
            return -1



    def __find_first_page(self,url,strt,end):
        val_out=self.__get_weight_page(url,end)
        val_in=self.__get_weight_page(url,strt)
        p=end-strt
        r=self.__page_compare(val_in,val_out,url,p)
        i=0

        while r!=0:
            p=p+r*end
            end=end//2
            r=self.__page_compare(val_in,val_out,url,p)
            i+=1


        return p

    def __get_weight_page(self,url,n):
        return len(self.__parse_content(url+str(n)).getText())

    def __parse_content(self,url):
        requete = requests.get(url)
        cont = requete.content
        soup = BeautifulSoup(cont, features="html.parser")

        return soup


    def get_seisms(self,page):
        content_page = self.__parse_content(page)
        seismes = []
        trs = content_page.find_all('tr')
        i=0
        for record in trs[1:]:
            try:
                m = record.find("a")
                id = str(m).split('\"')[1].split('/')[2]
                if id not in self.__pool:
                    s = Seisme()
                    s.id=id
                    img = record.find("img")
                    country = img.get('alt')
                    s.country=country
                    event = self.__get_event(s.id)
                    s=self.__read_event(event,s)
                    self.__add(s)


            except IndexError as e:
                pass

        return seismes
    def __get_event(self,id):

        p="https://renass.unistra.fr/evenements/"+id

        requete = requests.get(p)
        cont = requete.content
        soup = BeautifulSoup(cont, features="html.parser")

        return soup


    def __read_event(self,event,seisme):

            valid = event.find_all('div',{"class": "alert alert-error"})
            if(len(valid)>0):
                seisme.validation=False
            else:
                seisme.validation=True
            trs = event.find_all('tr')
            #0 dateheure locale

            seisme.set_date_local(str(trs[0].getText()).split('\n')[2])
            #1 dateheure UTC
            seisme.set_date_UTC(str(trs[1].getText()).split('\n')[2])
            #2 : latitude
            la=str(trs[2].getText()).split('\n')[2][:-1]
            la=float(la)
            seisme.latitude=la
            #3 : longitude
            lo=str(trs[3].getText()).split('\n')[2][:-1]
            lo = float(lo)
            seisme.longitude=lo
            #4 : Profondeur
            pro1 = (str(trs[4].getText()).split('\n')[2])
            pro = pro1.split(' ')
            val_depth=int(pro[0])
            #print(pro)
            seisme.depth=val_depth
            #5 : magnitude
            magnitude=str(trs[5].getText()).split('\n')[2]
            magnitude=magnitude.split('\xa0')
            seisme.magnitude=magnitude[0]
            seisme.magnitude_unit= magnitude[1]
            #6 : Type
            seisme.type=str(trs[6].getText()).split('\n')[2]
            # 8: ville
            seisme.city=str(trs[8].getText()).split('\n')[1]
            return seisme

    def __add(self,seisme):
        self.__pool[seisme.id]=seisme
        
    def start(self,nb_pages=0,update=True):
        d,f=self.__find_borders(self.__base_url)
        if not update: self.__pool={}
        #print(d,f)
        derniere_page=self.__find_first_page(self.__base_url,d,f)
        #derniere_page=1976
        print(derniere_page)
        tailles = list()
        thrds = []

        if nb_pages==0:
            np=derniere_page
        else :
            np=nb_pages
        for p in tqdm(range(1,np,self.__nthreads)):
            for t_i in range(self.__nthreads):
                t = threading.Thread(target=self.get_seisms,args=(self.__base_url+str(p+t_i),))
                t.start()
                thrds.append(t)
            for th in thrds:
                th.join()
            thrds.clear()
        self.__save()

    def apply(self,fun):
        r = {}
        for sid in self.__pool:
            s=self.__pool[sid]
            s=fun(s)
            r[sid]=s
        self.__pool=r
        self.__save()

    def __sort__pool(self):

        newpool = sorted(self.__pool.values(), key=lambda x: x.date_time_UTC)
        self.__pool={}
        for c in newpool:
            self.__add(c)

    def __save(self):
        self.__sort__pool()
        with open(self.__save_path,"w") as out:
            for s in self.__pool:
                out.write(self.__pool[s].to_JSON()+';\n')
        print(len(self.__pool))
