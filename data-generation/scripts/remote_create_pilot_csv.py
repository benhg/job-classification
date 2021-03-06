import csv
import MySQLdb as mysql
import ast
import multiprocessing

"""Creates pilot csv for use with pilot sample of survey (we are looking for
specific people) (remote half)"""


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


def append_to_csv(tuple):
    """Populates csv with lead author of paper with wos_id provided
    Rewritten to use a csv DictWriter, so that we don't need to worry
    about ordering our list"""
    wos_id = tuple[0]
    pos = tuple[1]
    db.connect()
    field = 'pilot'
    line = {}
    csv_fieldnames = ['First Name', 'Last Name', "Email", 'title', 'abstract',
                      'year', 'amzn', 'title1', 'journal1', 'authors1',
                      'abstract1', 'year1', 'title2', 'journal2', 'authors2',
                      'abstract2', 'year2', 'title3', 'journal3', 'authors3',
                      'abstract3', 'year3']
    list_of_citation_wos_ids = ast.literal_eval(
        open('{}.txt'.format(wos_id)).read())
    citations = [get_info(cited_wos_id, n)
                 for n, cited_wos_id in enumerate(list_of_citation_wos_ids)]
    c = csv.DictWriter(
        open(
            "{}_data.csv".format(field),
            "a"),
        fieldnames=csv_fieldnames)
    for citation in citations:
        line.update(citation)
    db.connect()
    sql = """SELECT first_name,last_name,email_addr,title,abstract,pubyear
    FROM publications JOIN contributors
    ON contributors.wos_id=publications.wos_id
    JOIN abstracts ON abstracts.wos_id=contributors.wos_id
    WHERE contributors.wos_id='{}' AND position={}""".format(wos_id, pos)
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
