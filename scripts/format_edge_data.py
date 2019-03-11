"""Takes the edge data and outputs it to a SQLite3 database"""

import pickle
import sqlite3

conn = sqlite3.connect('SQLITE FILE')


def dump_mapping_to_pickle(edgefile):
    """takes the file of edge data, (wos.net) and extracts the
    wos_id:int_id mapping into pickled python dictionaries"""
    index_int = 0
    with open(edgefile, "rt") as fh:
        line = fh.readline()
        while line:
            line = fh.readline()
            line = line.split(" ")
            if line[0] != "*verticies":
                if index_int <= line[0]:
                    outfile = open("mapping.pkl", "a")
                    mapping = {}
                    mapping[int(line[0].strip())] = line[1].strip().replace('"', "")
                    # print(mapping)
                    pickle.dump(mapping, outfile)
                    outfile.close
                    index_int += 1
                else:
                    break


def load_mapping_from_pickle(filename):
    """Creates a generator which will stream one pickled dictionary
    at a time"""
    with open(filename, "rb") as f:
        while True:
            try:
                yield pickle.load(f)
            except EOFError:
                break


def insert_mapping_to_db(picklefile):
    """Takes pickle file generated with dump_mapping_tp_pickle()
    and inserts all values into sqlite3 db"""
    items = load_mapping_from_pickle(picklefile)
    c = conn.cursor()
    for item in items:
        int_id = item.keys()[0]
        wos_id = item.values()[0]
        sql = "INSERT INTO mapping VALUES ({},'{}')".format(int_id, wos_id)
        c.execute(sql)
        conn.commit()


def insert_edges_to_db(edges):
    """opens a file of edge data only (int_id:int_id) and inserts into
    sqlite3 db. File can be generated with
    `sed -n '219963475,$p' wos.net > edges`"""
    with open(edges) as file:
        line = file.readline()
        line = file.readline()
        c = conn.cursor()
        while line:
            source = int(line.split(" ")[0])
            target = int(line.split(" ")[1].strip())
            sql = "INSERT INTO edges VALUES ({},{})".format(source, target)
            c.execute(sql)
            line = file.readline()
            conn.commit()


dump_mapping_to_pickle("wos.net")
insert_mapping_to_db("mapping.pkl")
insert_edges_to_db("edges")
conn.close()
