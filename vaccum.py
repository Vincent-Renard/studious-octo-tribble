#! /usr/local/bin/pypy3
# -*-coding:utf-8 -*
import requests
from bs4 import BeautifulSoup
from sys import argv
import multiprocessing as mp

def avg(list):
    if (len(list)):
        return sum(list)/len(list)
    else:
        return 0

def find_borders(url):
    """
    Retrouve les bornes contenant la page pivot
    url: url de la page-mère
    """
    w = get_weight_page(url,1)
    weights ,lp= [],[]
    p=1
    while (not( w < avg(weights)/2 )):
        lp.append(p)
        w = get_weight_page(url,p)
        #print(p,w)
        weights.append(w)
        if p > 1:
            p*=2
        else:
            p=2
    r = lp[-2:]
    return r[0] ,r[1]

def page_compare(val_in,val_out,url,n_page):
    val_p=get_weight_page(url,n_page)
    val_p_next=get_weight_page(url,n_page+1)

    if val_p > val_in//4 and val_p_next == val_out :
        #print(" comp",n_page,val_p,val_p_next,"( ZERO ) ",end='')
        return 0
    if val_p > val_in//4 and val_p_next > val_in//4:
        #print(" comp",n_page,val_p,val_p_next," ( -1 ) ",end='')
        return 1
    else:
        #print(" comp",n_page,val_p,val_p_next," ( 1 ) ",end='')
        return -1



def find_first_page(url,strt,end):
    val_out=get_weight_page(url,end)
    val_in=get_weight_page(url,strt)
    p=end-strt
    r=page_compare(val_in,val_out,url,p)
    i=0

    while r!=0:
        p=p+r*end
        end=end//2
        r=page_compare(val_in,val_out,url,p)
        i+=1


    return p

def get_weight_page(path,n): return len(parse_content(path,n).getText())

def parse_content(url,nombre):
    requete = requests.get(path+str(nombre))
    cont = requete.content
    soup = BeautifulSoup(cont, features="html.parser")

    return soup

def save_html(page,n):
    s= parse_content(page,n)
    if (len(s.getText())!= 1604):
        with open("ht/seisme_"+str(n)+".html","w") as f :
            f.write(str(s))



'''
      <th>Date</th>
      <th>Heure UTC</th>
      <th>Heure locale</th>
      <th>Magnitude</th>
      <th>Latitude</th>
      <th>Longitude</th>
      <th>Status</th>
      Type event
      Validé ?

'''

def dico(f,l):
    p=l-f
    r=oracle(p)
    i=0
    while r!=0:

        p=p+ r*(l//2)
        l=l//2
        r=oracle(p)
        i+=1
        print(i,p,r)




def oracle(v):
    THE_VALUE = 1256
    if (v==THE_VALUE):
        return 0
    else:
        if v>THE_VALUE:
            return -1
        else:
            return 1


def get_seisms(content_page):

    balsis = [s for s in content_page.find_all('tr')]
    ses=[]
    b=balsis[1]
    #for b in balsis:
    print(b)
    t = [s for s in str(b).split("\n")]
    for i in t:

        print(i)
    n=0


    return ses

min = 1

path= "https://renass.unistra.fr/les-derniers-seismes/page/"
page = parse_content(path,34)
#print(page)

for s in get_seisms(page):
    print("\n\n\n\n\n\n\n",s)



'''

d,f=find_borders(path)
#d,f=1024 ,2048

print(d,f)

derniere_page=find_first_page(path,d,f)
print(derniere_page)

PREMIERE PAGE
find_first_page(path,d,f)
https://renass.unistra.fr/les-derniers-seismes/page/1920
tailles = list()
thrds = []

for p in range(1,1920,5):
    for i in range(5):
        print('page : ',p+i)
        t = mp.Process(target=save_html,args=(path,p+i))
        t.start()
        thrds.append(t)
    for th in thrds:
        th.join()
    thrds.clear()
    '''
