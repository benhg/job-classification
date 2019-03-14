import MySQLdb as mysql
import sqlite3
import json
import csv
import random

"""This file was made in order to generate a test csv from a pre-selected wos_id
for the purpose of having real (though not randomly selected) data to test our
qualtrics survey with"""

conn = sqlite3.connect("/Users/Ben/jevin_west/edge_data.db")


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
    c = csv.DictWriter(
        open(
            "{}.csv".format(field),
            "a"),
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
