import MySQLdb as mysql
import hashlib
import cPickle as pickle
import collections

abstracts = []
outfile=open("abs.txt","w")
multifile=open("multiples.txt","w")

class DB:
    conn = None
    """This is a class which wraps around the MySQLdb database class.
    The only real difference here is that this DB class will try a
    query again if it catches an operational exception from mySQL.
    For example, if it cannot connect to the db, it will try again"""
    def connect(self):
        self.conn = mysql.connect(
                    host="DB HOST",
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


db=DB()


def get_abstracts():
    """Get all abstracts and save hash to pickle file and string 
    representation of list"""
    pickle_file = open("abstracts.pkl", 'a')
    abstract = {}
    db.connect()
    sql = "SELECT wos_id,abstracts FROM abstracts"
    cursor = db.query(sql)
    res = cursor.fetchone()
    while res:
        m = hashlib.md5()
        m.update(res[1])
        md5sum = m.digest()
        abstract[res[0]] = md5sum
        pickle_file.write(pickle.dumps(abstract))
        abstracts.append(abstract)
    outfile.write(abstracts)

get_abstracts()

def compare_abstracts(abstracts):
    """Compare all hashes and save duplicates"""
    multiples=[]
    for abstract in abstracts:
        if abstract.values()[0] not in multiples:
            multiples.append(abstract)
    counter=collections.Counter(multiples)
    file=open("abstracts.txt")
    file.write(json.dumps(counter))

compare_abstracts(abstracts)

