#!/usr/bin/env/ python
"""Process BSE's equity file and store in redis"""


from urllib.request import urlretrieve
import zipfile
import time
import redis
import csv
import json

REDIS_HOST = 'localhost'
conn = redis.Redis(REDIS_HOST)


today = time.strftime("%d%m%y")
#today = '260119'
base_url = "https://www.bseindia.com/download/BhavCopy/Equity/EQ" + today + "_CSV.ZIP"
filename = "EQ" + today + "_CSV.ZIP"
csv_filename = "./CSVFiles/" + "EQ" + today + ".CSV"


def download_extract(file_url):
    urlretrieve(file_url, filename)
    with zipfile.ZipFile(filename, "r") as z:
        z.extractall("./CSVFiles")


def read_csv(csvname):
    with open(csvname, "r") as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)
        for line in csv_reader:
            data_id = line[0]
            details = line[1:]
            store_data(data_id, details)
            #return data_id, details


def store_data(r_id, r_details):
    if r_id not in conn:
        for i in r_details:
            conn.lpush(r_id, i)
    #return data


def main():
    try:
        download_extract(base_url)
    except:
        print("The file you are looking for is not updated yet!! "
              "Kindly check back after sometime.")                    # In case file is not updated yet
    csv_data = read_csv(csv_filename)
    #db_data = store_data(csv_data)
    #print(json.dumps(store_data(csv_data)))


if __name__ == '__main__':
    conn.flushall()
    main()

    #read_csv(csv_filename)
