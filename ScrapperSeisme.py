#! /usr/local/bin/pypy3
# -*-coding:utf-8 -*
from time import sleep

import requests,os,threading,random,json
from bs4 import BeautifulSoup
from sys import argv
import multiprocessing as mp
from Seisme import Seisme

class ScrapperSeisme:
    """docstring for ScrapperSeisme."""

    def __init__(self, base_url,nb_threads=4,save_path=None):
        self._base_url = base_url
        self._nthreads=nb_threads
        if save_path is None :
            self._pool=dict()
        else:

            # from json
            pass


    def avg(self,list):
        if (len(list)):
            return sum(list)/len(list)
        else:
            return 0

    def find_borders(self,url):
        """
        Retrouve les bornes contenant la page pivot
        url: url de la page-mère
        """
        w = self.get_weight_page(url,1)
        weights ,lp= [],[]
        p=1
        while (not( w < self.avg(weights)/2 )):
            lp.append(p)
            w = self.get_weight_page(url,p)
            #print(p,w)
            weights.append(w)
            if p > 1:
                p*=2
            else:
                p=2
        r = lp[-2:]
        return r[0] ,r[1]

    def page_compare(self,val_in,val_out,url,n_page):
        val_p=self.get_weight_page(url,n_page)
        val_p_next=self.get_weight_page(url,n_page+1)
        if val_p > val_in//4 and val_p_next == val_out :
            return 0
        if val_p > val_in//4 and val_p_next > val_in//4:
            return 1
        else:
            return -1



    def find_first_page(self,url,strt,end):
        val_out=self.get_weight_page(url,end)
        val_in=self.get_weight_page(url,strt)
        p=end-strt
        r=self.page_compare(val_in,val_out,url,p)
        i=0

        while r!=0:
            p=p+r*end
            end=end//2
            r=self.page_compare(val_in,val_out,url,p)
            i+=1


        return p

    def get_weight_page(self,path,n):
        return len(self.parse_content(path,n).getText())

    def parse_content(self,uri,nombre=None):

        if nombre is not None:
            uri += str(nombre)
        requete = requests.get(uri)
        cont = requete.content
        soup = BeautifulSoup(cont, features="html.parser")

        return soup



    def dico(self,f,l):
        p=l-f
        r=self.oracle(p)
        i=0
        while r!=0:

            p=p+ r*(l//2)
            l=l//2
            r=self.oracle(p)
            i+=1
            print(i,p,r)




    def oracle(self,v):
        THE_VALUE = 1256
        if (v==THE_VALUE):
            return 0
        else:
            if v>THE_VALUE:
                return -1
            else:
                return 1






    def get_seisms(self,page):
        content_page = self.parse_content(page)
        seismes = []

        trs = content_page.find_all('tr')
        i=0
        for record in trs[1:]:

            s = Seisme()
            try:
                m = record.find("a")
                id = str(m).split('\"')[1].split('/')[2]
                i+=1
                s.id=id
                img = record.find("img")
                country = img.get('alt')
                s.country=country
                event = self.get_event(s.id)
                s=self.read_event(event,s)
                self._pool[s.id]=s

            except IndexError as e:
                pass

        return seismes
    def get_event(self,id):

        p="https://renass.unistra.fr/evenements/"+id
        requete = requests.get(p)
        cont = requete.content
        soup = BeautifulSoup(cont, features="html.parser")

        return soup


    def read_event(self,event,seisme):
            trs = event.find_all('tr')
            #0 dateheure locale
            seisme.date_time_local=str(trs[0].getText()).split('\n')[2]
            #1 dateheure UTC
            seisme.date_time_UTC=str(trs[1].getText()).split('\n')[2]
            #2 : latitude
            la=str(trs[2].getText()).split('\n')[2][:-1]
            la=float(la)
            #print(la)
            seisme.latitude=la
            #3 : longitude
            lo=str(trs[3].getText()).split('\n')[2][:-1]
            lo = float(lo)
            #print(lo)
            seisme.longitude=lo
            #4 : Profondeur
            pro1 = (str(trs[4].getText()).split('\n')[2])
            pro = pro1.split(' ')
            unit = pro[1]
            val_depth=int(pro[0])

            #print(pro)
            seisme.depth=val_depth
            #5 : magnitude
            magnitude=str(trs[5].getText()).split('\n')[2]
            seisme.magnitude=magnitude
            #print(magnitude)
            mag=magnitude.split()[1]
            #6 : Type
            seisme.type=str(trs[6].getText()).split('\n')[2]
            # 8: ville
            seisme.city=str(trs[8].getText()).split('\n')[1]
            return seisme



    def start(self,nb_pages=0):
        d,f=find_borders(path)

        #print(d,f)
        derniere_page=self.find_first_page(path,d,f)
        print(derniere_page)
        tailles = list()
        thrds = []
        if nb_pages==0:
            np=derniere_page
        else :
            np=nb_pages
        for p in range(1,np,self._nthreads):
            for t_i in range(self._nthreads):
                print('page : ',p+t_i)
                t = threading.Thread(target=self.get_seisms,args=(path+str(p+t_i),))
                t.start()
                thrds.append(t)
            for th in thrds:
                th.join()
            thrds.clear()
        self.stop()
    def stop(self):
        """
        with open(save_path,"w") as out:

            for s in self._pool:
                print(s)
                out.write(self._pool[s].to_JSON()+'\n')
        """
        print(len(self._pool))
        #
        return json.dumps([self._pool[s].to_JSON() for s in self._pool], ensure_ascii=False,sort_keys=False, indent=4)
