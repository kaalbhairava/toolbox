import urllib.request
import time
import logging
import datetime
import argparse
import sys
import ipaddress
import ssl

parser = argparse.ArgumentParser(description='keyword based web scrapping for ip set or single ip',add_help=False)

parser.add_argument('-h','--help',action='help',help='Example: web_scrapper.py -t 192.168.10.0/24 or ip_filename or ip_address or comma separated ips -w search_keyword')

parser.add_argument('-t','--target',required=True,help='single ip_address or subnet or file_name or comma separated ips')

parser.add_argument('-w','--keyword',required=True,help='keyword for web scrapping')

parser.add_argument('-p','--port',default='80,443',help='destination port')

parser.add_argument('-P','--path',default='/',help='url path e.g. http://10.0.0.1/admin.php [ -P /admin.php]')

parser.add_argument('-o','--out',default='scrap_result.log',help='filename to write output to')

args = parser.parse_args()

target = args.target
keyword = args.keyword
outfile = args.out
port = args.port
path = args.path

ips =[]
ports=[]

try:
    if '.txt' in target:
        with open(target,'r') as fr:
            ips = fr.read().splitlines()
    elif '/' in target:
        for ip_addr in ipaddress.IPv4Network(target):
            ip = str(ip_addr)
            ips.append(ip)
    elif ',' in target:
        ips=target.split(',')
    else:
        ips.append(target)

    if ',' in port:
        ports= port.split(',')
    else:
        ports.append(port)
except Exception as e:
    print(e)

logger = logging.getLogger('web_scanner_log')
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
fh = logging.FileHandler(outfile)
fh.setLevel(level=logging.DEBUG)
fh.setFormatter(formatter)
logger.addHandler(fh)
logger.info('start '+str(datetime.datetime.now()))
headers = {}

headers['User-Agent'] = "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:48.0) Gecko/20100101 Firefox/48.0"
foundip=[]

for ip in ips:
    for p in ports:
        try:
            url = 'http://'+ip+':'+p+path
            print('checking '+ip+' for url '+url)
            req = urllib.request.Request(url,headers=headers)
            html = urllib.request.urlopen(req,timeout=10).read()
            if (keyword in html.decode()) or (keyword.upper() in html.decode()) or (keyword.lower() in html.decode()):
                print('found')
                logger.info('found at '+ip)
                foundip.append(ip)
        
        
        except:
            try:
                url = 'https://'+ip+':'+p+path
                print('checking '+ip+' for url '+url)
                req = urllib.request.Request(url,headers=headers)
                html = urllib.request.urlopen(req,timeout=10,context=ssl._create_unverified_context()).read()
                
                if (keyword in html.decode()) or (keyword.upper() in html.decode()) or (keyword.lower() in html.decode()):
                    print('found')
                    logger.info('found at '+ip+' '+url)
                    foundip.append(ip)
            except Exception as e:
                print(e)

        time.sleep(5)

logger.info('end time: '+str(datetime.datetime.now()))
logging.shutdown()
    

