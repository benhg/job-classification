#import sqlite3
import random
import csv
import MySQLdb as mysql

"""This file was made in order to generate a test csv from a pre-selected wos_id
for the purpose of having real (though not randomly selected) data to test our 
qualtrics survey with"""

#conn=sqlite3.connect("")

class DB:
    conn = None
    """This is a class which wraps around the MySQLdb database class.
    The only real difference here is that this DB class will try a
    query again if it catches an operational exception from mySQL.
    For example, if it cannot connect to the db, it will try again"""
    def connect(self):
        self.conn = mysql.connect(host="HOST",user="USER"
                 ,passwd="PASS",db="wos2")

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

personal_citations=[166185781, 107857604, 101479912, 55111087, 75748931, 84125731,
                  76790793, 131421296, 97873936, 129227631, 132346845, 140653550,
                  142858913, 150017059, 148039376, 151839286, 155835076, 156920592,
                  167294761, 173837431, 12880295, 167011093, 166271705, 81686579, 
                  101027412, 175422885, 175809488, 158414154, 175809489, 175809490,
                  175809491, 137128944, 98982416, 161721711, 175809492, 175809493,
                  75809494, 175809495, 175809496, 175809497, 175809498, 175809499, 
                   175809500, 175809501, 175809502, 175809503, 175809504, 175809505,
                   175809506, 175809507, 175809508]



def get_personal_citations(personal_citations):
    """Will go through list of citations that I generated manually"""
    citations=[]
    c=conn.cursor()
    for cite in personal_citations:
            sql = "select wos_id from mapping where int_id={}".format(cite)
            c.execute(sql)
            res = c.fetchone()
            citations.append(res[0])
    return citations


def append_to_csv(wos_id, field):
    """Populates csv with lead author of paper with wos_id provided
    NOTE:WOS:000285831900001 is the one we're using for now"""
    list_of_citation_wos_ids = cited_wos_ids
    citations = [get_info(paper) for paper in list_of_citation_wos_ids]
    c = csv.writer(open("{}_papers.csv".format(field), "a"))
    line = []
    db.connect()
    sql = """SELECT first_name,last_name,email_addr,title,abstract,pubyear
    FROM publications JOIN contributors
    ON contributors.wos_id=publications.wos_id
    JOIN abstracts ON abstracts.wos_id=contributors.wos_id
    WHERE contributors.wos_id='{}' AND position=2""".format(wos_id)
    # position=2 because we're using a specific paper for this test
    cursor = db.query(sql)
    res = cursor.fetchone()
    line.extend(list(res))
    line.append("Sample Amazon Gift Code")
    line.extend(citations)
    c.writerow(line)


def create_csv(field):
    """Creates csv in the format that qualtrics needs"""
    c = csv.writer(open("{}_papers.csv".format(field), "w"))
    c.writerow(["First Name", "Last Name","Email", "title", "abstract", "year",
                "amzn", "cite1", "cite2","cite3", "cite4","cite5","cite6",
                "cite7", "cite8", "cite9","cite10","cite11","cite12","cite13",
                "cite14", "cite15", "cite16","cite17","cite18","cite19","cite20"])


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

def generate_20_cites():
    #cited_wos_ids = get_personal_citations(personal_citations)
    #hardcoded in because we have to run the MySQL part on a different machine
    #The sqlite db is on a different machine that cannot access the mysql db
    cited_wos_ids=['000346592400003.9', '', 'WOS:A1997BH72F00008', 'WOS:A1984TK52800001', 'WOS:A1991GY05000003', 'WOS:A1993KU17200010', 'WOS:A1991GW75700005', 'WOS:000181178000004', 'WOS:A1996VK34100001', 'WOS:000183737000003', 'WOS:000221233300003', 'WOS:000227815400008', 'WOS:000232389800006', 'WOS:000234454900003', 'WOS:000238750000008', 'WOS:000243711600015', 'WOS:000244595100001', '000319632600045.31', 'WOS:000268255300002', 'WOS:000270423300014', '000345325900011.50', '000346172000001.3', '000346456300002.13', '000329007600014.12', '000345179200007.16', 'WOS:000275898300075', '000333778400008.15', 'WOS:000208596600002', 'WOS:000278389300090', '000301594500001.22', 'WOS:000285831900001.25', '000344405600014.23', 'WOS:000285831900001.11', '000334414900001.18', '000342168500020.22', 'WOS:000285831900001.1', 'WOS:A1991FP99500014', 'WOS:000285831900001.4', '000301594500001.3', '000301594500001.4', 'WOS:000285831900001.13', '000339113300008.8', '000344748400006.5', 'WOS:000285831900001.20', 'WOS:000285831900001.23', 'WOS:000285831900001.24', 'WOS:000285831900001.30', 'WOS:000285831900001.39', 'WOS:000285831900001.49', '000301594500001.39', '000301594500001.42']
    cites=[]
    while len(cites) <20:
        print(len(cites))
        rdm=random.choice(cited_wos_ids)
        if rdm not in cites and 'WOS:' in rdm:
            cites.append(rdm)
        print(cites)

cited_wos_ids=['WOS:000270423300014', 'WOS:000183737000003', 'WOS:000268255300002', 'WOS:000285831900001.20', 'WOS:000285831900001.25', 'WOS:000275898300075', 'WOS:000285831900001.23', 'WOS:000285831900001.11', 'WOS:000285831900001.4', 'WOS:A1991GW75700005', 'WOS:000232389800006', 'WOS:A1996VK34100001', 'WOS:A1991GY05000003', 'WOS:000285831900001.24', 'WOS:000278389300090', 'WOS:000238750000008', 'WOS:A1997BH72F00008', 'WOS:000285831900001.30', 'WOS:A1984TK52800001', 'WOS:000285831900001.13']

append_to_csv('WOS:000285831900001', 'ComputerScience')
