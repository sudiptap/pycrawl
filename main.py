import threading
from queue import Queue
from spider import Spider
from domain import *
from general import *
import requests
import json
import string
import urllib
import os.path
import shutil
import sys

JSON_FILE_NAME = 'jsonfile.json'
PROJECT_NAME = 'viper-seo'
HOMEPAGE = sys.argv[1]#'https://www.pnc.com/en/personal-banking.html'#'http://viper-seo.com/'
print(HOMEPAGE)
DOMAIN_NAME = get_domain_name(HOMEPAGE)
QUEUE_FILE = PROJECT_NAME + '/queue.txt'
CRAWLED_FILE = PROJECT_NAME + '/crawled.txt'
NUMBER_OF_THREADS = 8
queue = Queue()
Spider(PROJECT_NAME, HOMEPAGE, DOMAIN_NAME)
count_pdf = 1;

# Create worker threads (will die when main exits)
def create_workers():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()


# Do the next job in the queue
def work():
    while True:
        url = queue.get()
        Spider.crawl_page(threading.current_thread().name, url)
        queue.task_done()


# Each queued link is a new job
def create_jobs():
    for link in file_to_set(QUEUE_FILE):
        queue.put(link)
    queue.join()
    crawl()


# Check if there are items in the queue, if so crawl them
def crawl():
    queued_links = file_to_set(QUEUE_FILE)
    if len(queued_links) > 0:
        print(str(len(queued_links)) + ' links in the queue')
        create_jobs()

def read_html_content(url):
    #url = "https://apps.pnc.com/apps/servlet/ExternalPopup?page=http://www.sec.gov/rules/final/34-51983fr.pdf"
    res = requests.get(url)
    text = res.text
    return text
    #print(text)
def store_dictionary(dictionary, key, value):
    #aDict = {}
    dictionary[key] = value
              
def jason_save(json_file_name, dictionary):    
    with open(json_file_name, 'w') as fp:
        json.dump(dictionary, fp)
        
def download_documents(image_url, type_file):
    #image_url = "http://www.sec.gov/rules/final/34-51983fr.pdf"#"https://www.python.org/static/community_logos/python-logo-master-v3-TM.png"
 
    # URL of the image to be downloaded is defined as image_url
    r = requests.get(image_url) # create HTTP response object
 
    # send a HTTP request to the server and save
    # the HTTP response in a response object called r
    with open("python_logo.pdf",'wb') as f:
 
        # Saving received content as a png file in
        # binary format
 
        # write the contents of the response (r.content)
        # to a new file in binary mode.
        f.write(r.content)

def slugify(filename):
    """
    Normalizes string, converts to lowercase, removes non-alpha characters,
    and converts spaces to hyphens.
    """   
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    valid_name = ''.join(c for c in filename if c in valid_chars)
    return valid_name
        
def download_documents1(url):
    r = requests.get(url)
    content_type = r.headers.get('content-type')

    if 'application/pdf' in content_type:
        ext = '.pdf'
        #with open('myfile'+ext, 'wb') as f:
        #    f.write(r.raw.read())
        pdfFile = urllib.request.urlopen(url)
        file = open('pdfs/'+os.path.basename(url)+ext, 'wb')
        file.write(pdfFile.read())
        file.close()
    elif 'text' in content_type:
        ext = '.html'
    else:
        ext = ''
        #print('Unknown type: {}'.format(content_type))
        

def create_dirs(dir):    
    if not os.path.exists(dir):
        os.makedirs(dir)
    else:
        shutil.rmtree(dir)           #removes all the subdirectories!
        os.makedirs(dir)
    
def another(url):
    r = requests.get(url)
    content_type = r.headers.get('content-type')

    if 'application/pdf' in content_type:
        ext = '.pdf'
    elif 'text/html' in content_type:
        ext = '.html'
    else:
        ext = ''
        print('Unknown type: {}'.format(content_type))

    with open('myfile'+ext, 'wb') as f:
       f.write(r.raw.read())   
       
def download_file(download_url):
    with open('/tmp/metadata.pdf', 'wb') as f:
        f.write(response.content)
    

#perform crawling and write the urls
create_workers()
crawl()
create_dirs('pdfs')
create_dirs('imgs')
create_dirs('txts')
#create dictionary and generate the json file
dictionary = {}
crawled_urls = PROJECT_NAME+'/crawled.txt'
lines = [line.rstrip('\n') for line in open(crawled_urls)]
for line in lines:
    content = read_html_content(line)
    store_dictionary(dictionary, line, content)
    download_documents1(line)
jason_save(JSON_FILE_NAME, dictionary)