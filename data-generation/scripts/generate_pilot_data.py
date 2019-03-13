import random
import sqlite3
import multiprocessing

"""Creates pilot csv for use with pilot sample of survey (we are looking for
specific people) (local half)"""

conn = sqlite3.connect('edge_data.db')
interested_wos_ids = ['WOS:000347762000002', 'WOS:000355255600021', 'WOS:000349297300005', 'WOS:000353934700007', 'WOS:000354391000015', 'WOS:000359594300010', 'WOS:000355491800001', 'WOS:000358808900002', ]


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


def lookup(wos_id):
    """Write citation to file named as according to the wos_id"""
    outfile = open('{}.txt'.format(wos_id), 'w')
    ids_to_lookup = []
    print(wos_id)
    ids_to_lookup.extend(generate_citation_sample(wos_id))
    print(("Done WIth "+wos_id))
    outfile.write(ids_to_lookup)


pool = multiprocessing.Pool(20)
out = pool.map(lookup, interested_wos_ids)
