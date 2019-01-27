#!/usr/bin/env/ python
"""Process BSE's equity file and store in redis"""


from urllib.request import urlretrieve
import zipfile
import time
import redis
import csv

REDIS_HOST = 'localhost'
conn = redis.Redis(REDIS_HOST)


#today = time.strftime("%d%m%y")
today = '250119'
base_url = "https://www.bseindia.com/download/BhavCopy/Equity/EQ" + today + "_CSV.ZIP"
filename = "EQ" + today + "_CSV.ZIP"
csv_filename = "./CSVFiles/" + "EQ" + today + ".CSV"


def download_extract(file_url):
    urlretrieve(file_url, filename)
    with zipfile.ZipFile(filename, "r") as z:
        z.extractall("./CSVFiles")


def read_csv(csvname):
    with open(csvname, "r", encoding='utf-8') as csv_file:
        first = csv_file.readline()
        header = [x.strip() for x in first.split(',')]
        csv_reader = csv.reader(csv_file)
        for line in csv_reader:
            data_id = line[0]
            details = line[1:]
            store_data(data_id, details)
        return header


def store_data(r_id, r_details):
    if r_id not in conn:
        for i in r_details:
            conn.rpush(r_id, i)


def write_data():
    try:
        download_extract(base_url)
    except:
        print("The file you are looking for is not updated yet!! "
              "Kindly check back after sometime.")                    # In case file is not updated yet
    header = read_csv(csv_filename)
    return header


def show_data(seq=conn.keys()):
    s_seq = sorted(seq)
    topten = s_seq[:10]
    codelist = []
    detaillist = {}
    for c in topten:
        code = c.decode('utf-8')
        codelist.append(code)
    for codes in codelist:
        detail = conn.lrange(codes, 0, -1)
        temp_list = []
        for i in detail:
            d = i.decode('utf-8')
            temp_list.append(d)
        detaillist[codes] = temp_list
    return detaillist


def search(name, seq=conn.keys()):
    result = []
    for item in sorted(seq):
        detail = conn.lrange(item, 0, -1)
        tempx_name = detail[0].decode('utf-8')
        temp_name = tempx_name.strip()
        #print(temp_name)
        if temp_name == name:
            d_item = item.decode('utf-8')
            result.append(d_item)
            for i in detail:
                d = i.decode('utf-8')
                result.append(d)
    return result


if __name__ == '__main__':
    conn.flushall()
    write_data()
    x = search(name='HDFC')
    print(x)
