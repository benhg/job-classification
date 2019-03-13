import MySQLdb as mysql
import csv
import multiprocessing
class DB:
    conn = None
    """This is a class which wraps around the MySQLdb database class. 
    The only real difference here is that this DB class will try a query again if it catches an 
    operational exception from mySQL. For example, if it cannot connect to the db, it will try again"""
    def connect(self):
        self.conn = mysql.connect(host="",user=""
                 ,passwd="",db="wos2")
    def query(self, sql):
        try:
            cursor = mysql.cursors.SSCursor(self.conn)
            cursor.execute(sql)
        except (AttributeError, mysql.OperationalError):
            print("trying again")
            self.connect()
            cursor = self.conn.cursor()
            cursor.execute(sql)
        return cursor

topic="Criminology & Penology"
def process(year):
    db=DB()
    db.connect()
    sql="SELECT publications.wos_id,title,abstract FROM publications as publications join subjects as subjects on publications.wos_id=subjects.wos_id join abstracts on abstracts.wos_id=subjects.wos_id where subject='Criminology & Penology' and pubyear={}".format(year)
    print(sql)
    cursor=db.query(sql)
    res=cursor.fetchall()

    c = csv.writer(open("{}_papers.csv".format(year),"a"))
    c.writerow(["wos_id","title","abstract"])
    c.writerows(res)

pool=multiprocessing.Pool(16)
pool.map(process,list(range(2015,1999,-1)))
