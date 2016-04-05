# coding=utf8
from qqwry import QQwry
from datetime import datetime
from ua_parser import user_agent_parser
from settings import HOST
from urllib.parse import quote
from settings import MONGODB_HOST, MONGODB_PORT, DATABASE, COLLECTION
from pymongo import MongoClient


q = QQwry()
q.load_file('qqwry.dat', loadindex=False)

client = MongoClient(MONGODB_HOST, MONGODB_PORT)
db = client[DATABASE]
collection = db[COLLECTION]


def analyse_client(ip, ua):
    data = {}
    data['time'] = datetime.now()
    data['location'] = get_loc_from_ip(ip)
    data['client'] = user_agent_parser.Parse(ua)
    collection.insert(data)


def get_loc_from_ip(ip):
    loc, supplier = q.lookup(ip)
    return {
        'ip': ip,
        'loc': loc,
        'supplier': supplier
    }


def gen_new_url(url):
    if not url.startswith("http:"):
        url = "http://{}".format(url)
    return "{}{}".format(HOST, quote(url))