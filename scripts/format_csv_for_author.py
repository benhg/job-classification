import sqlite3
import csv
import random
import MySQLdb as mysql

conn = sqlite3.connect('SQLITE FILE')
global sampled_papers
sampled_papers = []


class DB:
    conn = None
    """This is a class which wraps around the MySQLdb database class.
    The only real difference here is that this DB class will try a
    query again if it catches an operational exception from mySQL.
    For example, if it cannot connect to the db, it will try again"""
    def connect(self):
        self.conn = mysql.connect(host="DB HOST",
                                  user="DB USER",
                                  passwd="DB PASS", db="wos2")

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


def get_author_citations(wos_id):
    """Gets a list of all citations that a paper makes"""
    c = conn.cursor()
    sql = "SELECT int_id FROM mapping WHERE wos_id='{}'".format(wos_id)
    c.execute(sql)
    int_id = c.fetchone()
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


def get_info(citation_wos_id):
    """gets information about a citation.
    Will return authors' names and year of cited paper"""
    sql = """SELECT pubyear, display_name, title, source
    FROM contributors
    join publications on contributors.wos_id=publications.wos_id
    WHERE publications.wos_id='{}'
    ORDER BY position ASC""".format(citation_wos_id.split('.')[0])
    db.connect()
    cursor = db.query(sql)
    res = cursor.fetchall()
    print(res)
    year = res[0][0]
    lead_author = res[0][1]
    title=res[0][2]
    source=res[0][3]
    if len(res) == 1:
        citation = "[{} {}] {}. ({})".format(lead_author, year, title, source)
    else:
        citation = "[{} et al. {} {}. ({})]".format(lead_author, year, title, source)
    return citation

def generate_citation_sample(wos_id):
    """If a paper makes more than 20 citations, we randomly select 20
    If a paper makes less than 20 citations, we can't ask the author
    about 20 citations, so we can't use it"""
    list_of_citations = get_author_citations(wos_id)
    if len(list_of_citations) < 20:b
        return -1
    elif len(list_of_citations) == 20:
        sampled_papers.append(wos_id)
        return list_of_citations
    else:
        used_citations = []
        for i in range(21):
            used_citations.append(random.choice(list_of_citations))
        return used_citations


def create_csv(field):
    """Creates csv in the format that qualtrics needs"""
    c = csv.writer(open("{}_papers.csv".format(field), "w"))
    c.writerow(["First Name", "Last Name","Email", "title", "abstract", "year",
                "amzn", "cite1", "cite2","cite3", "cite4","cite5","cite6",
                "cite7", "cite8", "cite9","cite10","cite11","cite12","cite13",
                "cite14", "cite15", "cite16","cite17","cite18","cite19","cite20"])


def append_to_csv(wos_id, field):
    """Populates csv with lead author of paper with wos_id provided"""
    list_of_citation_wos_ids = generate_citation_sample(wos_id)
    list_of_citation_wos_ids=generate_20_cites(list_of_citation_wos_ids)
    citations = [get_info(paper) for paper in list_of_citation_wos_ids]
    c = csv.writer(open("{}_papers.csv".format(field), "a"))
    line = []
    db.connect()
    sql = """SELECT first_name,last_name,email_addr,title,abstract,pubyear
    FROM publications JOIN contributors
    ON contributors.wos_id=publications.wos_id
    JOIN abstracts ON abstracts.wos_id=contributors.wos_id
    WHERE contributors.wos_id='{}' AND position=1""".format(wos_id)
    cursor = db.query(sql)
    res = cursor.fetchone()
    line.extend(list(res))
    line.append("Sample Amazon Gift Code")
    line.extend(citations)
    c.writerow(line)

def generate_20_cites():
    cited_wos_ids = get_personal_citations(personal_citations)
    #hardcoded in because we have to run the MySQL part on a different machine
    #The sqlite db is on a different machine that cannot access the mysql db
    cited_wos_ids=[u'000346592400003.9', u'', u'WOS:A1997BH72F00008', u'WOS:A1984TK52800001', u'WOS:A1991GY05000003', u'WOS:A1993KU17200010', u'WOS:A1991GW75700005', u'WOS:000181178000004', u'WOS:A1996VK34100001', u'WOS:000183737000003', u'WOS:000221233300003', u'WOS:000227815400008', u'WOS:000232389800006', u'WOS:000234454900003', u'WOS:000238750000008', u'WOS:000243711600015', u'WOS:000244595100001', u'000319632600045.31', u'WOS:000268255300002', u'WOS:000270423300014', u'000345325900011.50', u'000346172000001.3', u'000346456300002.13', u'000329007600014.12', u'000345179200007.16', u'WOS:000275898300075', u'000333778400008.15', u'WOS:000208596600002', u'WOS:000278389300090', u'000301594500001.22', u'WOS:000285831900001.25', u'000344405600014.23', u'WOS:000285831900001.11', u'000334414900001.18', u'000342168500020.22', u'WOS:000285831900001.1', u'WOS:A1991FP99500014', u'WOS:000285831900001.4', u'000301594500001.3', u'000301594500001.4', u'WOS:000285831900001.13', u'000339113300008.8', u'000344748400006.5', u'WOS:000285831900001.20', u'WOS:000285831900001.23', u'WOS:000285831900001.24', u'WOS:000285831900001.30', u'WOS:000285831900001.39', u'WOS:000285831900001.49', u'000301594500001.39', u'000301594500001.42']
    cites=[]
    while len(cites) <20:
        print len(cites)
        rdm=random.choice(cited_wos_ids)
        if rdm not in cites and 'WOS:' in rdm:
            cites.append(rdm)
        return cites
 

create_csv("ComputerScience")
append_to_csv("WOS:000285831900001", "ComputerScience")
