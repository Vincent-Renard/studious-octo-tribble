#! /usr/local/bin/pypy3
# -*-coding:utf-8 -*

from ScrapperSeisme import ScrapperSeisme

import argparse



if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Get seisms from renass.unistra')
    parser.add_argument('-p', '--last_page', type=int,
                        help='N0 of last page')
    
    parser.add_argument('-n', '--nodes', default=1,
                        type=int, help='numbers of cpus, 0 = auto ')


    parser.add_argument('-j','--json_path', type=str, metavar='',
                        help='path/to/json/file/location')

    parser.add_argument('-c', '--csv_path', type=str, metavar='',required=True,
                        help='path/to/csv/output/file')


    args = parser.parse_args()

    if not args.json_path:
        args.json_path='data/output.json'

    if not args.last_page:
        args.last_page=0



    scr = ScrapperSeisme(nb_threads=args.nodes, save_path=args.json_path)
    scr.start(end_page= args.last_page, flush=True)
    scr.write_CSV(args.csv_path)
