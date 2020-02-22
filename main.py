#! /usr/local/bin/pypy3
# -*-coding:utf-8 -*

from ScrapperSeisme import ScrapperSeisme


if __name__ == '__main__':
    scr = ScrapperSeisme(nb_threads=4,save_path='output.json')
    scr.start(end_page=20,flush = True)
