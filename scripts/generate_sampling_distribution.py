import sqlite3
import csv
import random
#import MySQLdb as mysql
import multiprocessing.pool
import collections
import json
import ast

conn=sqlite3.connect('/Users/ben/jevin_west/edge_data.db')
#db=DB()
citationsDict={}
percentiles={}

def get_author_citations(wos_id):
    """Gets a list of all citations that a paper makes"""
    c=conn.cursor()
    sql = "SELECT int_id FROM mapping WHERE wos_id='{}'".format(wos_id[0])
    print(sql)
    c.execute(sql)
    int_id = c.fetchone()[0]
    sql = "SELECT target FROM edges WHERE source={}".format(int_id)
    c.execute(sql)
    cites = c.fetchall()
    #We have to get the wos_ids for those papers that the paper cites
    citations = []
    for cite in cites:
        sql = "select wos_id from mapping where int_id={}".format(cite[0])
        c.execute(sql)
        res = c.fetchone()
        citations.append(res[0])
    return citations

def load_topic(filename):
    """Loads suitable papers from a string-representation
    of either a tuple or a list"""
    topic = ast.literal_eval(open(filename).read())
    return topic


def process(suitable_paper):
    """Grabs all citation wos_ids and puts them in the dictionary of 
    citations. Needs to be a function so we can parallelize easily"""
    citationsDict[suitable_paper] = get_author_citations(suitable_paper)


def postprocess_citations(topic):
    """Process aggregated data and save multiple formats of it"""
    # Flatten list of citations, keeping duplicates
    all_citations = [item for sublist in citationsDict.values() for item in sublist]
    # Count how many times papers are cited
    counter = collections.Counter(all_citations).most_common()
    output = open("counts_{}.json".format(topic))
    output.write(json.dumps(counter, indent=4))
    output.close()
    # Dump dictionary of citations to json
    citations = open("citations_{}.json".format(topic))
    citations.write(json.dumps(citationsDict, indent=4))
    citations.close()
    # calculate percentiles
    total_size = len(counter.values())
    percentile_size = total_size / 100
    for i in range(0, total_size, percentile_size):
        percentiles[i] = counter.values()[i]


pool = multiprocessing.Pool(64)
out1 = pool.map(process, load_topic("wos_ids_Surgery.txt"))
postprocess_citations()
