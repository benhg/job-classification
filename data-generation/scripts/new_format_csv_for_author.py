import sqlite3
import csv
import random
import MySQLdb as mysql
import ast
import multiprocessing

"""Collection of functions useful for creating sample and gettting data
to load qualtrics survey with."""

conn = sqlite3.connect('edge_data.db')


class DB():
    conn = None
    """This is a class which wraps around the MySQLdb database class.
    The only real difference here is that this DB class will try a
    query again if it catches an operational exception from mySQL.
    For example, if it cannot connect to the db, it will try again"""

    def __init__(self, db):
        self.db = db

    def connect(self):
        self.conn = mysql.connect(host="HOST",
                                  user="USER",
                                  passwd="PASS", db=self.db)

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


db = DB(db="wos2")
db2 = DB(db="wos")


def append_to_csv(wos_id):
    """Populates csv with lead author of paper with wos_id provided
    Rewritten to use a csv DictWriter, so that we don't need to worry
    about ordering our list"""
    db.connect()
    sql = """SELECT subject FROM subjects WHERE wos_id='{}'""".format(wos_id)
    field = db.query(sql).fetchone()[0]
    line = {}
    csv_fieldnames = ['First Name', 'Last Name', "Email", 'title', 'abstract',
                      'year', 'amzn', 'title1', 'journal1', 'authors1',
                      'abstract1', 'year1', 'title2', 'journal2', 'authors2',
                      'abstract2', 'year2', 'title3', 'journal3', 'authors3',
                      'abstract3', 'year3']
    list_of_citation_wos_ids = get_author_citations(wos_id)
    citations = [get_info(cited_wos_id, n) for n, cited_wos_id in enumerate(list_of_citation_wos_ids)]
    c = csv.DictWriter(open("{}_papers.csv".format(field), "a"), fieldnames=csv_fieldnames)
    for citation in citations:
        line.update(citation)
    db.connect()
    sql = """SELECT first_name,last_name,email_addr,title,abstract,pubyear
    FROM publications JOIN contributors
    ON contributors.wos_id=publications.wos_id
    JOIN abstracts ON abstracts.wos_id=contributors.wos_id
    WHERE contributors.wos_id='{}' AND position=1""".format(wos_id)
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


def get_author_citations(wos_id):
    """Gets a list of all citations that a paper makes"""
    c = conn.cursor()
    sql = "SELECT int_id FROM mapping WHERE wos_id='{}'".format(wos_id)
    c.execute(sql)
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


def generate_citation_sample(wos_id):
    """If a paper makes more than 3 citations, we randomly select 3
    If a paper makes less than 3 citations, we can't ask the author
    about 3 citations, so we can't use it"""
    list_of_citations = get_author_citations(wos_id)
    if len(list_of_citations) < 3:
        return -1
    elif len(list_of_citations) == 3:
        return list_of_citations
    else:
        used_citations = []
        for i in range(4):
            rdm = random.choice(list_of_citations)
            if rdm not in used_citations:
                used_citations.append(rdm)
        return used_citations


def make_samples(fields):
    """Make csv files for field @param fields,
    using papers from @param papers in parallel"""

    for field in fields:
        create_csv(field)
        papers = get_papers(field)
        pool2 = multiprocessing.Pool(500)
        output2 = pool2.map(append_to_csv, papers)


def get_papers(field):
    papers_list = ast.literal_eval(open("wos_ids_{}.txt".format(field)).read())
    papers = []
    while len(papers) < 500:
        rdm = random.choice(papers_list)[0]
        if rdm not in papers:
            papers.append(rdm)
    return papers


make_samples(['Surgery'])
