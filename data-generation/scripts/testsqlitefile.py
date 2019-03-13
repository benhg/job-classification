import sqlite3
import csv
import random
import json
import MySQLdb as mysql
import multiprocessing
import ast
import glob
"""Collection of functions useful for creating sample and gettting data
to load qualtrics survey with."""

conn = sqlite3.connect('edge_data.db')
global sampled_papers
sampled_papers = []


class DB:
    conn = None
    """This is a class which wraps around the MySQLdb database class.
    The only real difference here is that this DB class will try a
    query again if it catches an operational exception from mySQL.
    For example, if it cannot connect to the db, it will try again"""

    def connect(self):
        self.conn = mysql.connect(host="wos2.cvirc91pe37a.us-east-1.rds.amazonaws.com",
                                  user="benjaminglick",
                                  passwd="cfa1fc20f3a7475aa41c", db="wos2")

    def query(self, sql):
        try:
            cursor = mysql.cursors.SSCursor(self.conn)
            cursor.execute(sql)
        except (AttributeError, mysql.OperationalError):
            # print("trying again")
            self.connect()
            cursor = self.conn.cursor()
            cursor.execute(sql)
        return cursor


db = DB()


def append_to_csv(wos_id, cited_wos_ids, field):
    """Populates csv with lead author of paper with wos_id provided
    Rewritten to use a csv DictWriter, so that we don't need to worry
    about ordering our list"""
    line = {}
    csv_fieldnames = ['First Name', 'Last Name', "Email", 'title', 'abstract',
                      'year', 'amzn', 'title1', 'journal1', 'authors1',
                      'abstract1', 'year1', 'title2', 'journal2', 'authors2',
                      'abstract2', 'year2', 'title3', 'journal3', 'authors3',
                      'abstract3', 'year3']
    list_of_citation_wos_ids = cited_wos_ids
    citations = [get_info(cited_wos_id, n)
                 for n, cited_wos_id in list_of_citation_wos_ids]
    c = csv.DictWriter(open("{}.csv".format(field), "a"),
                       fieldnames=csv_fieldnames)
    for citation in citations:
        line.update(citation)
    db.connect()
    sql = """SELECT first_name,last_name,email_addr,title,abstract,pubyear
    FROM publications JOIN contributors
    ON contributors.wos_id=publications.wos_id
    JOIN abstracts ON abstracts.wos_id=contributors.wos_id
    WHERE contributors.wos_id='{}' AND position=2""".format(wos_id)
    # Position=2 because we are looking for a specific paper and
    # targeting author 2
    cursor = db.query(sql)
    res = cursor.fetchone()
    line['First Name'] = res[0]
    line['Last Name'] = res[1]
    line['Email'] = res[2]
    line['title'] = res[3]
    line['abstract'] = res[4]
    line['year'] = res[5]
    line['amzn'] = "Sample Amazon Gift Code"
    c.writerow(line)


def get_info(citation_wos_id, n):
    """gets information about a citation.
    Will return authors' names and year of cited paper"""
    citation = {}
    sql = """SELECT pubyear, display_name, title, source, abstract
    FROM contributors
    join publications on contributors.wos_id=publications.wos_id
    join abstracts on contributors.wos_id=abstracts.wos_id
    WHERE publications.wos_id='{}'
    ORDER BY position ASC""".format(citation_wos_id.split('.')[0])
    db.connect()
    cursor = db.query(sql)
    res = cursor.fetchall()
    print(res)
    citation['year{}'.format(n)] = res[0][0]
    citation['title{}'.format(n)] = res[0][2]
    citation['journal{}'.format(n)] = res[0][3]
    citation['abstract{}'.format(n)] = res[0][4]
    authors = [res[i][1] for i in range(len(res))]
    auths = ""
    for author in authors:
        auths += author + ", "
    citation['authors{}'.format(n)] = auths
    return citation


def create_csv(field):
    """Creates csv in the format that qualtrics needs"""
    c = csv.writer(open("{}_papers.csv".format(field), "w"))
    c.writerow(['First Name', 'Last Name', "Email", 'title', 'abstract',
                'year', 'amzn', 'title1', 'journal1', 'authors1',
                'abstract1', 'year1', 'title2', 'journal2', 'authors2',
                'abstract2', 'year2', 'title3', 'journal3', 'authors3',
                'abstract3', 'year3'])


def generate_citation_sample(wos_id):
    """If a paper makes more than 3 citations, we randomly select 20
    If a paper makes less than 3 citations, we can't ask the author
    about 3 citations, so we can't use it"""
    list_of_citations = get_author_citations(wos_id)
    if len(list_of_citations) < 3:
        return -1
    elif len(list_of_citations) == 3:
        sampled_papers.append(wos_id)
        return list_of_citations
    else:
        used_citations = []
        for i in range(4):
            used_citations.append(random.choice(list_of_citations))
        return used_citations


def makeSamples(fields):
    for field in fields:
        create_csv(field)
        for paper in open("{}.txt".format(field)):
            append_to_csv(paper, field)


"""Creates pilot csv for use with pilot sample of survey (we are looking for
specific people) (local half)"""

conn = sqlite3.connect('edge_data.db')


def get_author_citations(wos_id):
    """Gets a list of all citations that a paper makes"""
    c = conn.cursor()
    sql = "SELECT int_id FROM mapping WHERE wos_id='{}'".format(wos_id)
    c.execute(sql)
    try:
        int_id = c.fetchone()[0]
        sql = "SELECT target FROM edges WHERE source={}".format(int_id)
        c.execute(sql)
        cites = c.fetchall()
        # We have to get the wos_ids for those papers that the paper cites
        citations = []
        for cite in cites:
            sql = "select wos_id from mapping where int_id={}".format(cite[0])
            c.execute(sql)
            res = c.fetchone()
            # Some wos_ids are in the format WOS:XXXXXXXX.YY and we only
            # want the part before the .
            citations.append(res[0].split(".")[0])
            return citations
    except Exception as e:
        print(("failed on {}".format(wos_id)))
        return []


def lookup(wos_id):
    """Write citation to file named as according to the wos_id"""
    outfile = open('{}.txt'.format(wos_id), 'w')
    ids_to_lookup = []
    print(wos_id)
    ids_to_lookup.extend(generate_citation_sample(wos_id))
    print(("Done WIth " + wos_id))
    outfile.write(ids_to_lookup)


def get_interested_wos_ids(n, field):
    re = []
    with open("wos_ids_{}.txt".format(field)) as wos_ids:
        possibles = ast.literal_eval(wos_ids.read())
        for i in range(n):
            re.append(random.choice(possibles))
    return re


interested_wos_ids2 = get_interested_wos_ids(500, "CS_AI")
pool = multiprocessing.Pool(500)
out = pool.map(lookup, interested_wos_ids)
out = pool.map(lookup, interested_wos_ids2)
create_csv("CS_AI")

for paper in glob.glob("WOS:*"):
    append_to_csv(paper.split(".")[0], ast.literal_eval(
        open(paper).read()), "CS_AI")
