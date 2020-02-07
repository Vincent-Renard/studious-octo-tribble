#! /usr/local/bin/pypy3
# -*-coding:utf-8 -*

from ScrapperSeisme import ScrapperSeisme



if __name__ == '__main__':
    path= "https://renass.unistra.fr/les-derniers-seismes/page/"
    scr = ScrapperSeisme(path,nb_threads=8,save_path="seismes.json")
    scr.start()
