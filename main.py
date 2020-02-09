#! /usr/local/bin/pypy3
# -*-coding:utf-8 -*

from ScrapperSeisme import ScrapperSeisme

if __name__ == '__main__':
    path = "https://renass.unistra.fr/les-derniers-seismes/page/"
    scr = ScrapperSeisme(path, nb_threads=16, save_path="seismes.json")
    scr.start(end_page=1978)
    # scr.get_seisms(67)
