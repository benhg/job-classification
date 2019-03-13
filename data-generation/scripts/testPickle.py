import pickle
import sqlite3
import time
conn = sqlite3.connect('/Users/ben/jevin_west/edge_data.db')


# KARIM LAKHANI WOS_ID:WOS:000247030600053

time1 = time.time()
flag = 0


def load(filename):

    with open(filename, "rb") as f:
        while True:
            try:
                yield pickle.load(f)
            except EOFError:
                break


items = load("mapping.pkl")
c = conn.cursor()


c.execute("BEGIN")
for item in items:
    int_id = list(item.keys())[0]
    wos_id = list(item.values())[0]
    if int_id > 177056639:
        time2 = time.time() - time1
        if flag == 0:
            print(time2)
            flag = 1
        sql = "INSERT INTO mapping VALUES ({},'{}')".format(int_id, wos_id)
        c.execute(sql)
c.execute("COMMIT")
conn.commit()
conn.close()
